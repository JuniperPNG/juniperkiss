---
layout: post
title: "Working title"
slug: new-blog-entry
description: >-
  Write a complete one- or two-sentence summary here. It will appear below
  your title and in the blog listing when you publish.
published: false
excerpt_separator: "<!--more-->"
# Optional cover image: uncomment and replace all four values together.
# image: /assets/blog/new-blog-entry/cover.jpg
# image_alt: "Describe only what is visible in the cover image."
# image_width: 1600
# image_height: 1200
---

{% comment %}
This draft stays out of normal builds, blog listings, feeds and the sitemap.
Keep published: false while writing. Duplicate this file for each new post,
and give each copy its own title and slug.

Preview locally only: bundle exec jekyll serve --drafts --unpublished
Stop your existing local server first; only one can use port 4000.

When ready to publish, move your completed copy into _posts/ with a filename
such as YYYY-MM-DD-your-post-slug.md, set slug to your-post-slug, add the date
(for example date: YYYY-MM-DD HH:MM:SS +0100), and change published to true.
Use +0000 during GMT or the correct offset for your publication date.
Keep this template in _drafts/ with published: false.
{% endcomment %}

Write your opening paragraph here. Introduce the experience, question or idea
you want to explore, in your own words.

<!--more-->

## The beginning

Start your story here. Use short paragraphs, and keep the details that make
the experience yours.

## What happened next

Continue your story here.

### A closer look

Use a subheading when a section needs another level of detail. Headings also
become links in the page's section navigation.

{% comment %}
PHOTOS
Put image files in assets/blog/your-post-slug/.
In _data/blog_galleries.json, add your slug and named gallery groups. Each
photo needs src, alt, width and height, using its actual pixel dimensions.
See docs/WRITING-BLOG-POSTS.md for a copyable example.

Place this include between paragraphs once your gallery data is ready:
{% include blog-gallery.html gallery="gallery-1" %}

Groups of more than two photos automatically use a manual carousel.

VIDEO
Place this include between paragraphs after replacing the ID and title:
{% include video.html id="YOUTUBE_VIDEO_ID" title="Descriptive video title" %}
{% endcomment %}

## What stayed with me

Finish with your reflection, an open question or what happened afterwards.
