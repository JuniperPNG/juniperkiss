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
  Blog, Ancient Assessments, Repos, ordinary pages and individual posts.
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

| Task | File |
| --- | --- |
| New blog post | `_posts/YYYY-MM-DD-slug.md` (front matter: `layout: post`, `title`, `date`, `description`, `image`) |
| Post images | `assets/blog/<slug>/` |
| CV | `_data/cv.yml` |
| CV image dimensions | `_data/cv_image_dimensions.json` |
| Assignments | `_data/assignments.yml` + PDF in `assets/documents/` |
| Navigation | `_data/nav.yml` |
| Colours, type, spacing | `assets/css/tokens.css` |

Blog URLs use `/post/:slug/`, matching the old Wix site so inbound links keep
working. Do not change `permalink` in `_config.yml`.

## Design

Viridis palette, Kew-derived spacing and typography, and a bramble cane drawn as
a botanical illustration running down the left gutter of every page.

Built to WCAG 2.2 level AA — see [/accessibility/](https://juniperkiss.com/accessibility/).

## Docs

- [How this is deployed](docs/DEPLOYMENT.md)
- [Moving the domain off Wix](docs/DOMAIN-MIGRATION.md)

## `_migration/`

One-off scripts used to pull the content out of Wix (fetch posts, convert HTML,
download PDFs, optimise images). Excluded from the Jekyll build. Kept for the
record; not needed to run the site.
