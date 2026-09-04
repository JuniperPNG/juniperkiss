/* Gentle progressive reveal for larger content groups. Content remains fully
   visible when JavaScript is unavailable or reduced motion is requested. */
(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reducedMotion.matches) return;

  var selector = [
    '.about__layout',
    '.section > .shell > h2',
    '.card',
    '.post-card',
    '.assignment',
    '.repo-feature__copy',
    '.repo-feature__logo-panel',
    '.entry',
    '.pub-list',
    '.plain-list',
    '.rich-text > h2',
    '.callout',
    '.site-footer__grid'
  ].join(',');

  /* Ignore alternate responsive layouts that are display:none at this width.
     Unmarked elements remain normally visible if the breakpoint later changes. */
  var elements = Array.prototype.slice.call(document.querySelectorAll(selector)).filter(function (element) {
    return element.getClientRects().length > 0;
  });
  if (!elements.length) return;

  var pending = new Set();
  elements.forEach(function (element, index) {
    element.setAttribute('data-scroll-reveal', '');
    var delay = 0;
    if (element.matches('.card, .post-card, .assignment, .repo-feature__copy, .repo-feature__logo-panel')) {
      var siblings = Array.prototype.slice.call(element.parentElement.children);
      delay = Math.min(siblings.indexOf(element) * 70, 210);
    }
    element.style.setProperty('--reveal-delay', delay + 'ms');

    /* Establish already-visible content in its final state before the CSS
       reveal state is enabled. This prevents the load -> hidden -> visible
       reversal that caused groups to flash and move twice. */
    var rect = element.getBoundingClientRect();
    var staggerVisibleGroup = element.matches(
      '.card-grid--skills .card, .repo-feature__copy, .repo-feature__logo-panel'
    ) && rect.top >= 0;
    if (rect.top < window.innerHeight && !staggerVisibleGroup) element.classList.add('is-revealed');
    else pending.add(element);
  });
  document.documentElement.classList.add('reveal-ready');

  /* Commit the initial states before transitions are armed. From this point
     onwards only the one-way hidden -> revealed change can transition. */
  document.documentElement.offsetWidth;
  document.documentElement.classList.add('reveal-armed');

  if (!pending.size) return;

  var observer = null;
  var ticking = false;

  function reveal(element) {
    if (element.classList.contains('is-revealed')) return;
    element.classList.add('is-revealed');
    pending.delete(element);
    if (observer) observer.unobserve(element);
    if (!pending.size) {
      window.removeEventListener('scroll', requestRevealCheck);
      window.removeEventListener('resize', requestRevealCheck);
    }
  }

  function revealVisible() {
    var triggerLine = window.innerHeight * 0.93;
    pending.forEach(function (element) {
      var rect = element.getBoundingClientRect();
      if (rect.top <= triggerLine && rect.bottom >= 0) reveal(element);
    });
    ticking = false;
  }

  function requestRevealCheck() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(revealVisible);
  }

  if ('IntersectionObserver' in window) {
    observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) reveal(entry.target);
      });
    }, {
      threshold: 0.08,
      rootMargin: '0px 0px -7% 0px'
    });

    pending.forEach(function (element) {
      observer.observe(element);
    });
  }

  /* Privacy-focused browsers can delay observer callbacks. This fallback uses
     the same trigger line and only ever adds the final state once. */
  window.addEventListener('scroll', requestRevealCheck, { passive: true });
  window.addEventListener('resize', requestRevealCheck);
  requestRevealCheck();
})();
