/* Gentle progressive reveal for larger content groups. Content remains fully
   visible when JavaScript is unavailable or reduced motion is requested. */
(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reducedMotion.matches || !('IntersectionObserver' in window)) return;

  var selector = [
    '.hero__copy-panel',
    '.photo-carousel',
    '.about__layout',
    '.cv-header',
    '.section > .shell > h2',
    '.card',
    '.post-card',
    '.assignment',
    '.entry',
    '.pub-list',
    '.plain-list',
    '.post-header',
    '.post-hero',
    '.rich-text > h2',
    '.callout',
    '.site-footer__grid'
  ].join(',');

  var elements = Array.prototype.slice.call(document.querySelectorAll(selector));
  if (!elements.length) return;

  elements.forEach(function (element, index) {
    element.setAttribute('data-scroll-reveal', '');
    var delay = 0;
    if (element.matches('.card, .post-card, .assignment')) {
      var siblings = Array.prototype.slice.call(element.parentElement.children);
      delay = Math.min(siblings.indexOf(element) * 70, 210);
    }
    element.style.setProperty('--reveal-delay', delay + 'ms');
  });
  document.documentElement.classList.add('reveal-ready');

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-revealed');
      observer.unobserve(entry.target);
    });
  }, {
    threshold: 0.08,
    rootMargin: '0px 0px -7% 0px'
  });

  elements.forEach(function (element) {
    observer.observe(element);
  });
})();
