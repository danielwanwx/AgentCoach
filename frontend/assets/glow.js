// Background aurora bands (two giant off-screen discs, inner arcs peek into
// the viewport as curved light bands, Stitch-style) + per-module cursor
// tracking for the glass specular gloss. Nothing else: no cursor trail,
// no breathing, no color halo on the cards themselves.

// ONE wide aurora ribbon, rendered as TWO STATIC overlaid paths that
// only move via CSS `transform`.
//
// Why no SMIL path morphing here:
//   SMIL <animate> on the `d` attribute re-rasterizes the SVG every
//   frame, and the feGaussianBlur filter re-runs over the entire output
//   region on every update. All of that is main-thread / CPU work. When
//   the user scrolls, the scroll event competes for the main thread and
//   the animation visibly stalls — exactly the "滑动一下就卡一下" stutter.
//
// Fix: freeze the path geometry and the filter (browser rasterizes the
// blurred ribbon ONCE and caches the bitmap). Then animate only CSS
// `transform: translate3d(...)`, which runs on the GPU compositor
// thread and is completely isolated from main-thread / scroll work.
//
// To keep the ribbon feeling alive without path morphing, we stack TWO
// ribbons at slightly different shapes and translate them at different
// speeds. Their overlapping shift creates emergent shape variation.
function ensureAurora() {
  if (document.querySelector(".aurora-bg")) return;
  const wrap = document.createElement("div");
  wrap.className = "aurora-bg";
  wrap.setAttribute("aria-hidden", "true");

  // Silk-ribbon composition. Two ribbons (A = upper, B = lower) each
  // rendered as TWO overlaid paths of the same `d`:
  //    · halo layer: wide stroke, heavy blur, low opacity — the diffuse
  //      atmospheric glow of the silk
  //    · core layer: narrower stroke, lighter blur, higher opacity — the
  //      bright central body of the silk where light catches the fabric
  // That pairing is what sells the "silk" look: soft fuzzy edges bloom
  // outward, a tauter bright spine glides through the middle.
  //
  // Shapes are LONG GRACEFUL S-CURVES (only 2 lobes), not busy wiggles —
  // silk in wind moves in broad arcs, not high-frequency ripples.
  //
  // Motion is CSS-only (translate + tiny rotate on each layer-div), so
  // it runs entirely on the GPU compositor and is unaffected by scroll.
  wrap.innerHTML = `
    <div class="aurora-layer a">
      <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice"
           overflow="visible" aria-hidden="true">
        <defs>
          <linearGradient id="auroraBlueA" gradientUnits="userSpaceOnUse"
                          x1="0" y1="540" x2="1920" y2="540">
            <stop offset="0"    stop-color="rgba(178,212,240,0)"/>
            <stop offset="0.22" stop-color="rgba(178,212,240,0.14)"/>
            <stop offset="0.50" stop-color="rgba(190,220,246,0.22)"/>
            <stop offset="0.78" stop-color="rgba(178,212,240,0.13)"/>
            <stop offset="1"    stop-color="rgba(178,212,240,0)"/>
          </linearGradient>
          <filter id="auroraBlurHaloA"
                  filterUnits="userSpaceOnUse"
                  x="-1200" y="-1200" width="4320" height="3480">
            <feGaussianBlur stdDeviation="110"/>
          </filter>
          <filter id="auroraBlurCoreA"
                  filterUnits="userSpaceOnUse"
                  x="-1200" y="-1200" width="4320" height="3480">
            <feGaussianBlur stdDeviation="60"/>
          </filter>
        </defs>
        <!-- 3-lobe silk that CROSSES layer B at x≈200, 900, 1600. Starts
             high (y=200), plunges deep (y=780 via control), climbs back
             up (y=320), plunges again (y=720), ends middle (y=480).
             Path extends far past the viewBox so drift reveals fresh
             sections without exposing a stroke endpoint. -->
        <path filter="url(#auroraBlurHaloA)"
              stroke="url(#auroraBlueA)" stroke-width="440"
              stroke-linecap="round" vector-effect="non-scaling-stroke"
              fill="none" opacity="0.9"
              d="M -480 200 C 200 140, 520 840, 960 620 S 1480 200, 1760 420 S 2200 760, 2400 480"/>
        <path filter="url(#auroraBlurCoreA)"
              stroke="url(#auroraBlueA)" stroke-width="220"
              stroke-linecap="round" vector-effect="non-scaling-stroke"
              fill="none" opacity="0.75"
              d="M -480 200 C 200 140, 520 840, 960 620 S 1480 200, 1760 420 S 2200 760, 2400 480"/>
      </svg>
    </div>
    <div class="aurora-layer b">
      <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice"
           overflow="visible" aria-hidden="true">
        <defs>
          <linearGradient id="auroraBlueB" gradientUnits="userSpaceOnUse"
                          x1="0" y1="540" x2="1920" y2="540">
            <stop offset="0"    stop-color="rgba(176,210,238,0)"/>
            <stop offset="0.22" stop-color="rgba(176,210,238,0.11)"/>
            <stop offset="0.50" stop-color="rgba(188,218,244,0.18)"/>
            <stop offset="0.78" stop-color="rgba(176,210,238,0.10)"/>
            <stop offset="1"    stop-color="rgba(176,210,238,0)"/>
          </linearGradient>
          <filter id="auroraBlurHaloB"
                  filterUnits="userSpaceOnUse"
                  x="-1200" y="-1200" width="4320" height="3480">
            <feGaussianBlur stdDeviation="120"/>
          </filter>
          <filter id="auroraBlurCoreB"
                  filterUnits="userSpaceOnUse"
                  x="-1200" y="-1200" width="4320" height="3480">
            <feGaussianBlur stdDeviation="70"/>
          </filter>
        </defs>
        <!-- Phase-inverted 3-lobe silk: starts low (y=820), soars high
             (y=200 via control), dips to upper-mid (y=360), climbs
             again (y=260), ends low (y=640). Where A plunges, B rises
             — they cross at roughly x=200, 900, and 1600. -->
        <path filter="url(#auroraBlurHaloB)"
              stroke="url(#auroraBlueB)" stroke-width="480"
              stroke-linecap="round" vector-effect="non-scaling-stroke"
              fill="none" opacity="0.85"
              d="M -480 820 C 200 880, 520 200, 960 360 S 1480 820, 1760 620 S 2200 260, 2400 640"/>
        <path filter="url(#auroraBlurCoreB)"
              stroke="url(#auroraBlueB)" stroke-width="240"
              stroke-linecap="round" vector-effect="non-scaling-stroke"
              fill="none" opacity="0.65"
              d="M -480 820 C 200 880, 520 200, 960 360 S 1480 820, 1760 620 S 2200 260, 2400 640"/>
      </svg>
    </div>`;
  document.body.insertBefore(wrap, document.body.firstChild);
}
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", ensureAurora);
} else {
  ensureAurora();
}

// Per-module cursor tracking. Writes the cursor's position (as % of each
// card's box) into --mx / --my so the specular gloss on .module cards
// gently shifts its focal point with the mouse.
const wired = new WeakSet();
function wire(el) {
  if (wired.has(el)) return;
  wired.add(el);
  const move = (e) => {
    const r = el.getBoundingClientRect();
    const x = ((e.clientX - r.left) / r.width) * 100;
    const y = ((e.clientY - r.top) / r.height) * 100;
    el.style.setProperty("--mx", x + "%");
    el.style.setProperty("--my", y + "%");
  };
  const leave = () => {
    el.style.setProperty("--mx", "50%");
    el.style.setProperty("--my", "50%");
  };
  el.addEventListener("mousemove", move, { passive: true });
  el.addEventListener("mouseleave", leave, { passive: true });
}

function wireAll() {
  document.querySelectorAll(".module, .glow-target").forEach(wire);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", wireAll);
} else {
  wireAll();
}

// Wire up any modules mounted later (survey modal, report cards, …).
const mo = new MutationObserver(() => wireAll());
mo.observe(document.body, { childList: true, subtree: true });
