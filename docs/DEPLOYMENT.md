# How juniperkiss.com is deployed

## The short version

You write Markdown/HTML, run `git push`, and GitHub builds and serves the site.
There is no server to manage and nothing to pay for.

```
your laptop  --git push-->  GitHub repo  --Jekyll build-->  GitHub Pages CDN
                                                                  |
                                              DNS points juniperkiss.com here
                                                                  |
                                                        https://juniperkiss.com
```

## The pieces

| Piece | What it is | Where it lives |
| --- | --- | --- |
| Repository | `JuniperPNG/juniperkiss.com`, branch `main` | GitHub |
| Site generator | Jekyll, run automatically by GitHub Pages | GitHub's build servers |
| `CNAME` file | A one-line file in the repo root containing `juniperkiss.com`. This is what tells GitHub Pages "answer for this hostname" | repo root |
| `_config.yml` | `url` — used for absolute links in the sitemap and social cards | repo root |
| TLS certificate | Let's Encrypt, issued and renewed automatically by GitHub once DNS is correct | GitHub |
| DNS | The records that send `juniperkiss.com` to GitHub instead of Wix | **currently Wix — this is the bit that has to change** |

## What happens on `git push`

1. You push a commit to `main`.
2. GitHub Pages runs `jekyll build` on the repo.
3. The generated `_site` output is published to GitHub's CDN.
4. GitHub reads `CNAME` and serves that output for `juniperkiss.com`.
5. Because "Enforce HTTPS" is on, `http://` is redirected to `https://`.

Usually live within a minute. Build status appears under
**Settings → Pages** and in the **Actions** tab.

## Two things to know about this repo

**It is a *project* site, not a user site.** The repo is named
`juniperkiss.com`, not `JuniperPNG.github.io`. Without a custom domain it would
serve at `https://juniperpng.github.io/juniperkiss.com/`. The `CNAME` file is
what moves it to the root of your own domain, and `baseurl` is therefore empty.

**Do not delete the `CNAME` file.** It is regenerated whenever you set the
custom domain in **Settings → Pages**, but if it goes missing from a commit the
site silently reverts to the `github.io` address and your domain 404s.

## Old Wix URLs are preserved

`_config.yml` sets:

```yaml
permalink: /post/:slug/
```

That is deliberately the same URL shape Wix used
(`https://www.juniperkiss.com/post/mykindofamentor`), so every existing link,
bookmark, citation and search-engine result keeps working after the move.

## Local preview

```powershell
bundle install          # once
bundle exec jekyll serve # then open http://127.0.0.1:4000
```

`_site/`, `.jekyll-cache/` and `Gemfile.lock` are git-ignored; GitHub builds its
own copy.

## What is *not* on GitHub

- **Domain registration.** GitHub is not a registrar. Whoever you bought the
  domain from (currently Wix) stays the registrar unless you transfer it.
- **DNS.** GitHub does not host your DNS zone. You need the records to point at
  GitHub — see [DOMAIN-MIGRATION.md](DOMAIN-MIGRATION.md).
