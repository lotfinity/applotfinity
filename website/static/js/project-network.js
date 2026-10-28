/* Lotfinity ambient project network.
 * Dependency-free Canvas 2D: no Three.js bundle, no WebGL, no asset downloads.
 * Precomputed topology, tiny frame buffer, capped timers, hidden-tab shutdown.
 */
(() => {
  'use strict';

  const host = document.querySelector('[data-project-network]');
  if (!host) return;
  const canvas = host.querySelector('canvas');
  const ctx = canvas && canvas.getContext('2d', { alpha: true });
  if (!ctx) return; // The layered CSS atmosphere remains a complete fallback.

  const motionSetting = window.matchMedia('(prefers-reduced-motion: reduce)');
  const saveData = Boolean(navigator.connection && navigator.connection.saveData);
  const reduced = () => motionSetting.matches || saveData;
  const stats = { draws: 0, pulses: 0, nodes: 0, edges: 0, reduced: reduced() };
  // Exposed for browser performance checks; not part of the content UI.
  window.__lotfinityProjectNetwork = stats;

  let w = 0;
  let h = 0;
  let mobile = false;
  let nodes = [];
  let links = [];
  let frameTimer = 0;
  let resizeTimer = 0;
  let lastActivity = performance.now();
  let nextPulse = lastActivity + 1600;
  let pulse = null;
  let running = false;
  let seed = 0x5a81da5;

  function random() {
    seed ^= seed << 13;
    seed ^= seed >>> 17;
    seed ^= seed << 5;
    return (seed >>> 0) / 4294967296;
  }

  function rebuild() {
    w = Math.max(1, window.innerWidth);
    h = Math.max(1, window.innerHeight);
    mobile = w < 700;
    // Bound real pixel cost on ultrawide/4K screens as well as high-DPI phones.
    const pixelBudget = mobile ? 430000 : 1600000;
    const dpr = Math.min(
      window.devicePixelRatio || 1,
      mobile ? 1 : 1.15,
      Math.sqrt(pixelBudget / (w * h)),
    );
    canvas.width = Math.max(1, Math.round(w * dpr));
    canvas.height = Math.max(1, Math.round(h * dpr));
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    seed = (0x5a81da5 ^ (w * 41) ^ (h * 83)) >>> 0;

    nodes = [];
    links = [];
    const count = mobile ? 23 : Math.min(55, Math.max(38, Math.round(w / 29)));
    for (let i = 0; i < count; i++) {
      // Keep the brightest network to the right of the project headline.
      const x = (random() < 0.76 ? 0.30 + 0.7 * random() : random()) * w;
      const y = (0.05 + random() * 0.90) * h;
      nodes.push({
        x, y,
        phase: random() * Math.PI * 2,
        speed: 0.17 + random() * 0.25,
        radius: random() < 0.16 ? 2.2 : 1 + random() * 0.45,
        orbit: 2.2 + random() * 4,
        anchor: random() < 0.14,
      });
    }

    const maxDistance = mobile ? 170 : 225;
    const used = new Set();
    for (let i = 0; i < nodes.length; i++) {
      const nearby = [];
      for (let j = 0; j < nodes.length; j++) {
        if (i === j) continue;
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const distance = Math.hypot(dx, dy);
        if (distance < maxDistance && distance > 25) nearby.push({ j, distance });
      }
      nearby.sort((a, b) => a.distance - b.distance);
      for (const candidate of nearby.slice(0, mobile ? 2 : 3)) {
        const a = Math.min(i, candidate.j);
        const b = Math.max(i, candidate.j);
        const key = `${a}-${b}`;
        if (used.has(key)) continue;
        used.add(key);
        links.push({
          a, b,
          brightness: 0.09 + random() * 0.115,
          phase: random() * Math.PI * 2,
        });
      }
    }
    // Bound the cost regardless of viewport size or edge density.
    links = links.slice(0, mobile ? 41 : 90);
    stats.nodes = nodes.length;
    stats.edges = links.length;
    stats.resolution = [canvas.width, canvas.height];
    pulse = null;
  }

  function coordinates(t) {
    return nodes.map((n) => {
      const phase = n.phase + t * n.speed;
      return {
        x: n.x + Math.sin(phase) * n.orbit,
        y: n.y + Math.cos(phase * 0.8) * n.orbit,
      };
    });
  }

  function electricArc(from, to, age) {
    const dx = to.x - from.x;
    const dy = to.y - from.y;
    const length = Math.hypot(dx, dy);
    if (length < 5) return;
    const nx = -dy / length;
    const ny = dx / length;
    const opacity = Math.max(0, 1 - age / 620);
    const stepCount = 9;

    ctx.save();
    ctx.lineWidth = 1.35;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = `rgba(141, 240, 255, ${0.76 * opacity})`;
    ctx.shadowColor = '#60dbff';
    ctx.shadowBlur = mobile ? 8 : 13;
    ctx.beginPath();
    ctx.moveTo(from.x, from.y);
    for (let step = 1; step < stepCount; step++) {
      const ratio = step / stepCount;
      const jitter = Math.sin(step * 19.2 + age * 0.031) * 5.7 * Math.sin(Math.PI * ratio);
      ctx.lineTo(from.x + dx * ratio + nx * jitter, from.y + dy * ratio + ny * jitter);
    }
    ctx.lineTo(to.x, to.y);
    ctx.stroke();
    ctx.shadowBlur = 0;
    ctx.lineWidth = .55;
    ctx.strokeStyle = `rgba(245, 252, 255, ${0.78 * opacity})`;
    ctx.stroke();
    ctx.restore();
  }

  function draw(now) {
    const t = now / 1000;
    const dots = coordinates(t);
    ctx.clearRect(0, 0, w, h);

    // Thin, barely luminous connections, behind the project content.
    for (const link of links) {
      const from = dots[link.a];
      const to = dots[link.b];
      const breathing = reduced() ? 1 : 0.81 + 0.19 * Math.sin(t * 0.7 + link.phase);
      const dim = mobile ? 0.73 : 1;
      ctx.beginPath();
      ctx.moveTo(from.x, from.y);
      ctx.lineTo(to.x, to.y);
      ctx.strokeStyle = `rgba(92, 179, 207, ${link.brightness * breathing * dim})`;
      ctx.lineWidth = .8;
      ctx.stroke();
    }

    // Small circuit junctions with occasional brighter anchors.
    for (let i = 0; i < dots.length; i++) {
      const p = dots[i];
      const n = nodes[i];
      if (n.anchor) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, n.radius * 3.8, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(94, 190, 216, .115)';
        ctx.lineWidth = .8;
        ctx.stroke();
      }
      ctx.beginPath();
      ctx.arc(p.x, p.y, n.radius, 0, Math.PI * 2);
      ctx.fillStyle = n.anchor ? 'rgba(135, 225, 241, .73)' : 'rgba(116, 195, 220, .49)';
      ctx.fill();
    }

    // A short, rare electric pulse gives the background personality without a
    // costly shader bloom or a continuously animating particle field.
    if (!reduced() && now >= nextPulse && links.length) {
      pulse = { index: Math.floor(random() * links.length), started: now };
      nextPulse = now + 3000 + random() * 3000;
      stats.pulses++;
    }
    if (pulse) {
      const age = now - pulse.started;
      if (age < 620) {
        const link = links[pulse.index];
        electricArc(dots[link.a], dots[link.b], age);
      } else {
        pulse = null;
      }
    }
    stats.draws++;
  }

  function schedule() {
    if (!running || document.hidden || reduced()) return;
    const active = performance.now() - lastActivity < 4000;
    // In background browsing, animate at 7 FPS, not a permanent 60 FPS loop.
    // During user activity the motion is a smoother 18-24 FPS.
    const interval = active ? (mobile ? 1000 / 18 : 1000 / 24) : 1000 / 7;
    frameTimer = window.setTimeout(tick, interval);
  }

  function tick() {
    if (!running || document.hidden) return;
    draw(performance.now());
    schedule();
  }

  function stop() {
    running = false;
    window.clearTimeout(frameTimer);
    frameTimer = 0;
  }

  function start() {
    if (document.hidden) return;
    stop();
    running = true;
    draw(performance.now());
    schedule();
  }

  function activity() {
    lastActivity = performance.now();
  }

  function resized() {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(() => {
      rebuild();
      start();
    }, 150);
  }

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stop();
    else start();
  });
  window.addEventListener('resize', resized, { passive: true });
  window.addEventListener('pointerdown', activity, { passive: true });
  window.addEventListener('pointermove', activity, { passive: true });
  window.addEventListener('scroll', activity, { passive: true });
  const motionChanged = () => {
    stats.reduced = reduced();
    nextPulse = performance.now() + 2000;
    start();
  };
  if (motionSetting.addEventListener) motionSetting.addEventListener('change', motionChanged);
  else if (motionSetting.addListener) motionSetting.addListener(motionChanged);

  rebuild();
  start();
})();
