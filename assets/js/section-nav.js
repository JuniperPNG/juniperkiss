/* Shared page contents and scroll position, derived from the page's headings. */
(function () {
  'use strict';

  var nav = document.querySelector('[data-section-nav]');
  var main = document.getElementById('main');
  if (!nav || !main) return;

  var list = nav.querySelector('ul');
  var masthead = document.querySelector('.masthead');
  var breadcrumbs = document.querySelector('.breadcrumbs');
  var startAnchor = main.querySelector('[data-section-nav-start]');
  var desktop = window.matchMedia('(min-width: 1200px)');
  var targets = [main];
  var links = [list.querySelector('a')];
  var current = 0;
  var frame = 0;

  // Include prose subheadings, but not the many nested CV/card titles.
  main.querySelectorAll('h2, .prose h3').forEach(function (heading) {
    var label = heading.textContent.replace(/\s+/g, ' ').trim();
    if (!label || heading.closest('[hidden], dialog, [aria-hidden="true"]')) return;

    if (!heading.id) {
      var base = 'section-' + (label.toLowerCase().normalize('NFKD')
        .replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '') || 'heading');
      var id = base;
      var suffix = 2;
      while (document.getElementById(id)) id = base + '-' + suffix++;
      heading.id = id;
    }

    var item = document.createElement('li');
    var link = document.createElement('a');
    link.className = 'section-nav__link';
    link.href = '#' + encodeURIComponent(heading.id);
    link.textContent = label;
    if (heading.tagName === 'H3') item.className = 'section-nav__subsection';
    item.appendChild(link);
    list.appendChild(item);
    targets.push(heading);
    links.push(link);
  });

  function update() {
    frame = 0;
    if (!desktop.matches) return;

    // Home starts level with its hero panels; other pages start below breadcrumbs.
    // Both settle below the sticky masthead as the reader scrolls.
    var headerBottom = masthead ? masthead.getBoundingClientRect().bottom : 0;
    var breadcrumbBottom = breadcrumbs ? breadcrumbs.getBoundingClientRect().bottom : 0;
    var startTop = startAnchor ? startAnchor.getBoundingClientRect().top : breadcrumbBottom + 16;
    nav.style.setProperty('--section-nav-top', Math.max(headerBottom + 16, startTop) + 'px');

    var threshold = (masthead ? masthead.getBoundingClientRect().height : 0) + 32;
    var active = 0;
    targets.forEach(function (target, index) {
      if (target.getClientRects().length && target.getBoundingClientRect().top <= threshold) {
        active = index;
      }
    });
    // The last heading may not be able to reach the top on a short final section.
    if (window.scrollY > 0 && window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2) {
      active = targets.length - 1;
    }
    if (current === active) return;
    links[current].removeAttribute('aria-current');
    links[active].setAttribute('aria-current', 'location');
    current = active;

    // Keep long contents lists readable without moving the document or keyboard focus.
    if (!nav.contains(document.activeElement)) {
      var linkRect = links[active].getBoundingClientRect();
      var listRect = list.getBoundingClientRect();
      if (linkRect.top < listRect.top) list.scrollTop += linkRect.top - listRect.top - 8;
      else if (linkRect.bottom > listRect.bottom) list.scrollTop += linkRect.bottom - listRect.bottom + 8;
    }
  }

  function scheduleUpdate() {
    if (!frame) frame = window.requestAnimationFrame(update);
  }

  function measureHeader() {
    document.documentElement.style.setProperty('--masthead-h',
      Math.ceil(masthead ? masthead.getBoundingClientRect().height : 0) + 'px');
    scheduleUpdate();
  }

  window.addEventListener('scroll', scheduleUpdate, { passive: true });
  window.addEventListener('resize', measureHeader);
  window.addEventListener('hashchange', scheduleUpdate);
  window.addEventListener('pageshow', measureHeader);
  window.addEventListener('load', measureHeader);
  desktop.addEventListener('change', measureHeader);
  if ('ResizeObserver' in window) {
    var observer = new ResizeObserver(measureHeader);
    if (masthead) observer.observe(masthead);
    if (breadcrumbs) observer.observe(breadcrumbs);
    if (startAnchor) observer.observe(startAnchor);
    observer.observe(main);
  }
  measureHeader();

  // Native fragment links preserve history and keyboard navigation. Honour an
  // incoming fragment for headings whose IDs were added after HTML parsing.
  if (window.location.hash) {
    try {
      var initialTarget = document.getElementById(decodeURIComponent(window.location.hash.slice(1)));
      if (targets.indexOf(initialTarget) > 0) initialTarget.scrollIntoView({ behavior: 'instant' });
    } catch (error) { /* Ignore malformed fragment escapes. */ }
  }
}());
