/* Photo lightbox for the CV page.
   Thumbnails are plain links to the full image, so this is pure enhancement:
   with JavaScript off, clicking opens the image directly. */
(function () {
  'use strict';

  var dialog = document.getElementById('lightbox');
  if (!dialog || typeof dialog.showModal !== 'function') return;

  var image = dialog.querySelector('.lightbox__image');
  var caption = dialog.querySelector('.lightbox__caption');
  var closeButton = dialog.querySelector('.lightbox__close');
  var lastFocused = null;

  function open(link) {
    lastFocused = link;
    image.src = link.getAttribute('href');
    image.alt = link.getAttribute('data-caption') || '';
    caption.textContent = link.getAttribute('data-caption') || '';
    dialog.showModal();
    closeButton.focus();
  }

  document.addEventListener('click', function (event) {
    var link = event.target.closest ? event.target.closest('a.photo') : null;
    if (!link) return;
    // Let modified clicks open in a new tab as normal.
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
    event.preventDefault();
    open(link);
  });

  closeButton.addEventListener('click', function () {
    dialog.close();
  });

  // Click on the backdrop area closes.
  dialog.addEventListener('click', function (event) {
    if (event.target === dialog) dialog.close();
  });

  dialog.addEventListener('close', function () {
    image.src = '';
    image.alt = '';
    caption.textContent = '';
    if (lastFocused) {
      lastFocused.focus();
      lastFocused = null;
    }
  });
})();
