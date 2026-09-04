/* Lightweight deterrents for casual saving of original photographs. Public
   web assets can still be retrieved from network tools or screenshots. */
(function () {
  'use strict';

  var selector = [
    '.photo img',
    '.photo-carousel img',
    '.post-hero img',
    '.rich-text img',
    '.cv-header__portrait',
    '.about__art img'
  ].join(',');

  document.querySelectorAll(selector).forEach(function (image) {
    image.setAttribute('draggable', 'false');
    image.setAttribute('data-protected-image', '');
  });

  document.addEventListener('contextmenu', function (event) {
    if (event.target.closest('[data-protected-image]')) {
      event.preventDefault();
    }
  });
})();
