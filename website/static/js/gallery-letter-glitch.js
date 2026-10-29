/* Lotfinity / numbered portfolio — Letter Glitch background.
 * A framework-free Canvas2D adaptation of the React Bits Letter Glitch visual
 * (https://reactbits.dev/c/backgrounds/letter-glitch) for Django/Wagtail.
 * No React runtime, WebGL, third-party CDN or continuously running 60 FPS loop.
 * Inspired by React Bits by David Haz. Source: https://github.com/DavidHDev/react-bits
 * License reference: MIT + Commons Clause. This file is an independent implementation.
 */
(() => {
  'use strict';

  const host = document.querySelector('[data-letter-glitch]');
  if (!host) return;
  const canvas = host.querySelector('canvas');
  const ctx = canvas?.getContext('2d', { alpha: true });
  if (!ctx) return;

  const media = window.matchMedia('(prefers-reduced-motion: reduce)');
  const saveData = Boolean(navigator.connection?.saveData);
  const reduce = () => media.matches || saveData;
  const colors = ['#2b4539', '#61dca3', '#61b3dc', '#8addf3'];
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*+-=[]{}<>/';
  const stats = { frames: 0, glitches: 0, letters: 0, reduced: reduce(), running: false };
  window.__lotfinityLetterGlitch = stats;

  let width = 0;
  let height = 0;
  let columns = 0;
  let rows = 0;
  let cellW = 18;
  let cellH = 25;
  let mobile = false;
  let letters = [];
  let frameTimer = 0;
  let resizeTimer = 0;
  let lastInput = 0;
  let lastChange = 0;
  let cursor = null;
  let burst = null;
  let running = false;
  let randomSeed = 0x91d3a6b;

  const rand = () => {
    randomSeed ^= randomSeed << 13;
    randomSeed ^= randomSeed >>> 17;
    randomSeed ^= randomSeed << 5;
    return (randomSeed >>> 0) / 4294967296;
  };
  const char = () => chars[Math.floor(rand() * chars.length)];
  const randomColor = () => colors[Math.floor(rand() * colors.length)];

  function setup() {
    width = Math.max(1, innerWidth);
    height = Math.max(1, innerHeight);
    mobile = width < 700;
    // At 4K/ultrawide sizes, scale spacing rather than drawing 15–25k glyphs.
    // Approximate maximum: 3,200 desktop / 800 mobile letters.
    const baseW = mobile ? 20 : 18;
    const baseH = mobile ? 29 : 25;
    const maxCells = mobile ? 800 : 3200;
    const scale = Math.max(1, Math.sqrt((width * height) / (baseW * baseH * maxCells)));
    cellW = baseW * scale;
    cellH = baseH * scale;
    columns = Math.ceil(width / cellW);
    rows = Math.ceil(height / cellH);
    // The raster is capped because text is positioned in CSS pixels, not
    // because we need device-native 3x/4x resolution for a background.
    const maxPixels = mobile ? 400000 : 1250000;
    const dpr = Math.min(devicePixelRatio || 1, mobile ? 1 : 1.1, Math.sqrt(maxPixels / (width * height)));
    canvas.width = Math.max(1, Math.round(width * dpr));
    canvas.height = Math.max(1, Math.round(height * dpr));
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.textBaseline = 'middle';
    ctx.textAlign = 'center';
    ctx.font = `${Math.min(24, Math.round((mobile ? 13 : 14) * Math.sqrt(scale)))}px ui-monospace, SFMono-Regular, Consolas, Liberation Mono, monospace`;
    randomSeed = (0x91d3a6b ^ (width * 97) ^ (height * 71)) >>> 0;
    letters = Array.from({ length: columns * rows }, () => ({
      glyph: char(),
      color: randomColor(),
      strength: .22 + rand() * .3,
      flash: 0,
    }));
    stats.letters = letters.length;
    stats.size = [canvas.width, canvas.height];
    cursor = null;
    burst = null;
    lastChange = 0;
  }

  function scramble(time) {
    if (reduce()) return;
    if (time - lastChange < 55) return;
    lastChange = time;
    // React Bits characteristic: random letters scramble with intermittent
    // bursts of color. Alter only a small fraction of cells each update.
    const count = Math.min(45, Math.max(8, Math.round(letters.length * (mobile ? .009 : .008))));
    for (let i = 0; i < count; i++) {
      const index = Math.floor(rand() * letters.length);
      const letter = letters[index];
      letter.glyph = char();
      letter.color = randomColor();
      letter.flash = 1;
      stats.glitches++;
    }
    // Proximity interaction, attenuated and bounded to avoid large redraw cost.
    if (cursor && time - lastInput < 900 && rand() < .7) {
      const col = Math.round(cursor.x / cellW);
      const row = Math.round(cursor.y / cellH);
      for (let i = 0; i < 9; i++) {
        const c = col + Math.floor(rand() * 11) - 5;
        const r = row + Math.floor(rand() * 7) - 3;
        if (c < 0 || c >= columns || r < 0 || r >= rows) continue;
        const letter = letters[r * columns + c];
        letter.glyph = char();
        letter.color = '#9bfce1';
        letter.flash = 1.25;
      }
    }
    // A short burst of scrambling near click position; never captures clicks.
    if (burst && time - burst.at < 470) {
      const row = Math.floor(burst.y / cellH);
      const start = Math.max(0, row - 2);
      const end = Math.min(rows - 1, row + 2);
      for (let r = start; r <= end; r++) {
        const c = Math.floor(rand() * columns);
        const letter = letters[r * columns + c];
        letter.glyph = char();
        letter.color = '#c0fff0';
        letter.flash = 1.45;
      }
    }
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);
    // A single fillText per glyph, with a restrained dark teal base palette.
    // Bright flashes are short-lived and never obscure interactive controls.
    for (let index = 0; index < letters.length; index++) {
      const letter = letters[index];
      const x = (index % columns + .5) * cellW;
      const y = (Math.floor(index / columns) + .5) * cellH;
      if (letter.flash > .02) {
        ctx.globalAlpha = Math.min(.94, .37 + letter.flash * .38);
        letter.flash *= .72;
      } else {
        letter.flash = 0;
        ctx.globalAlpha = letter.strength;
      }
      ctx.fillStyle = letter.color;
      ctx.fillText(letter.glyph, x, y);
    }
    ctx.globalAlpha = 1;
    stats.frames++;
  }

  function stop() {
    running = false;
    stats.running = false;
    clearTimeout(frameTimer);
    frameTimer = 0;
  }

  function tick() {
    if (!running || document.hidden) return;
    const now = performance.now();
    scramble(now);
    draw();
    schedule();
  }

  function schedule() {
    if (!running || document.hidden || reduce()) return;
    const active = performance.now() - lastInput < 3500;
    const fps = active ? (mobile ? 15 : 24) : (mobile ? 6 : 10);
    frameTimer = setTimeout(tick, 1000 / fps);
  }

  function start() {
    if (document.hidden) return;
    stop();
    running = true;
    stats.running = true;
    stats.reduced = reduce();
    scramble(performance.now());
    draw();
    if (reduce()) { stop(); return; }
    schedule();
  }

  function resize() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => { setup(); start(); }, 160);
  }

  window.addEventListener('resize', resize, { passive: true });
  window.addEventListener('pointermove', (event) => {
    cursor = { x: event.clientX, y: event.clientY };
    lastInput = performance.now();
  }, { passive: true });
  window.addEventListener('pointerdown', (event) => {
    if (reduce()) return;
    burst = { x: event.clientX, y: event.clientY, at: performance.now() };
    lastInput = burst.at;
  }, { passive: true });
  window.addEventListener('scroll', () => { lastInput = performance.now(); }, { passive: true });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stop();
    else start();
  });
  const onMotion = () => { stats.reduced = reduce(); start(); };
  if (media.addEventListener) media.addEventListener('change', onMotion);
  else if (media.addListener) media.addListener(onMotion);

  setup();
  start();
})();
