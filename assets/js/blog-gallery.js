/* Manual controls for larger blog galleries. Native scrolling and image links
   remain usable without JavaScript; these galleries never autoplay. */
(function () {
  'use strict';
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  document.querySelectorAll('[data-blog-carousel]').forEach(function (gallery) {
    var track = gallery.querySelector('.blog-gallery--carousel');
    var items = Array.prototype.slice.call(track.querySelectorAll('.blog-gallery__item'));
    var prev = gallery.querySelector('[data-gallery-prev]');
    var next = gallery.querySelector('[data-gallery-next]');
    var count = gallery.querySelector('[data-gallery-count]');
    var timer = 0;

    function update() {
      var bounds = track.getBoundingClientRect();
      var visible = [];
      items.forEach(function (item, index) {
        var rect = item.getBoundingClientRect();
        if (Math.min(rect.right, bounds.right) - Math.max(rect.left, bounds.left) > Math.min(rect.width, track.clientWidth) / 2) {
          visible.push(index + 1);
        }
      });
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 2;
      if (visible.length) {
        var first = visible[0], last = visible[visible.length - 1];
        count.textContent = (first === last ? first : first + '–' + last) + ' of ' + items.length + ' photos';
      }
    }

    function nearest() {
      var left = track.getBoundingClientRect().left + parseFloat(getComputedStyle(track).paddingLeft);
      var best = 0, distance = Infinity;
      items.forEach(function (item, index) {
        var gap = Math.abs(item.getBoundingClientRect().left - left);
        if (gap < distance) { best = index; distance = gap; }
      });
      return best;
    }

    function go(index) {
      var item = items[Math.max(0, Math.min(items.length - 1, index))];
      var inset = parseFloat(getComputedStyle(track).paddingLeft);
      track.scrollTo({
        left: track.scrollLeft + item.getBoundingClientRect().left - track.getBoundingClientRect().left - inset,
        behavior: reducedMotion.matches ? 'instant' : 'smooth'
      });
    }

    prev.addEventListener('click', function () { go(nearest() - 1); });
    next.addEventListener('click', function () { go(nearest() + 1); });
    track.addEventListener('keydown', function (event) {
      if (event.target !== track || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
      var target;
      if (event.key === 'ArrowLeft') target = nearest() - 1;
      else if (event.key === 'ArrowRight') target = nearest() + 1;
      else if (event.key === 'Home') target = 0;
      else if (event.key === 'End') target = items.length - 1;
      else return;
      event.preventDefault();
      go(target);
    });
    track.addEventListener('scroll', function () {
      window.clearTimeout(timer);
      timer = window.setTimeout(update, 120);
    }, { passive: true });
    if ('ResizeObserver' in window) new ResizeObserver(update).observe(track);
    else window.addEventListener('resize', update);
    gallery.querySelector('.blog-carousel__controls').hidden = false;
    update();
  });
}());
