/* Report renderer — consumes the payload returned by /api/session/end and
 * produces a generous, candidate-facing HTML report with animated bars,
 * strengths/focus-next lists, and per-dimension growth sparklines.
 *
 * The data shape is identical whether the real LLM scorer or the demo
 * stub produced it, so the rendering code is single-path. */

import { api, loadStashedReport } from "/assets/api.js";

const root = document.getElementById("report");
const timingEl = document.getElementById("timing");

const qs = new URLSearchParams(location.search);
const session_id = qs.get("session") || "";

// Prefer the payload stashed by the session page so we don't need a
// round-trip on the hot path. Fall back to the API if we arrived via a
// deep link.
const cached = loadStashedReport();
let data = cached && cached.session_id === session_id ? cached : null;

async function boot() {
  if (!data) {
    try {
      data = await api.report(session_id || "demo");
    } catch (e) {
      root.innerHTML = "<p>Report unavailable. Start a new session from the home page.</p>";
      return;
    }
  }
  render(data);
}
boot();

/* ───────────────── rendering ───────────────── */

const RUBRIC_ORDER = [
  "requirements", "high_level_design", "deep_dive", "scalability",
  "tradeoffs", "specificity", "self_awareness", "communication",
  "approach", "complexity_analysis", "edge_cases",
  "fundamentals", "rag_pipeline", "agent_systems", "practical_experience",
];

function titleCase(s) {
  return (s || "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function orderedDims(dims) {
  const m = new Map((dims || []).map((d) => [d.name, d]));
  const ordered = [];
  RUBRIC_ORDER.forEach((n) => { if (m.has(n)) { ordered.push(m.get(n)); m.delete(n); } });
  m.forEach((v) => ordered.push(v));
  return ordered;
}

function sparklinePath(values, { w, h, pad = 4 }) {
  if (!values || values.length === 0) return "";
  const lo = 1, hi = 5;
  const n = values.length;
  const step = (w - pad * 2) / Math.max(1, n - 1);
  const y = (v) => pad + (1 - (Math.max(lo, Math.min(hi, v)) - lo) / (hi - lo)) * (h - pad * 2);
  let d = "";
  for (let i = 0; i < n; i += 1) {
    const x = pad + i * step;
    d += (i === 0 ? "M" : "L") + x.toFixed(2) + "," + y(values[i]).toFixed(2) + " ";
  }
  return d.trim();
}

function sparklineSVG(values, { emphasizeLast = true } = {}) {
  const w = 260, h = 38;
  const d = sparklinePath(values, { w, h });
  if (!d) return "";
  const last = values[values.length - 1];
  const lastX = (w - 8) * ((values.length - 1) / Math.max(1, values.length - 1)) + 4;
  const lastY = 4 + (1 - (Math.max(1, Math.min(5, last)) - 1) / 4) * (h - 8);
  return `<svg class="gspark" viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="gspark-grad" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%"  stop-color="#0071e3"/>
        <stop offset="100%" stop-color="#af52de"/>
      </linearGradient>
    </defs>
    <path d="${d}" fill="none" stroke="url(#gspark-grad)" stroke-width="1.8"
      stroke-linecap="round" stroke-linejoin="round"/>
    ${emphasizeLast ? `<circle cx="${lastX.toFixed(2)}" cy="${lastY.toFixed(2)}"
      r="3.5" fill="#af52de"/>` : ""}
  </svg>`;
}

function render(d) {
  const overall = Number(d.overall_score || 0);
  const pct = Math.max(0, Math.min(1, overall / 5)) * 100;
  const mode = (d.mode || "").replace(/_/g, " ");
  const topic = d.topic_name || (d.topic_id || "").replace(/_/g, " ");
  const dims = orderedDims(d.dimensions || []);

  const dimRows = dims.map((dim) => {
    const s = Math.max(0, Math.min(5, Number(dim.score) || 0));
    const w = (s / 5) * 100;
    return `<div class="dim-row">
      <div class="name">${titleCase(dim.name)}</div>
      <div class="bar"><span data-w="${w}"></span></div>
      <div class="score">${s.toFixed(0)}<span style="color:var(--muted);font-size:14px">/5</span></div>
      ${dim.evidence ? `<div class="evidence">${escapeHtml(dim.evidence)}</div>` : ""}
    </div>`;
  }).join("");

  const strengths = (d.strengths || []).slice(0, 4)
    .map((x) => `<li>${escapeHtml(x)}</li>`).join("");
  const areas = (d.areas_to_improve || []).slice(0, 4)
    .map((x) => `<li>${escapeHtml(x)}</li>`).join("");

  const growthEntries = Object.entries(d.growth || {})
    .filter(([, vals]) => Array.isArray(vals) && vals.length >= 2);
  const growthBlock = growthEntries.length
    ? `<h2>Your growth</h2>
       <p class="sub">Per-dimension trajectory across your recent sessions.</p>
       <div class="growth-grid">
         ${growthEntries.map(([name, vals]) => `
           <div class="gname">${titleCase(name)}</div>
           ${sparklineSVG(vals)}
         `).join("")}
       </div>`
    : "";

  const masteryBlock = (typeof d.mastery_before === "number")
    ? `<div class="mastery-card module">
         <div class="topline">Topic mastery</div>
         <div class="delta">
           ${d.mastery_before}% → ${d.mastery_after}%
           <span class="sign">${(d.mastery_delta || 0) >= 0 ? "+" : ""}${d.mastery_delta || 0}</span>
         </div>
       </div>`
    : "";

  const survey = d.survey || {};
  const surveyBits = Object.keys(survey.scores || {}).length
    ? `<p class="sub">Your survey: ${Object.entries(survey.scores)
         .map(([k, v]) => `${titleCase(k)} ${v}/5`).join(" · ")}
         ${survey.word ? ` · "${escapeHtml(survey.word)}"` : ""}</p>`
    : "";

  root.innerHTML = `
    <div class="topline">${escapeHtml(mode)} · ${escapeHtml(topic)}</div>
    <h1>${overall.toFixed(1)}<span class="over">/ 5 overall</span></h1>
    <div class="hero-bar"><span data-w="${pct.toFixed(1)}"></span></div>

    <h2>Where you stood</h2>
    <p class="sub">Scored against the ${(d.mode || "").startsWith("mock") ? "mock-interview" : "rubric"} dimensions for this topic.</p>
    <div>${dimRows}</div>

    ${strengths ? `<h2>What landed</h2><ul class="list-block">${strengths}</ul>` : ""}
    ${areas ? `<h2>What to practice next</h2><ul class="list-block focus">${areas}</ul>` : ""}

    ${growthBlock}
    ${masteryBlock}
    ${surveyBits}

    <div class="footer">
      <a href="/session.html?mode=${encodeURIComponent(d.mode || "mock_system_design")}&topic_id=${encodeURIComponent(d.topic_id || "")}">Practice this again →</a>
      <a href="/">Back home</a>
    </div>
  `;

  // Animate bars on next frame.
  requestAnimationFrame(() => {
    root.querySelectorAll("[data-w]").forEach((el) => {
      el.style.width = el.dataset.w + "%";
    });
  });

  timingEl.textContent = `· session ${session_id.slice(-6) || "demo"}`;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}
