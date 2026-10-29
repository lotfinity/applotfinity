/* Lotfinity: lightweight ambient animations for the six numbered project cards.
 * CSS runs effects; IntersectionObserver pauses offscreen cards; pointer events
 * update a small hover transform with no perpetual JS animation loop.
 */
(() => {
  'use strict';
  const cards = [...document.querySelectorAll('.gallery-page [data-project-card]')];
  if (!cards.length) return;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const pointer = matchMedia('(hover: hover) and (pointer: fine)');
  const saveData = Boolean(navigator.connection?.saveData);
  const body = document.body;
  let visible = 0;
  const stats = { count: cards.length, nearby: 0, pointerUpdates: 0, still: false };
  window.__lotfinityGalleryCards = stats;

  function setStill() {
    const still = motion.matches || saveData || document.hidden;
    body.classList.toggle('gallery-cards--still', still);
    stats.still = still;
  }
  setStill();
  const observer = 'IntersectionObserver' in window ? new IntersectionObserver(entries => {
    for (const entry of entries) {
      entry.target.classList.toggle('is-near', entry.isIntersecting);
    }
    visible = cards.filter(card => card.classList.contains('is-near')).length;
    stats.nearby = visible;
  }, { rootMargin: '140px 0px', threshold: 0 }) : null;

  for (const card of cards) {
    if (observer) observer.observe(card);
    else card.classList.add('is-near');
    let scheduled = 0;
    let lastX = 0;
    let lastY = 0;
    function paint() {
      scheduled = 0;
      if (!pointer.matches || stats.still) return;
      const rect = card.getBoundingClientRect();
      const px = Math.max(0, Math.min(1, (lastX - rect.left) / rect.width));
      const py = Math.max(0, Math.min(1, (lastY - rect.top) / rect.height));
      card.style.setProperty('--card-pointer-x', `${(px * 100).toFixed(1)}%`);
      card.style.setProperty('--card-pointer-y', `${(py * 100).toFixed(1)}%`);
      card.style.setProperty('--card-tilt-x', `${((.5 - py) * 4).toFixed(2)}deg`);
      card.style.setProperty('--card-tilt-y', `${((px - .5) * 5).toFixed(2)}deg`);
      stats.pointerUpdates++;
    }
    card.addEventListener('pointerenter', () => {
      if (pointer.matches && !stats.still) card.classList.add('is-hovered');
    }, { passive: true });
    card.addEventListener('pointermove', e => {
      if (!pointer.matches || stats.still) return;
      lastX = e.clientX;
      lastY = e.clientY;
      if (!scheduled) scheduled = requestAnimationFrame(paint);
    }, { passive: true });
    card.addEventListener('pointerleave', () => {
      if (scheduled) cancelAnimationFrame(scheduled);
      scheduled = 0;
      card.classList.remove('is-hovered');
      card.style.removeProperty('--card-tilt-x');
      card.style.removeProperty('--card-tilt-y');
      card.style.removeProperty('--card-pointer-x');
      card.style.removeProperty('--card-pointer-y');
    }, { passive: true });
  }
  if (!observer) stats.nearby = cards.length;
  document.addEventListener('visibilitychange', () => {
    setStill();
    if (stats.still) cards.forEach(card => card.classList.remove('is-hovered'));
  });
  const onMotionChange = () => {
    setStill();
    if (stats.still) cards.forEach(card => card.classList.remove('is-hovered'));
  };
  if (motion.addEventListener) motion.addEventListener('change', onMotionChange);
  else if (motion.addListener) motion.addListener(onMotionChange);
})();
