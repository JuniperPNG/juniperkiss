# juniperkiss.com

Personal site of Juniper Kiss — CV, blog, and university assignments.
Static site built with [Jekyll](https://jekyllrb.com/) and hosted on GitHub Pages.

## Run it locally

```powershell
bundle install
bundle exec jekyll serve
# http://127.0.0.1:4000
```

## Adding content

| Task | File |
| --- | --- |
| New blog post | `_posts/YYYY-MM-DD-slug.md` (front matter: `layout: post`, `title`, `date`, `description`, `image`) |
| Post images | `assets/blog/<slug>/` |
| CV | `_data/cv.yml` |
| Assignments | `_data/assignments.yml` + PDF in `assets/documents/` |
| Navigation | `_data/nav.yml` |
| Colours, type, spacing | `assets/css/tokens.css` |

Blog URLs use `/post/:slug/`, matching the old Wix site so inbound links keep
working. Do not change `permalink` in `_config.yml`.

## Design

Viridis palette, Kew-derived spacing and typography, and a bramble cane drawn as
a botanical illustration running down the left gutter of every page. Documented
at [/colophon/](https://juniperkiss.com/colophon/).

Built to WCAG 2.2 level AA — see [/accessibility/](https://juniperkiss.com/accessibility/).

## Docs

- [How this is deployed](docs/DEPLOYMENT.md)
- [Moving the domain off Wix](docs/DOMAIN-MIGRATION.md)

## `_migration/`

One-off scripts used to pull the content out of Wix (fetch posts, convert HTML,
download PDFs, optimise images). Excluded from the Jekyll build. Kept for the
record; not needed to run the site.
