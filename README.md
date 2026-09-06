# juniperkiss.com

Personal site of Juniper Kiss — CV, blog, and university assignments.
Static site built with [Jekyll](https://jekyllrb.com/) and hosted on GitHub Pages.

## Run it locally

```powershell
bundle install
bundle exec jekyll serve
# http://127.0.0.1:4000
```

Only one Jekyll process should listen on port 4000. Multiple old servers can
serve different `_site` builds and make refreshes appear inconsistent. Check
the listener before restarting:

```powershell
Get-NetTCPConnection -LocalPort 4000 -State Listen |
  Select-Object LocalAddress, LocalPort, OwningProcess

# Stop only the confirmed stale listener, then start Jekyll once.
Stop-Process -Id <PID>
bundle exec jekyll serve
```

## Motion and layout maintenance

The gentle reveal behaviour has two deliberately separate paths:

- Scroll reveals are controlled by `assets/js/reveal.js` and the
  `reveal-ready`/`reveal-armed` rules in `assets/css/site.css`. Initial element
  states are committed before transitions are armed. Each element only gains
  `is-revealed` once and is then unobserved. Never remove and re-add that class,
  or replace this path with a keyframe added after page load: either change
  makes already-rendered content flash and move again.
- Page-load reveals apply automatically to the shared `.post-header` used by
  Blog, Ancient Assignments, Repos, ordinary pages and individual posts.
  Custom Home and CV hero groups use `data-load-reveal`. These selectors are
  present before first paint, so their one-time keyframe is safe. The separate
  `--dur-load` token keeps the initial entrance slower than scroll reveals;
  `--load-delay` creates a restrained top-to-bottom sequence. Do not put hero
  content back into the scroll observer.
- The observer has a geometry fallback for browsers that delay
  `IntersectionObserver`. Both paths only add the final state; neither may
  toggle it while scrolling.
- Hidden responsive duplicates are ignored when reveal targets are collected.
  Keep all motion inside the existing `prefers-reduced-motion` guards.
- Blog and ordinary-page prose use the same scroll reveal for headings,
  paragraphs, lists, quotes, figures and galleries. Blocks inside an already
  animated group are not animated a second time. Desktop and mobile both
  fade once; keyboard focus, reduced motion and print keep content available.

CV photographs are lazy-loaded, so their space must be reserved before the
files arrive. `_includes/cv-entry.html` reads intrinsic dimensions from
`_data/cv_image_dimensions.json`. Whenever a CV image is added or replaced,
update its width and height in that data file. Missing or incorrect dimensions
can move entries while the visitor scrolls and look like a broken animation.

Before publishing motion or responsive changes, build from scratch and check
at least Home, CV, Repos, Blog, Assignments and Accessibility at both 390px and
1200px. Confirm that content reveals once, remains visible when scrolling back,
the page height stays stable as images load, and there is no horizontal
overflow. Also test with reduced motion enabled.

## Adding content

Start new posts by copying `_drafts/new-blog-entry.md`. Keep `published: false`
while writing: the template and drafts stay out of normal builds, listings,
feeds and the sitemap. See [Writing blog posts](docs/WRITING-BLOG-POSTS.md)
for local draft previews, photo galleries and publishing instructions.

Every page has a fixed "On this page" navigator on screens at least 1200px
wide; it is hidden on smaller screens and in print. The shared
`assets/js/section-nav.js` builds its links from `h2` headings and prose `h3`
subheadings, preserving existing IDs and generating unique IDs where needed.
The active link follows the scroll position. Add headings to the content to
update the navigator; no separate link list needs maintaining. It starts below
the breadcrumbs and follows the sticky masthead once the breadcrumbs scroll
away. The breadcrumb background spans the full viewport width, flush beneath
the masthead, with no outer gaps. Only its text follows the content column.
On Home, the navigator starts level with the hero text panel, using the
`data-section-nav-start` marker, then settles beneath the masthead on scroll.

All rectangular components use square corners through the shared radius
tokens. Keep circular icon controls circular.

The carousel pauses while the pointer is over it or keyboard focus is inside
it. It resumes after both leave, unless reduced motion is enabled or the
carousel/page is hidden. `_data/carousel.yml` preserves the original photo
order. Append new photographs at the end in the requested order; do not shuffle
the existing collection.

Photo descriptions should say what is visible, without inferring places,
events, dates or job context from filenames. The CV uses each image's `alt`
for its lightbox caption too; blog hero descriptions use `image_alt` in front
matter. Keep alt attributes escaped in shared templates. See
`docs/site-review-2026-09-05.md` for the visual review and suggested next steps.

Each blog post's `description` is a complete summary shown below the title
and reused in post cards and metadata. Hero images also need `image_alt`,
`image_width` and `image_height`. Blog galleries are grouped by post `slug`
and gallery key in `_data/blog_galleries.json`; render one with
`{% include blog-gallery.html gallery="gallery-1" %}`. Each image records its
local `src`, neutral `alt`, `width` and `height`. The shared component handles
captions, lazy loading and enlargement. Use the `video.html` include with
`id` and `title` for a YouTube video that loads only after a click.

Blog gallery groups with more than two images automatically become horizontal
photo strips, with previous/next buttons, keyboard arrows and touch scrolling.
They do not autoplay. One- and two-image groups keep the regular layout.
All photos retain their order, full-image previews and captions; print shows
the complete grid. Controls are in `assets/js/blog-gallery.js`.

| Task | File |
| --- | --- |
| New blog post | `_posts/YYYY-MM-DD-slug.md` (front matter: `layout: post`, `title`, `date`, `description`, `image`) |
| Post images | `assets/blog/<slug>/` |
| Blog galleries | `_data/blog_galleries.json` + `_includes/blog-gallery.html` |
| Home carousel | `_data/carousel.yml` + images in `assets/home/` |
| CV | `_data/cv.yml` |
| CV image dimensions | `_data/cv_image_dimensions.json` |
| Assignments | `_data/assignments.yml` + PDF in `assets/documents/` |
| Navigation | `_data/nav.yml` |
| Colours, type, spacing | `assets/css/tokens.css` |

Blog URLs use `/post/:slug/`, matching the old Wix site so inbound links keep
working. Do not change `permalink` in `_config.yml`.

### Reordering Home carousel photos

1. Open `_data/carousel.yml`. The carousel follows this file from top to bottom.
2. Find a photo by searching for its `src` filename or words in its `alt`
   description. Imported filenames use hyphens in place of spaces, dots and
   underscores: `2023-10-28 08.44.22` becomes
   `instagram-2023-10-28-08-44-22.jpg`.
3. Cut the whole photo entry, from `- src:` through its `width`, `height` and
   `alt` lines. Paste it before or after another complete entry. Keep the
   indentation exactly as it is. The first entry is the opening photo.
4. Save, run `bundle exec jekyll build`, and refresh the Home page. A server
   started with the ordinary `bundle exec jekyll serve` command rebuilds on
   changes automatically; a server using `--no-watch` needs the manual build.

No HTML edits are needed to change the order. `_includes/carousel.html`
renders the photos using `{% for photo in site.data.carousel %}`.
`index.html` places that component inside `hero__carousel-panel` with
`{% include carousel.html %}`. The actual image files are in `assets/home/`.
Do not edit `_site/index.html`: it is generated and gets replaced on each build.

## Design

Viridis palette with Kew-derived spacing and typography. The decorative botanical
motif is disabled pending a [complete redesign](docs/BOTANICAL-MOTIF-REDESIGN.md);
its source artwork is retained.

Built to WCAG 2.2 level AA — see [/accessibility/](https://juniperkiss.com/accessibility/).

## Docs

- [How this is deployed](docs/DEPLOYMENT.md)
- [Moving the domain off Wix](docs/DOMAIN-MIGRATION.md)

## `_migration/`

One-off scripts used to pull the content out of Wix (fetch posts, convert HTML,
download PDFs, optimise images). Excluded from the Jekyll build. Kept for the
record; not needed to run the site.
