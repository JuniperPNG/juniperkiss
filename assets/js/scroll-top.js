/* Progressive return-to-top control shared by every page. */
(function () {
  'use strict';

  var button = document.querySelector('[data-scroll-top]');
  if (!button) return;

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var showAfter = Math.max(500, Math.round(window.innerHeight * 0.75));
  var ticking = false;

  function updateVisibility() {
    var visible = window.scrollY > showAfter;
    if (visible) {
      button.hidden = false;
      window.requestAnimationFrame(function () {
        button.classList.add('is-visible');
      });
    } else {
      button.classList.remove('is-visible');
      button.hidden = true;
    }
    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(updateVisibility);
  }, { passive: true });

  window.addEventListener('resize', function () {
    showAfter = Math.max(500, Math.round(window.innerHeight * 0.75));
    updateVisibility();
  });

  button.addEventListener('click', function () {
    window.scrollTo({
      top: 0,
      behavior: reducedMotion.matches ? 'auto' : 'smooth'
    });
  });

  updateVisibility();
}());
