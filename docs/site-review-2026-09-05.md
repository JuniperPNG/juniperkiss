# Site review — 5 September 2026

The strongest direction is precise layout with candid writing: consistent
edges, predictable navigation and readable evidence, with the detours,
humour and personal notes left intact. The CV's combination of professional
entries and informal margin notes already supports that balance.

## Changes completed

- The hero copy and carousel panels stretch to the same grid-row height.
  Their entrance animations use the same delay, so the backgrounds remain
  aligned during the transition. Stacked mobile panels keep their natural
  heights, and photographs retain their aspect ratios.
- Neutral visual descriptions replace placeholders, generic descriptions
  and unverified context across 169 carousel images, 77 CV image entries and
  228 blog image placements, including repeated thumbnails. Existing blog
  figure captions were updated alongside their images. Twelve blog hero
  images now have their own `image_alt` field; the homepage artwork, portraits
  and repository illustrations were also reviewed.
- Shared templates escape alt attributes, preventing quotation marks in
  descriptions from breaking the HTML.
- Carousel movement now scrolls only the horizontal photo track. The previous
  `scrollIntoView` call could also move the page and pull the reader towards
  the hero during autoplay.

## Photo review findings

Descriptions should identify what is visible. A location, award, date or job
should not be inferred from a filename or the surrounding CV entry. Text
actually printed in a slide, certificate or graphic can be described.
This follows the user's requested neutral approach and the purpose-based
approach in the [W3C image tutorial](https://www.w3.org/WAI/tutorials/images/).

Examples of corrections:

| Previous description | What the image shows |
| --- | --- |
| Graduating from Aberystwyth University | Two speakers at a lectern with Royal Society of Biology branding |
| Young Systematists Forum at the Natural History Museum | A young bramble plant in a container |
| Tropical Agriculture Association fieldwork | Cooked banana slices on a plate |
| C. Roy Adair Scholar award | Crop rows, a pick-up truck and dry hills |
| Banana field trial in Papua New Guinea | Small cultivated plots on a steep hillside |
| Bramble project untangling a classification system | A laptop and equipment used to photograph leaves |

The image files and their placement within CV entries have been retained.
Neutral descriptions correct what is said about them; they do not establish
whether each photograph belongs under its current job or award. The NIAB
flowering-field image and some imported blog photos are visibly sideways;
orientation needs a separate image pass.

Text-heavy infographics and research slides would also benefit from adjacent
HTML summaries or transcripts. The new alt text identifies their visible
subject; it does not reproduce every data point or paragraph inside them.

## Suggested next work, in priority order

This table records the original review. The follow-up implementation below
supersedes the completed parts of recommendations 1, 3, 4 and 8.

| Priority | Recommendation | Benefit and scope |
| --- | --- | --- |
| 1 | Give the carousel a visible Pause/Play control, stop on hover and keyboard focus, and slow the rotation. | It currently advances roughly every 2.5 seconds and resumes shortly after focus. Allow time to inspect a photograph without chasing it. Preserve autoplay as an optional behaviour. |
| 2 | Create responsive image sizes and a smaller initial carousel selection. | The 169 carousel files total 99.8 MB on disk. Lazy loading means this is **not** the initial page download, but browsing the whole gallery can still be expensive. Use smaller variants for the 220px mobile and 380px desktop photo rows; keep originals for a full gallery. |
| 3 | Finish the Wix gallery migration. | The review needed 108 distinct remote Wix image files beyond local copies. Some posts repeat large images and thumbnails. Replace imported gallery markup with one shared local gallery component, intrinsic dimensions, lazy loading and consistent captions. This also removes a remaining dependency on Wix. |
| 4 | Remove the repeated opening paragraph from About. | The hero and About currently repeat the account of first building the site as a final-year undergraduate. Keep the concise introduction in the hero; let About start with the specific stories. This shortens the homepage without losing its voice. |
| 5 | Define compact spacing rules for pairs and cards. | Replace repeated inline margins with a few component classes. Consider reducing the 64px hero/About column gaps to 24–32px, and the 64–96px hero outer padding to 32–48px. Align card headings and action rows; avoid forcing unrelated prose into equal-height boxes. |
| 6 | Make content columns respond to their actual available width. | The new sidebar consumes 192px, but several grids still switch using viewport width. Container queries would let CV entries and repository panels adapt to their own content width, avoiding cramped columns around desktop breakpoints. |
| 7 | Simplify motion. | Use one short reveal per group with a small translation and no blur. Keep paired panels synchronised. Preserve reduced-motion support and avoid repeated fading on carousel images while someone is reading nearby text. |
| 8 | Tighten the professional entry points. | Keep the first-person stories and margin notes, but make current work, selected outputs and ways to collaborate easy to scan. Add an explicit “updated” date to current CV information. Give older blog posts concise, complete summaries; some migrated descriptions currently end mid-sentence. |

The recommended carousel controls follow the
[W3C carousel pattern](https://www.w3.org/WAI/ARIA/apg/patterns/carousel/).
The other recommendations are based on the repository and visual inspection,
not on a measured Core Web Vitals audit.

## Architecture

Keep Jekyll, data-driven CV content, shared includes, local design tokens and
small JavaScript enhancements. There is no clear need for a framework rewrite.
The useful architectural work is a shared image/gallery model, consistent
spacing classes and build-time validation for missing image files, dimensions
and placeholder descriptions. Keep visible captions separate from alt text
if personal context is added later: alt describes the image, while a caption
can carry verified context or a personal observation.

## Verification

- Jekyll build and JavaScript syntax checks passed.
- Hero panels have a measured 0px difference in top edge, bottom edge and
  height at 901, 1024, 1199, 1200, 1440 and 1600px. At 900, 768, 700 and
  390px they stack without horizontal overflow.
- The Home, CV, Repos, Blog, Assignments and Accessibility layouts were checked
  at desktop and mobile widths. Light and dark themes, normal and reduced
  motion, and matching panel alignment during the entrance were checked.
- Rendered CV image descriptions and a corrected lightbox caption were
  verified. All 228 blog body images have non-empty descriptions; descriptions
  were also checked in the rendered DOM of the ten posts containing them.
- Carousel controls and autoplay preserve the document scroll position, and
  an incoming section link remains at its destination.
- Structural comparisons confirm that CV data apart from alt text, carousel
  ordering and dimensions, and blog prose and image URLs remain unchanged.

## Follow-up implementation

- Carousel autoplay pauses for the full duration of hover or keyboard focus,
  including moving focus between its controls. It resumes once both have
  left. Reduced motion and page/carousel visibility still take precedence.
- Removed the duplicated opening paragraph from Home's About section.
- Added all 59 distinct requested photos, including the Indonesian volcano
  confirmed for `_MG_8591`. Repeated filenames were imported once. Images
  were visually reviewed, given neutral descriptions, oriented using EXIF
  metadata and resized to at most 1600px on the longest edge. Original files
  remain untouched. The carousel now contains 228 images: the original 169
  retain their exact order, followed by the 59 additions in the requested
  order. This corrects the earlier, unwanted shuffle.
- Set rectangular corner tokens and remaining explicit rectangular radii
  to zero, including cards, navigation frames and video containers.
- Positioned the fixed section navigator below the breadcrumb band. The
  breadcrumb background spans the full viewport width, flush beneath the
  masthead with no outer gaps; only the text follows the content column.
- Completed the remaining blog gallery migration against the
  [original Wix site](https://tykoonbk.wixsite.com/juniperkiss/). Its blog
  sitemap contains the same 13 posts as this repository. Downloaded 108
  additional local image assets and removed 73 repeated thumbnail placements.
  Every image in the original article HTML has a local asset. The resulting
  posts contain 155 body images and 12 hero images, all with intrinsic
  dimensions and reviewed descriptions; none loads an image from Wix.
- Replaced imported image lists with one shared gallery include and data
  file, consistent neutral captions, lazy loading and image enlargement.
  Hero images show their full contents and can also be enlarged.
- Restored six YouTube videos omitted by the earlier converter, using IDs
  found in the original articles and titles checked against YouTube metadata.
  Players load only on request and have ordinary YouTube fallback links.
- Added complete summaries above the images on all 13 posts and reused them
  in blog cards and metadata. Converted existing section labels to semantic
  headings and repaired internal post links that incorrectly used `/blog/`.

### Follow-up verification

- Jekyll build, JavaScript syntax checks and `git diff --check` passed.
- Checked Home, CV, Repos, Blog, Assignments, Accessibility and a long blog
  post at 1600, 1440, 1200, 1199, 900, 768, 700 and 390px: no horizontal
  overflow; section navigation hidden below 1200px; square nav frames;
  breadcrumb text aligned with the content; desktop hero edges match exactly.
- Tested scroll-based active navigation, hover and focus pause, focus moving
  within the carousel, resume after leaving and reduced-motion suppression.
- All 167 rendered blog images decoded successfully with Wix blocked.
  Every post has a complete summary above its hero, local image dimensions,
  working image enlargement and Escape-to-close behaviour. All six video
  players have titles and remain unloaded until activated.
- Compared prose before and after migration: story text is preserved.
  All internal links in rendered posts resolve to local pages or assets.
- New carousel assets total 19.0 MB and new blog assets 26.0 MB on disk.
  These are whole-collection sizes, not initial page downloads. Responsive
  image variants remain a useful future performance improvement.

These are local changes; publishing and domain/DNS changes are separate.
