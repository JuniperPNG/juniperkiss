---
layout: page
title: GitHub repos
eyebrow: Code
lede: >-
  R packages, pipelines and training materials — some public, some still
  private while they're under active development.
description: GitHub repositories and R tools built by Juniper Kiss.
body_class: page-repos
---

<div class="repo-feature">
<div class="repo-feature__copy" markdown="1">

## MAP ECR Training Programme

Training materials and a companion site for the Malaria Atlas Project's Early
Career Researcher programme.

- [GitHub: MAP_training](https://github.com/JuniperPNG/MAP_training)
- [Course site](https://juniperpng.github.io/MAP_training/)

</div>
<a class="repo-feature__logo-panel photo" href="{{ '/assets/map-ecr-program-2025.png' | relative_url }}"
   data-caption="A training programme table with columns for data wrangling, coding, communication and proposal writing."
   aria-label="Expand the MAP Dar ECR Development Program diagram">
  <img class="repo-feature__logo" src="{{ '/assets/map-ecr-program-2025.png' | relative_url }}"
       width="4555" height="3694" alt="A training programme table with columns for data wrangling, coding, communication and proposal writing." />
</a>
</div>

{% include cane-rule.html %}

<div class="repo-feature">
<div class="repo-feature__copy" markdown="1">

## engraftR *(teaser)*

An R package and multilingual R Shiny app for data-driven plant
prioritisation. It combines numerous live APIs, GBIF records and users' own
data to establish what they want to target, what they already hold and what
can be deduced.

Behind the interface: taxonomy wrangling with WCVP and WFO; enrichment from
more than ten datasets and databases; stakeholder-engagement tools; and a
weighted scoring system that reprioritises plants around each user's
selections. Still a private repo while it's under active development — get in
touch if you'd like early access or want to try it.

[Get in touch]({{ '/#contact' | relative_url }})

</div>
<a class="repo-feature__logo-panel photo" href="{{ '/assets/engraftr-logo.png' | relative_url }}"
   data-caption="The engraftR wordmark beneath a leaf, data symbols and numbered plant icons." aria-label="Expand the engraftR package logo">
  <img class="repo-feature__logo" src="{{ '/assets/engraftr-logo.png' | relative_url }}"
       width="1312" height="1199" alt="The engraftR wordmark beneath a leaf, data symbols and numbered plant icons." />
</a>
</div>

{% include cane-rule.html %}

<div class="repo-feature">
<div class="repo-feature__copy" markdown="1">

## whereisthatR *(teaser)*

An R package for geolocating health facilities and locality names using
multiple APIs. Potential coordinates move through several stages of review in
R Shiny apps, with fallback strategies throughout, before the best available
match is selected.

The approach has been used for the Malaria Atlas Project (MAP), WHO and the
Gates Foundation to geolocate health facilities and MIS/DHS clusters. The
package consolidates three earlier project-specific coordinate-matching
pipelines into one reusable workflow and is still under active development.

[Get in touch]({{ '/#contact' | relative_url }})

</div>
<a class="repo-feature__logo-panel photo" href="{{ '/assets/whereisthatr-logo.png' | relative_url }}"
   data-caption="The whereisthatR wordmark beneath a magnifying glass and location markers on a folded map." aria-label="Expand the whereisthatR package logo">
  <img class="repo-feature__logo" src="{{ '/assets/whereisthatr-logo.png' | relative_url }}"
       width="1330" height="1182" alt="The whereisthatR wordmark beneath a magnifying glass and location markers on a folded map." />
</a>
</div>

<dialog class="lightbox" id="lightbox" aria-label="Enlarged image">
  <button class="lightbox__close" type="button" aria-label="Close image">
    <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
      <path d="M5 5l10 10M15 5L5 15"/>
    </svg>
  </button>
  <figure class="lightbox__figure">
    <img class="lightbox__image" src="" alt="" />
    <figcaption class="lightbox__caption"></figcaption>
  </figure>
</dialog>
<script src="{{ '/assets/js/lightbox.js' | relative_url }}" defer></script>
