/* Single-line black sound wave inspired by Her / the original Siri wave.
 *
 * Amplitude drives the vertical envelope. Two sources can feed it:
 *   - `attachMic()` — real RMS from AnalyserNode on getUserMedia.
 *   - `pulseOnWord()` — hand-driven for SpeechSynthesis "onboundary" events,
 *     since the synth's audio is not exposed to an AnalyserNode.
 *
 * Both converge on a single `targetAmp` scalar (0..1) that smoothly lerps
 * toward whatever the active source is asking for, giving us one uniform
 * animation regardless of who is talking. */

const TWO_PI = Math.PI * 2;

export class Wave {
  constructor(canvas, { color = "#1d1d1f" } = {}) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.color = color;

    this.targetAmp = 0;
    this.amp = 0;
    this.phase = 0;
    this.running = false;

    this._audioCtx = null;
    this._analyser = null;
    this._micBuf = null;
    this._micStream = null;
    this._decayTimer = null;

    this._resize = this._resize.bind(this);
    window.addEventListener("resize", this._resize);
    this._resize();
  }

  _resize() {
    const dpr = Math.max(1, window.devicePixelRatio || 1);
    const rect = this.canvas.getBoundingClientRect();
    this.canvas.width = Math.floor(rect.width * dpr);
    this.canvas.height = Math.floor(rect.height * dpr);
    this.ctx.scale(dpr, dpr);
    this.w = rect.width;
    this.h = rect.height;
  }

  start() {
    if (this.running) return;
    this.running = true;
    const frame = () => {
      if (!this.running) return;
      this._tick();
      requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  }

  stop() {
    this.running = false;
    if (this._micStream) {
      this._micStream.getTracks().forEach((t) => t.stop());
      this._micStream = null;
    }
    if (this._audioCtx) {
      this._audioCtx.close().catch(() => {});
      this._audioCtx = null;
    }
  }

  _tick() {
    // 1. Sample amplitude from mic if attached.
    if (this._analyser) {
      this._analyser.getByteTimeDomainData(this._micBuf);
      let sum = 0;
      for (let i = 0; i < this._micBuf.length; i += 1) {
        const v = (this._micBuf[i] - 128) / 128;
        sum += v * v;
      }
      const rms = Math.sqrt(sum / this._micBuf.length);
      const mapped = Math.min(1, rms * 3.5);
      // Only update from mic if mic is the louder source at the moment.
      this.targetAmp = Math.max(this.targetAmp * 0.9, mapped);
    }

    // 2. Smooth current amp toward target.
    this.amp += (this.targetAmp - this.amp) * 0.15;
    // Add a tiny background shimmer so a perfectly silent line still lives.
    const idle = 0.05 + 0.02 * Math.sin(this.phase * 0.15);
    const a = Math.max(idle, this.amp);

    // 3. Draw the line.
    const ctx = this.ctx;
    const w = this.w, h = this.h;
    ctx.clearRect(0, 0, w, h);
    ctx.shadowColor = "rgba(0, 113, 227, 0.45)";
    ctx.shadowBlur = 10 + a * 22;
    ctx.strokeStyle = this.color;
    ctx.lineWidth = 1.5;
    ctx.lineCap = "round";
    ctx.beginPath();
    const mid = h / 2;
    const cycles = 4 + a * 2.5;
    const envelopeX = (x) => {
      // Bell-shaped envelope — taller in the middle, fades at edges.
      const u = (x / w) * 2 - 1;
      return Math.exp(-u * u * 1.4);
    };
    for (let x = 0; x <= w; x += 1.6) {
      const env = envelopeX(x);
      const phi = this.phase + (x / w) * TWO_PI * cycles;
      const y = mid
        + Math.sin(phi) * env * a * (mid - 8)
        + Math.sin(phi * 0.33 + this.phase * 0.7) * env * a * 4;
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    this.phase += 0.035 + a * 0.08;

    // 4. Exponential amp decay when nothing is actively pushing it up.
    this.targetAmp *= 0.94;
  }

  async attachMic() {
    if (this._analyser) return;
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const AC = window.AudioContext || window.webkitAudioContext;
      const ctx = new AC();
      const source = ctx.createMediaStreamSource(stream);
      const analyser = ctx.createAnalyser();
      analyser.fftSize = 512;
      source.connect(analyser);
      this._audioCtx = ctx;
      this._analyser = analyser;
      this._micStream = stream;
      this._micBuf = new Uint8Array(analyser.fftSize);
    } catch (e) {
      // Mic permission denied — keep the wave alive via word pulses alone.
      // eslint-disable-next-line no-console
      console.info("mic unavailable:", e && e.message);
    }
  }

  pulseOnWord(strength = 0.7) {
    // Called from SpeechSynthesisUtterance.onboundary per word: snap up,
    // decay naturally in _tick.
    this.targetAmp = Math.min(1, Math.max(this.targetAmp, strength));
  }

  hold(strength = 0.4) {
    this.targetAmp = Math.max(this.targetAmp, strength);
  }
}
