/* Dark-first theme toggle. The small inline script in <head> restores a saved
   choice before CSS paints; this script handles the footer control. */
(function () {
  'use strict';

  var root = document.documentElement;
  var toggle = document.querySelector('[data-theme-toggle]');
  if (!toggle) return;

  function currentTheme() {
    return root.dataset.theme === 'light' ? 'light' : 'dark';
  }

  function updateLabel() {
    var nextTheme = currentTheme() === 'dark' ? 'light' : 'dark';
    toggle.textContent = 'Switch to ' + nextTheme + ' mode';
    toggle.setAttribute('aria-label', 'Switch to ' + nextTheme + ' mode');
  }

  toggle.addEventListener('click', function () {
    var nextTheme = currentTheme() === 'dark' ? 'light' : 'dark';
    root.dataset.theme = nextTheme;

    try {
      window.localStorage.setItem('juniper-theme', nextTheme);
    } catch (error) {
      /* The toggle still works for this page when storage is unavailable. */
    }

    updateLabel();
  });

  updateLabel();
}());
