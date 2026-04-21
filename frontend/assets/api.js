/* Tiny JSON client for the AgentCoach web backend with offline fallback.
 *
 * When the backend is not reachable OR ?demo=1 is present in the URL, we
 * substitute a scripted coach and a plausible scoring stub so the UI can
 * be explored without the python server running. The data shape is the
 * same in both paths — the UI never branches on source. */

const DEMO_OPENINGS = {
  learn: "Let's learn URL shorteners from the ground up. What do you already know about them?",
  reinforce: "We're going to reinforce what you know. Walk me through the read path first.",
  mock_system_design:
    "Great — let's design a URL shortener together. What scale are we designing for, roughly?",
};

const DEMO_REPLIES = [
  "Good start. Now walk me through the write path. A user hits POST /shorten — what happens next?",
  "You mentioned a hash. What properties does it need, and what's the risk if two inputs collide?",
  "Say we target 500 million shortens a year. How would you size the keyspace and the database?",
  "How would you handle reads? Think about caching layers and their invalidation story.",
  "Last one — how do you add rate limiting without breaking your 99.9% latency target?",
  "Let's stop there for today. Quick wrap-up coming.",
];

const DEMO_TOPICS = [
  { id: "system_design.url_shortener", name: "URL Shortener", domain: "system_design" },
  { id: "system_design.ticketmaster", name: "Ticketmaster", domain: "system_design" },
  { id: "system_design.distributed_rate_limiter", name: "Distributed Rate Limiter", domain: "system_design" },
  { id: "system_design.message_queues", name: "Message Queues (Kafka)", domain: "system_design" },
];

const DEMO_ASSESSMENT = {
  overall_score: 3.4,
  topic_name: "URL Shortener",
  mode: "mock_system_design",
  topic_id: "system_design.url_shortener",
  dimensions: [
    { name: "requirements", score: 4, evidence: "Clarified scale + traffic assumptions early." },
    { name: "high_level_design", score: 3, evidence: "Listed components but thin on data flow." },
    { name: "deep_dive", score: 3, evidence: "Touched hashing but skimmed collision handling." },
    { name: "scalability", score: 4, evidence: "Sized for 500M writes/year with numbers." },
    { name: "tradeoffs", score: 3, evidence: "Acknowledged CAP implications only when prompted." },
  ],
  strengths: [
    "Grounded the design in concrete numbers instead of hand-waving.",
    "Named the primary component cleanly.",
  ],
  areas_to_improve: [
    "Go one level deeper on the hot component — sharding, cache layer, replica lag.",
    "State trade-offs proactively rather than when I ask for them.",
  ],
  mastery_before: 38,
  mastery_after: 47,
  mastery_delta: 9,
  growth: {
    requirements: [2.5, 3.0, 3.5, 4.0],
    high_level_design: [2.0, 2.5, 3.0, 3.0],
    deep_dive: [1.5, 2.0, 2.5, 3.0],
    scalability: [2.0, 2.5, 3.5, 4.0],
    tradeoffs: [2.0, 2.0, 2.5, 3.0],
  },
};

function isDemoRequested() {
  const q = new URLSearchParams(location.search);
  return q.has("demo");
}

async function tryFetch(path, opts) {
  const res = await fetch(path, opts);
  if (!res.ok) throw new Error(`${path} → ${res.status}`);
  return res.json();
}

let demoMode = isDemoRequested();
let demoTurn = 0;

export const api = {
  get demo() { return demoMode; },

  async getTopics() {
    if (demoMode) return { topics: DEMO_TOPICS };
    try {
      return await tryFetch("/api/topics");
    } catch (e) {
      demoMode = true;
      return { topics: DEMO_TOPICS };
    }
  },

  async startSession({ mode, topic_id, user_id }) {
    if (demoMode) {
      demoTurn = 0;
      return {
        session_id: "demo-" + Math.random().toString(36).slice(2, 8),
        opening: DEMO_OPENINGS[mode] || DEMO_OPENINGS.mock_system_design,
        topic_id, topic_name: (DEMO_TOPICS.find((t) => t.id === topic_id) || {}).name || "URL Shortener",
        mode,
      };
    }
    try {
      return await tryFetch("/api/session/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode, topic_id, user_id }),
      });
    } catch (e) {
      demoMode = true;
      return this.startSession({ mode, topic_id, user_id });
    }
  },

  async turn({ session_id, user_text }) {
    if (demoMode) {
      const line = DEMO_REPLIES[Math.min(demoTurn, DEMO_REPLIES.length - 1)];
      demoTurn += 1;
      return { coach_text: line };
    }
    try {
      return await tryFetch("/api/session/turn", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id, user_text }),
      });
    } catch (e) {
      demoMode = true;
      return this.turn({ session_id, user_text });
    }
  },

  async end({ session_id, survey }) {
    if (demoMode) {
      return { session_id, ...DEMO_ASSESSMENT, survey };
    }
    try {
      return await tryFetch("/api/session/end", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id, survey }),
      });
    } catch (e) {
      demoMode = true;
      return this.end({ session_id, survey });
    }
  },

  async report(session_id) {
    if (demoMode) return { session_id, ...DEMO_ASSESSMENT };
    try {
      return await tryFetch(`/api/session/${session_id}/report`);
    } catch (e) {
      demoMode = true;
      return this.report(session_id);
    }
  },
};

export function stashReport(payload) {
  try {
    sessionStorage.setItem("agentcoach.report", JSON.stringify(payload));
  } catch (_) { /* ignore */ }
}

export function loadStashedReport() {
  try {
    const raw = sessionStorage.getItem("agentcoach.report");
    return raw ? JSON.parse(raw) : null;
  } catch (_) { return null; }
}
