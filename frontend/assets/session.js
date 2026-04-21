/* Session orchestrator — glues together:
 *   - backend (api.js) for coach turns + final scoring
 *   - SpeechSynthesis for the coach voice
 *   - SpeechRecognition for the user's voice
 *   - Wave (wave.js) for the visualization
 *   - Lyrics panel DOM for Apple-Music-style scroll
 *
 * Keyboard: hold SPACE or click the tap-talk button to open the mic.
 * Voice can be switched with ?voice=<name> (must match a browser voice).
 * The whole page degrades gracefully if mic/ASR/synth is blocked. */

import { api, stashReport } from "/assets/api.js";
import { Wave } from "/assets/wave.js";

const qs = new URLSearchParams(location.search);
const mode = qs.get("mode") || "mock_system_design";
const topic_id = qs.get("topic_id") || "system_design.url_shortener";
const user_id = qs.get("user_id") || "web-guest";

const waveEl = document.getElementById("wave");
const dotEl = document.getElementById("dot");
const lyricsEl = document.getElementById("lyrics");
const metaEl = document.getElementById("meta");
const closeEl = document.getElementById("close");
const modalEl = document.getElementById("modal");
const submitEl = document.getElementById("submit");
const tapEl = document.getElementById("tap-talk");

const wave = new Wave(waveEl);
wave.start();

const state = {
  session_id: null,
  topic_name: topic_id,
  history: [], // {speaker, text}
  turns: 0,
  ended: false,
  recognizing: false,
  lastInterim: "",
  survey: { scores: {}, word: "" },
};

/* ───────────────── lyrics ─────────────────
 * We keep 3 <div>s in the lyrics stack (past-2, past-1, current) and
 * demote them as new lines arrive. When a new line enters, we briefly
 * hold it in an `.enter` state for a fade-in.
 */
function pushLyric({ speaker, text }) {
  const rows = lyricsEl.querySelectorAll(".line");
  // Slide values up: current → past-1, past-1 → past-2, past-2 → drop.
  rows[0].textContent = rows[1].textContent;
  rows[0].dataset.speaker = rows[1].dataset.speaker || "";
  rows[0].className = "line past-2 " + (rows[0].dataset.speaker ? `speaker-${rows[0].dataset.speaker}` : "");
  rows[1].textContent = rows[2].textContent;
  rows[1].dataset.speaker = rows[2].dataset.speaker || "";
  rows[1].className = "line past-1 " + (rows[1].dataset.speaker ? `speaker-${rows[1].dataset.speaker}` : "");

  const cur = rows[2];
  cur.dataset.speaker = speaker;
  cur.classList.remove("enter");
  // Force reflow to reset animation, then apply.
  cur.className = "line current enter speaker-" + speaker;
  // eslint-disable-next-line no-unused-expressions
  cur.offsetHeight;
  cur.classList.remove("enter");
  cur.textContent = text;

  state.history.push({ speaker, text });
}

function updateCurrentLyricText(text) {
  const cur = lyricsEl.querySelector(".line.current");
  cur.textContent = text;
}

function setActiveDot(who) {
  dotEl.classList.remove("user-hot", "coach-hot");
  if (who === "user") dotEl.classList.add("user-hot");
  else if (who === "coach") dotEl.classList.add("coach-hot");
}

/* ───────────────── coach voice ───────────────── */

function pickCoachVoice() {
  const want = qs.get("voice");
  const voices = speechSynthesis.getVoices();
  if (want) {
    const match = voices.find((v) => v.name.toLowerCase().includes(want.toLowerCase()));
    if (match) return match;
  }
  // Prefer calm female en-US if available.
  return (
    voices.find((v) => /samantha/i.test(v.name)) ||
    voices.find((v) => v.lang === "en-US" && /female/i.test(v.name || "")) ||
    voices.find((v) => v.lang === "en-US") ||
    voices[0]
  );
}

function speakCoach(text) {
  return new Promise((resolve) => {
    setActiveDot("coach");
    pushLyric({ speaker: "coach", text });

    if (!("speechSynthesis" in window)) {
      // No synth — hold a soft amp while showing lyric, then move on.
      wave.hold(0.45);
      setTimeout(() => { setActiveDot(null); resolve(); },
        Math.min(6000, 600 + text.length * 40));
      return;
    }

    const u = new SpeechSynthesisUtterance(text);
    const voice = pickCoachVoice();
    if (voice) u.voice = voice;
    u.rate = 0.98;
    u.pitch = 1.0;
    u.volume = 1.0;
    u.onboundary = () => wave.pulseOnWord(0.75);
    u.onstart = () => wave.hold(0.4);
    u.onend = () => { setActiveDot(null); resolve(); };
    u.onerror = () => { setActiveDot(null); resolve(); };
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
  });
}

