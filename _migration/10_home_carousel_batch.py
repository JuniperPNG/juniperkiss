"""Copy, resize (no cropping) and re-encode the home-page hero carousel photos.

One-off batch for the 2026-09-03 homepage carousel: pulls originals from their
real Dropbox locations, normalises EXIF orientation, caps the long edge
(never upscales, never crops — native aspect ratios are kept exactly as
shot), re-encodes for the web, and drops them into assets/home/ as
carousel-01.jpg .. carousel-NN.jpg. Prints a _data/carousel.yml-ready
fragment (including native pixel dimensions, for CLS-safe width/height
attributes) to stdout.

Usage: python 10_home_carousel_batch.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).parent.parent
DEST = ROOT / "assets" / "home"
MAX_EDGE = 1600
JPEG_QUALITY = 82

DROPBOX = Path.home() / "Dropbox"

# (source, output filename) — order matches the user's supplied list, minus
# the 2 items confirmed dropped (Costa Rica _MG_1300 — ambiguous, no such
# file; Instagram b.png — does not exist).
JOBS = [
    (DROPBOX / "Camera Uploads/FB/20240521032708__MG_1744[1]_edited.jpg", "carousel-01.jpg"),
    (DROPBOX / "Camera Uploads/FB/_MG_7227[1]_edited.jpg", "carousel-02.jpg"),
    (DROPBOX / "Camera Uploads/FB/_MG_7255[1]_edited.jpg", "carousel-03.jpg"),
    (DROPBOX / "PICS/AFRICA/11227937_1005018492882774_6809939664731933044_o.jpg", "carousel-04.jpg"),
    (DROPBOX / "PICS/Instagram/_MG_3102.jpg", "carousel-05.jpg"),
    (DROPBOX / "PICS/Costa Rica/FB/a.jpg", "carousel-06.jpg"),
    (DROPBOX / "PICS/Costa Rica/cccc.png", "carousel-07.jpg"),
    (DROPBOX / "PICS/Indonesia 2025/_MG_9785.JPG", "carousel-08.jpg"),
    (DROPBOX / "PICS/AUS/PICS/Tenerife PS/_MG_3790 copy.png", "carousel-09.jpg"),
    (DROPBOX / "UK/Southampton/KISS - PNG - Report/Counting the number of sweet potato varieties in a very steep garden with local children and Shen, an masters student from New Guinea Binatang Research Centre.jpg", "carousel-10.jpg"),
    (DROPBOX / "UK/Southampton/KISS - PNG - Report/Sweet potato garden in Sinopas.jpg", "carousel-11.jpg"),
    (DROPBOX / "Camera Uploads/FB/IMG_20210730_150637_262.jpg", "carousel-12.jpg"),
    (DROPBOX / "Camera Uploads/FB/IMG_20210804_004137_910.webp", "carousel-13.jpg"),
    (DROPBOX / "PICS/Instagram/CostaRica2.jpg", "carousel-14.jpg"),
    (DROPBOX / "PICS/Instagram/_MG_9928.JPG", "carousel-15.jpg"),
    (DROPBOX / "PICS/AUS/Dally/20221111_151228.jpg", "carousel-16.jpg"),
    (DROPBOX / "PICS/AUS/Dally/20221107_150023.jpg", "carousel-17.jpg"),
    (DROPBOX / "PICS/AUS/Dally/20221013_130013.jpg", "carousel-18.jpg"),
    (DROPBOX / "UK/Southampton/KISS - PNG - Report/Soil DNA extraction trials with beads.jpg", "carousel-19.jpg"),
    (DROPBOX / "UK/Southampton/KISS - PNG - Report/Microcentrifuge and DNA extraction kit testing at the University of Southampton, pre-trip.jpg", "carousel-20.jpg"),
    (DROPBOX / "PICS/Instagram/_MG_8572.JPG", "carousel-21.jpg"),
    (DROPBOX / "Camera Uploads/FB/IMG_20200111_132501_346.jpg", "carousel-22.jpg"),
    (DROPBOX / "Camera Uploads/FB/IMG_20190801_071933_852.jpg", "carousel-23.jpg"),
    (DROPBOX / "PICS/AUS/Perth - Oct 2022/1.jpg", "carousel-24.jpg"),
    (DROPBOX / "UK/Southampton/KISS - PNG - Report/We had great chats beside the evening fires with community leaders and farmers.jpg", "carousel-25.jpg"),
    (DROPBOX / "UK/Southampton/KISS - PNG - Report/View from Sinopas of an old hut with Mt Wilhelm in the background.jpg", "carousel-26.jpg"),
    (DROPBOX / "PICS/Instagram/_MG_8599.JPG", "carousel-27.jpg"),
    (DROPBOX / "UK/Southampton/KISS - PNG - Report/IMG20220102103818.jpg", "carousel-28.jpg"),
    (DROPBOX / "PICS/Indonesia 2025/_MG_8524.JPG", "carousel-29.jpg"),
    (DROPBOX / "PICS/Indonesia 2025/_MG_9084.JPG", "carousel-30.jpg"),
    (DROPBOX / "PICS/Instagram/_MG_0408.JPG", "carousel-31.jpg"),
    (DROPBOX / "PICS/AUS/PICS/Tenerife PS/_MG_3646 copy.png", "carousel-32.jpg"),
    (DROPBOX / "Camera Uploads/2025-09-02 08.50.01.jpg", "carousel-33.jpg"),
    (DROPBOX / "PICS/Indonesia 2025/_MG_9232.JPG", "carousel-34.jpg"),
    (DROPBOX / "Camera Uploads/2025-09-06 11.20.27.jpg", "carousel-35.jpg"),
    (DROPBOX / "PICS/Indonesia 2025/_MG_9519.JPG", "carousel-36.jpg"),
    (DROPBOX / "PICS/Indonesia 2025/_MG_9707.JPG", "carousel-37.jpg"),
    (DROPBOX / "PICS/AUS/Darwin/_MG_8125.JPG", "carousel-38.jpg"),
    (DROPBOX / "PICS/AUS/PICS/Tenerife PS/_MG_3383 copy.png", "carousel-39.jpg"),
    (DROPBOX / "PICS/AUS/PICS/Tenerife PS/_MG_3520 copy.png", "carousel-40.jpg"),
    (DROPBOX / "Camera Uploads/2025-09-14 12.26.48-3.JPG", "carousel-41.jpg"),
]


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    manifest = []
    for src, name in JOBS:
        if not src.exists():
            print(f"  MISSING: {src}")
            continue
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)
            if max(im.size) > MAX_EDGE:
                im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
            out = DEST / name
            im.convert("RGB").save(out, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
            w, h = im.size
        kb = out.stat().st_size // 1024
        print(f"  {name}: {w}x{h}  {kb} KB  <- {src}")
        manifest.append((name, w, h))

    print("\n--- _data/carousel.yml fragment ---")
    for name, w, h in manifest:
        print(f"- src: {name}\n  width: {w}\n  height: {h}\n  alt: \"TODO\"")


if __name__ == "__main__":
    main()
