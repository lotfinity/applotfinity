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
  // Editors can change the exact phrases in the Wagtail Projects page settings.
  // Django's json_script filter encodes this safely; nothing is rendered as HTML.
  const config = document.getElementById('gallery-glitch-messages');
  let rawMessages = '';
  try { rawMessages = JSON.parse(config?.textContent || '""'); } catch { /* Empty field. */ }
  const messages = String(rawMessages).split(/\r?\n/)
    .map(s => s.toUpperCase().replace(/[^A-Z0-9 .,+\-/?!&]/g, '').replace(/\s+/g, ' ').trim().slice(0, 58))
    .filter(Boolean).slice(0, 8);
  const stats = {
    frames: 0, glitches: 0, letters: 0, reduced: reduce(), running: false,
    phrases: messages.length, activeMessage: null, messagesShown: 0,
  };
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
  let messageIndex = 0;
  let transmission = null;
  let nextTransmission = performance.now() + 1350;
  const decodeMs = 1200;
  const holdMs = 2850;
  const fadeMs = 1150;
  const totalMs = decodeMs + holdMs + fadeMs;


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
    transmission = null;
    nextTransmission = performance.now() + 1350;
  }

  function phraseLines(text) {
    const maxLen = Math.max(7, Math.min(columns - 4, mobile ? 16 : 22));
    const words = text.split(' ');
    const lines = [];
    let line = '';
    for (const word of words) {
      if (line && (line + ' ' + word).length > maxLen) {
        lines.push(line);
        line = '';
      }
      if (word.length > maxLen) {
        if (line) { lines.push(line); line = ''; }
        for (let i = 0; i < word.length; i += maxLen) lines.push(word.slice(i, i + maxLen));
      } else {
        line = line ? `${line} ${word}` : word;
      }
    }
    if (line) lines.push(line);
    return lines.slice(0, mobile ? 3 : 2);
  }

  function revealMessage(time, fixed = false) {
    if (!messages.length) return;
    const text = messages[messageIndex % messages.length];
    messageIndex++;
    const lines = phraseLines(text);
    // Right-hand open space on desktop; mobile messages remain centered.
    const row = mobile
      ? Math.max(2, Math.min(rows - lines.length - 2, Math.floor(rows * .74)))
      : Math.max(2, Math.min(rows - lines.length - 2, Math.floor(rows * .21)));
    const cells = new Map();
    for (let r = 0; r < lines.length; r++) {
      const line = lines[r];
      const origin = mobile
        ? Math.max(1, Math.floor((columns - line.length) / 2))
        : Math.max(1, Math.min(columns - line.length - 2, Math.floor(columns * .61)));
      for (let i = 0; i < line.length; i++) {
        const index = (row + r) * columns + origin + i;
        if (index < 0 || index >= letters.length) continue;
        cells.set(index, { glyph: line[i], delay: (r * 130) + (i * 57) });
      }
    }
    transmission = { text, cells, started: fixed ? time - decodeMs - 100 : time, fixed };
    stats.activeMessage = text;
    stats.messagePosition = { row, lines, columns };
    stats.messagesShown++;
  }

  function updateTransmission(now) {
    if (!messages.length) return;
    if (reduce()) {
      if (!transmission) revealMessage(now, true);
      else {
        transmission.fixed = true;
        transmission.started = now - decodeMs - 100;
      }
      return;
    }
    if (transmission && now - transmission.started >= totalMs) {
      // Send the revealed text back into the regular matrix.
      for (const index of transmission.cells.keys()) {
        letters[index].glyph = char();
        letters[index].flash = 1;
      }
      transmission = null;
      stats.activeMessage = null;
      stats.messagePosition = null;
      nextTransmission = now + 1550;
    }
    if (!transmission && now >= nextTransmission) revealMessage(now);
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
    updateTransmission(time);
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
    const age = transmission ? performance.now() - transmission.started : 0;
    const fading = !transmission || transmission.fixed ? 1
      : Math.min(1, Math.max(0, (totalMs - age) / fadeMs));
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
      const fixed = transmission?.cells.get(index);
      if (fixed && (transmission.fixed || age >= fixed.delay)) {
        const decoded = transmission.fixed || age > decodeMs + fixed.delay
          || Math.random() > 1 - Math.max(0, (age - fixed.delay) / decodeMs);
        ctx.fillStyle = '#eefff5';
        ctx.globalAlpha = Math.min(1, (.60 + .40 * fading) * fading);
        ctx.shadowColor = '#65ffbf';
        ctx.shadowBlur = mobile ? 16 : 17;
        ctx.fillText(decoded ? fixed.glyph : letter.glyph, x, y);
        if (decoded) {
          ctx.lineWidth = .45;
          ctx.strokeStyle = '#b8fff0';
          ctx.strokeText(fixed.glyph, x, y);
        }
        ctx.shadowBlur = 0;
      } else {
        ctx.fillText(letter.glyph, x, y);
      }
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
    updateTransmission(now);
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
    updateTransmission(performance.now());
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
