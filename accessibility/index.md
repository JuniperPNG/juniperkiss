---
layout: page
title: Accessibility statement
eyebrow: Accessibility
lede: >-
  This site is built to WCAG 2.2 level AA, the standard referenced by UK, EU and
  Australian accessibility law.
description: >-
  Accessibility statement for juniperkiss.com — conformance target, known
  limitations, and how to report a problem.
---

## Commitment

I want everybody to be able to read this site, including people using screen
readers, keyboard-only navigation, screen magnification, speech input or reduced
motion settings.

## Conformance target

This website aims to conform to
[**Web Content Accessibility Guidelines (WCAG) 2.2, level AA**](https://www.w3.org/TR/WCAG22/).

That single target is what satisfies the relevant law in each place I work:

| Where | Instrument | What it asks for |
| --- | --- | --- |
| United Kingdom | Public Sector Bodies (Websites and Mobile Applications) Accessibility Regulations 2018; Equality Act 2010 | WCAG 2.2 AA and an accessibility statement |
| European Union | EN 301 549 (harmonised standard); Web Accessibility Directive 2016/2102; European Accessibility Act 2019/882 | WCAG 2.1/2.2 AA as incorporated by EN 301 549 |
| Australia | Disability Discrimination Act 1992; Digital Service Standard | WCAG 2.x AA |

This is a personal website, so it is not itself a public sector body under the UK
regulations. It is built to the same bar anyway.

{% include cane-rule.html %}

## How that is delivered

**Perceivable**

- Every meaningful image carries alternative text; decorative images, including
  the bramble motif, the flags and the topic icons, are marked `aria-hidden` and
  given empty `alt` text. Every flag and icon sits beside a text label.
- Colour is never the only means of conveying information. Assignment marks show
  a number, navigation shows the current page with weight and an underline as
  well as colour, and links inside body text are underlined.
- Body text meets a contrast ratio of at least 4.5:1, and interface components
  and graphics at least 3:1, against their background. The viridis palette is
  split explicitly into text-safe and decorative-only ranges in the
  [design tokens](/assets/css/tokens.css).
- The layout reflows to a 320 CSS pixel viewport without two-dimensional
  scrolling, and text can be resized to 200% without loss of content.

**Operable**

- Everything works from the keyboard, in a logical order, with a visible focus
  indicator (a dark ring with a high-luminance halo) that is not obscured by the
  sticky header.
- A "Skip to main content" link is the first thing in the tab order.
- Interactive targets are at least 24 by 24 CSS pixels, and primary controls are
  44 pixels.
- There is no motion that starts automatically. The bramble only draws itself in
  response to your own scrolling, and stops doing even that if your device
  requests reduced motion.
- The CV photographs open in a dialog. Escape closes it, focus is trapped inside
  it while open and returned to the thumbnail on close. With JavaScript off, the
  thumbnails are ordinary links that open the full image.

**Understandable**

- Page language is declared as British English.
- Navigation, headings and page structure are consistent throughout.
- There are no forms, no logins and no time limits.

**Robust**

- Pages are static HTML with semantic landmarks (`header`, `nav`, `main`,
  `footer`), correct heading order and ARIA only where native HTML is not enough.
- The site works with JavaScript disabled; the mobile menu, photo lightbox and
  video embeds all degrade to plain links that still work without a script.

## Privacy

This site sets no cookies and uses no analytics. It loads no third-party
fonts, scripts or trackers. The CV page has a few click-to-load YouTube
videos, but nothing is requested from YouTube until you choose to press play
on one — otherwise nothing about your visit is shared with another
organisation, so there is no cookie banner to get in your way.

## Known limitations

- Some blog posts migrated from the previous Wix site contain images that were
  originally published without alternative text. These are being described one by
  one. If you hit one that matters to you, please tell me and I will prioritise it.
- Assignments are shared as PDFs exactly as they were submitted at university.
  Those original files are not tagged for accessibility. If you need one of them
  in an accessible format, email me and I will provide it.

## Reporting a problem

Email <hello@juniperkiss.com>. Please say which page you were on and what went
wrong. I aim to reply within 10 working days.

*Statement prepared {{ 'now' | date: "%-d %B %Y" }}, based on a self-assessment
against WCAG 2.2 level AA.*
