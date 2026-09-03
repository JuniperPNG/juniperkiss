// Mobile navigation disclosure.
// Progressive enhancement: without JS the nav is a plain list that the CSS
// media query hides only because the toggle exists, so the toggle is created
// as visible-but-inert only when scripting is available.
(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  if (!toggle || !nav) return;

  function setOpen(open) {
    toggle.setAttribute("aria-expanded", String(open));
    nav.dataset.open = String(open);
  }

  toggle.addEventListener("click", function () {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });

  // Escape closes the menu and returns focus to the control (SC 2.1.2).
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      setOpen(false);
      toggle.focus();
    }
  });

  // Reset state when the layout returns to the desktop breakpoint.
  var wide = window.matchMedia("(min-width: 769px)");
  wide.addEventListener("change", function (event) {
    if (event.matches) setOpen(false);
  });
})();
