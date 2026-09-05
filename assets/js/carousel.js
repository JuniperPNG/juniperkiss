/* Hero photo carousel controls and gentle autoplay. The track still scrolls
   natively without this script; autoplay pauses for interaction, visibility
   changes and reduced-motion preferences. */
(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var initialAutoplayDelay = 1000;
  var autoplayDelay = 2500;
  var interactionDelay = 1800;
  var fadeDuration = 280;

  document.querySelectorAll('.photo-carousel').forEach(function (carousel) {
    var track = carousel.querySelector('.photo-carousel__track');
    var prev = carousel.querySelector('[data-carousel-prev]');
    var next = carousel.querySelector('[data-carousel-next]');
    if (!track || !prev || !next) return;

    var items = Array.prototype.slice.call(track.querySelectorAll('.photo-carousel__item'));
    if (!items.length) return;

    // Photos vary in width (no cropping), so "one click = one photo" needs
    // to target the actual next/previous element, not a fixed pixel offset.
    function nearestIndex() {
      var trackLeft = track.getBoundingClientRect().left;
      var closest = 0;
      var closestDist = Infinity;
      items.forEach(function (item, i) {
        var dist = Math.abs(item.getBoundingClientRect().left - trackLeft);
        if (dist < closestDist) {
          closestDist = dist;
          closest = i;
        }
      });
      return closest;
    }

    function go(direction, wrap) {
      var target = nearestIndex() + direction;
      var atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 2;

      if (wrap && direction > 0 && atEnd) {
        target = 0;
      } else if (wrap && direction < 0 && target < 0) {
        target = items.length - 1;
      } else {
        target = Math.max(0, Math.min(items.length - 1, target));
      }

      // Move only the photo track: scrollIntoView also moves page ancestors
      // and can pull the reader back towards the hero during autoplay.
      track.scrollTo({
        left: track.scrollLeft + items[target].getBoundingClientRect().left - track.getBoundingClientRect().left,
        behavior: reducedMotion.matches ? 'auto' : 'smooth'
      });
      carousel.setAttribute('data-active-index', String(target));
    }

    var autoplayTimer = 0;
    var fadeOutTimer = 0;
    var fadeInTimer = 0;
    var hasAutoplayStarted = false;
    var isPointerDown = false;
    var isHovered = false;
    var hasFocus = carousel.contains(document.activeElement);
    var isVisible = true;

    function clearTimers() {
      window.clearTimeout(autoplayTimer);
      window.clearTimeout(fadeOutTimer);
      window.clearTimeout(fadeInTimer);
      carousel.classList.remove('is-auto-fading');
    }

    function canAutoplay() {
      return !reducedMotion.matches && !isPointerDown && !isHovered && !hasFocus && isVisible && !document.hidden;
    }

    function scheduleAutoplay(requestedDelay) {
      window.clearTimeout(autoplayTimer);
      if (!canAutoplay()) return;
      var delay = typeof requestedDelay === 'number'
        ? requestedDelay
        : (hasAutoplayStarted ? autoplayDelay : initialAutoplayDelay);
      autoplayTimer = window.setTimeout(function () {
        if (!canAutoplay()) return;
        hasAutoplayStarted = true;
        carousel.classList.add('is-auto-fading');
        fadeOutTimer = window.setTimeout(function () {
          if (canAutoplay()) go(1, true);
        }, fadeDuration / 2);
        fadeInTimer = window.setTimeout(function () {
          carousel.classList.remove('is-auto-fading');
          scheduleAutoplay();
        }, fadeDuration);
      }, delay);
    }

    function pauseAutoplay() {
      clearTimers();
    }

    prev.addEventListener('click', function () {
      go(-1);
      hasAutoplayStarted = true;
      scheduleAutoplay(interactionDelay);
    });

    next.addEventListener('click', function () {
      go(1);
      hasAutoplayStarted = true;
      scheduleAutoplay(interactionDelay);
    });

    carousel.addEventListener('focusin', function () {
      hasFocus = true;
      pauseAutoplay();
    });

    carousel.addEventListener('focusout', function (event) {
      hasFocus = carousel.contains(event.relatedTarget);
      if (!hasFocus) scheduleAutoplay(interactionDelay);
    });

    carousel.addEventListener('pointerenter', function (event) {
      if (event.pointerType === 'touch') return;
      isHovered = true;
      pauseAutoplay();
    });

    carousel.addEventListener('pointerleave', function (event) {
      if (event.pointerType === 'touch') return;
      isHovered = false;
      scheduleAutoplay(interactionDelay);
    });

    track.addEventListener('pointerdown', function () {
      isPointerDown = true;
      pauseAutoplay();
    });
    track.addEventListener('pointerup', function () {
      isPointerDown = false;
      hasAutoplayStarted = true;
      scheduleAutoplay(interactionDelay);
    });
    track.addEventListener('pointercancel', function () {
      isPointerDown = false;
      scheduleAutoplay(interactionDelay);
    });

    document.addEventListener('visibilitychange', function () {
      if (document.hidden) pauseAutoplay();
      else scheduleAutoplay();
    });

    if ('IntersectionObserver' in window) {
      var visibilityObserver = new IntersectionObserver(function (entries) {
        isVisible = entries[0].isIntersecting;
        if (isVisible) scheduleAutoplay();
        else pauseAutoplay();
      }, { threshold: 0.15 });
      visibilityObserver.observe(carousel);
    }

    if (typeof reducedMotion.addEventListener === 'function') {
      reducedMotion.addEventListener('change', function () {
        if (reducedMotion.matches) pauseAutoplay();
        else scheduleAutoplay();
      });
    }

    scheduleAutoplay();
  });
})();
