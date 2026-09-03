// Click-to-load YouTube embeds. Nothing is requested from YouTube until the
// reader presses play, so the page stays first-party-only by default.
(function () {
  document.querySelectorAll(".video-embed").forEach(function (wrap) {
    var btn = wrap.querySelector(".video-embed__play");
    if (!btn) return;

    btn.addEventListener(
      "click",
      function () {
        var id = wrap.dataset.videoId;
        var title = btn.dataset.title || "YouTube video";

        var frameWrap = document.createElement("div");
        frameWrap.className = "video-embed__frame-wrap";

        var iframe = document.createElement("iframe");
        iframe.src = "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1";
        iframe.title = title;
        iframe.allow =
          "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
        iframe.allowFullscreen = true;

        frameWrap.appendChild(iframe);
        wrap.replaceChildren(frameWrap);
      },
      { once: true }
    );
  });
})();
