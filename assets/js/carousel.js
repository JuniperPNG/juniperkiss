/* Hero photo carousel prev/next buttons.
   Track scrolls natively (keyboard, trackpad, scrollbar) without this script;
   the buttons are pure enhancement on top of that. */
(function () {
  'use strict';

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

    function go(direction) {
      var target = nearestIndex() + direction;
      target = Math.max(0, Math.min(items.length - 1, target));
      items[target].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });
    }

    prev.addEventListener('click', function () {
      go(-1);
    });

    next.addEventListener('click', function () {
      go(1);
    });
  });
})();
