# Writing a blog post

Copy `_drafts/new-blog-entry.md` to another file in `_drafts/` and edit that
copy. Change its `title`, `slug` and `description`; the description is the
summary shown above the article and on blog cards. Write the story below
the second `---` line using Markdown. The page supplies the main title, so
start section headings with `##` and subheadings with `###`.

Keep `published: false`. Normal builds omit the draft entirely, including
the article URL, Home/Blog listings, feed and sitemap. The template remains
excluded even if someone starts Jekyll with `--drafts` alone.

## Preview without publishing

Stop the current local server with Ctrl+C, then run:

```powershell
bundle exec jekyll serve --drafts --unpublished
```

The template preview is at `http://127.0.0.1:4000/post/new-blog-entry/`.
Your copy uses its own `slug`. These flags are for local preview only and
are not used by the GitHub Pages workflow. Return to the ordinary serve
command afterwards to remove drafts from the local preview.

## Add photographs

Save photos in `assets/blog/your-post-slug/`. Use neutral descriptions of
what is visible. Copy the following structure into `_data/blog_galleries.json`,
inside its outer braces alongside the other posts. Replace the slug, image
path and dimensions with your own. Separate neighbouring post entries with
a comma so that the whole file remains valid JSON.

```json
"your-post-slug": {
  "gallery-1": [
    {
      "src": "/assets/blog/your-post-slug/photo-01.jpg",
      "alt": "A description of what is visible in this image.",
      "width": 1600,
      "height": 1200
    }
  ]
}
```

Add more photo objects to the array, separated by commas, in the order you
want them displayed. Insert the gallery in your post with:

```liquid
{% include blog-gallery.html gallery="gallery-1" %}
```

One or two photos use the regular layout; larger groups become a horizontal
carousel. All support enlargement. Add `gallery-2`, and so on, for separate
groups between paragraphs. Images placed in `assets/` are public files when
pushed, even while their associated article remains a draft.

For a cover image, uncomment the four `image` fields in the template and
use the actual pixel dimensions. Do not leave a placeholder path active.

## Publish when ready

1. Move the finished draft into `_posts/` and name it
   `YYYY-MM-DD-your-post-slug.md` with the intended publication date.
2. Set `slug: your-post-slug`, add its `date` if you want a specific time,
   and change `published: false` to `published: true`.
3. Run `bundle exec jekyll build` and check the article locally.
4. Commit and push the completed post and its images when ready to publish.

Leave the reusable template unpublished in `_drafts/`.
