# AGENTS.md — juniperkiss.com

Personal Jekyll site (CV, blog, assignments) hosted on GitHub Pages. General
collaboration style (tone, commits, confirmations) is defined in a user-level
instructions file and applies automatically — no need to repeat it here.

## Build and run

```powershell
bundle install
bundle exec jekyll serve   # http://127.0.0.1:4000
bundle exec jekyll build   # -> _site/
```

See [README.md](README.md) for the content-editing table (posts, CV, nav, tokens).

## Architecture

- Content lives in `_data/*.yml` (`cv.yml`, `assignments.yml`, `nav.yml`,
  `countries.yml`), rendered by `_includes/*.html` components and `_layouts/`.
- CV is a photo-essay, not a timeline — see `/memories/repo/juniperkiss-cv-rebuild.md`
  for the `cv.yml` schema and rendering conventions if editing CV content.
- `_migration/` holds one-off Wix-import scripts, excluded from the Jekyll
  build. Historical record only — not needed to run the site.

## Conventions and gotchas

- **Never delete the `CNAME` file** or change `permalink: /post/:slug/` in
  `_config.yml` — both are load-bearing for keeping old Wix URLs working.
  See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).
- **Design system**: viridis palette, one font family only (`--font-sans` —
  do not add a second/display font), tokens in `assets/css/tokens.css`. Site
  targets WCAG 2.2 AA — see [/accessibility/index.md](accessibility/index.md)
  for the rationale.
  - Spacing/type rhythm is already Kew-inspired (`--pad-h`/`--pad-v`, fluid
    `--step-*` type scale, Roboto) — see the reference bundle at
    `C:\Users\junip\OneDrive - The Royal Botanic Gardens, Kew\DataProcessing\34_Kew_stylesheets\01_Kew_style_guide_22072026`
    for component patterns, but **not** its generous 112px/88px padding —
    this site is compact by design: no dead whitespace, avoid needless line
    breaks, favour tight `--space-*` values over the largest steps.
  - Mobile-first: check every new component at the existing breakpoints
    (1200px, 900px, 768px, 700px in `site.css`) before calling it done.
  - Tell the story with the bramble/topic-icon illustration system
    (`_includes/bramble.html`, `_includes/topic-icon.html`), not stock icons
    or emoji — extend that botanical set rather than introducing a new style.
  - Motion: use the existing `--dur`/`--ease` tokens for transitions and keep
    everything wrapped in the `prefers-reduced-motion` guard already in
    `site.css` — never add unconditional animation.
- **Content sensitivity**: do not mention a book/"Tendril" anywhere on the
  site unless the user explicitly asks — the bramble motif is described only
  as a botanical/design choice.
- **Uncommitted work risk**: this repo has repeatedly been left with
  uncommitted changes across sessions. Check `git status` and remind the user
  to commit before ending a session.
- Language is `en-GB` (`_config.yml`) — British spelling in all site content.