/* ───────────────── user voice (ASR) ───────────────── */

const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognizer = null;
if (SR) {
  recognizer = new SR();
  recognizer.lang = "en-US";
  recognizer.interimResults = true;
  recognizer.continuous = false;

  recognizer.onstart = () => {
    state.recognizing = true;
    setActiveDot("user");
    pushLyric({ speaker: "user", text: "…" });
  };
  recognizer.onresult = (ev) => {
    let interim = "";
    let final = "";
    for (let i = ev.resultIndex; i < ev.results.length; i += 1) {
      const r = ev.results[i];
      if (r.isFinal) final += r[0].transcript;
      else interim += r[0].transcript;
    }
    if (interim) {
      state.lastInterim = interim;
      updateCurrentLyricText(interim);
    }
    if (final) {
      state.lastInterim = final;
      updateCurrentLyricText(final);
    }
  };
  recognizer.onerror = () => { state.recognizing = false; setActiveDot(null); };
  recognizer.onend = async () => {
    state.recognizing = false;
    setActiveDot(null);
    const said = (state.lastInterim || "").trim();
    state.lastInterim = "";
    if (said && !state.ended) await handleUserUtterance(said);
  };
}

function startListening() {
  if (!recognizer || state.recognizing || state.ended) return;
  try { recognizer.start(); } catch (_) { /* already started */ }
}
function stopListening() {
  if (!recognizer || !state.recognizing) return;
  try { recognizer.stop(); } catch (_) { /* noop */ }
}

/* ───────────────── turn dispatcher ───────────────── */

async function handleUserUtterance(text) {
  updateCurrentLyricText(text);
  state.turns += 1;
  try {
    const { coach_text } = await api.turn({ session_id: state.session_id, user_text: text });
    if (!coach_text) return;
    await speakCoach(coach_text);
  } catch (e) {
    await speakCoach("Let me think about that — can you say a bit more?");
  }
  // After the coach is done, re-open the mic unless the user ended.
  if (!state.ended) setTimeout(startListening, 350);
}

/* ───────────────── kickoff ───────────────── */

async function init() {
  metaEl.textContent = `· ${mode.replace("_", " ")} · ${topic_id.split(".").pop().replace(/_/g, " ")}`;
  await wave.attachMic();

  const { session_id, opening, topic_name } = await api.startSession({ mode, topic_id, user_id });
  state.session_id = session_id;
  state.topic_name = topic_name;

  // Browsers need a user gesture to start speechSynthesis. Wait for the
  // first interaction (click or space) before we begin. This also doubles
  // as the push-to-talk affordance.
  const begin = async () => {
    document.removeEventListener("keydown", kickoff);
    document.removeEventListener("click", kickoff);
    tapEl.textContent = "hold space or tap to talk";
    await speakCoach(opening);
    setTimeout(startListening, 400);
  };
  const kickoff = (ev) => {
    if (ev.type === "keydown" && ev.code !== "Space") return;
    begin();
  };
  tapEl.textContent = "tap anywhere to begin";
  document.addEventListener("keydown", kickoff, { once: false });
  document.addEventListener("click", kickoff, { once: false });
}
init();

/* ───────────────── push-to-talk ───────────────── */

tapEl.addEventListener("click", () => {
  if (state.recognizing) stopListening();
  else startListening();
});
document.addEventListener("keydown", (e) => {
  if (e.code === "Space" && !e.repeat && state.session_id && !state.ended) {
    startListening();
  }
});
document.addEventListener("keyup", (e) => {
  if (e.code === "Space" && state.recognizing) stopListening();
});

/* ───────────────── end + survey ───────────────── */

closeEl.addEventListener("click", openSurvey);

function openSurvey() {
  state.ended = true;
  stopListening();
  speechSynthesis.cancel();
  modalEl.classList.add("open");
}

// Stars
modalEl.querySelectorAll(".stars").forEach((row) => {
  row.addEventListener("click", (e) => {
    const star = e.target.closest(".star");
    if (!star) return;
    const v = parseInt(star.dataset.v, 10);
    const q = row.dataset.q;
    state.survey.scores[q] = v;
    row.querySelectorAll(".star").forEach((s) => {
      s.classList.toggle("on", parseInt(s.dataset.v, 10) <= v);
    });
  });
});

submitEl.addEventListener("click", async () => {
  state.survey.word = document.getElementById("survey-word").value.trim();
  submitEl.textContent = "Rendering…";
  const report = await api.end({ session_id: state.session_id, survey: state.survey });
  stashReport(report);
  location.href = `/report.html?session=${state.session_id}`;
});
