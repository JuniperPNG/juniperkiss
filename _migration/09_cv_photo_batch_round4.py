"""Copy, resize and re-encode the round-4 CV photos from Dropbox/Downloads.

One-off batch for the 2026-09-03 CV fixes: pulls originals from their real
locations (found via Get-ChildItem), normalises orientation, caps the long
edge, re-encodes for the web, and drops them straight into assets/cv/ under
the descriptive filenames used in _data/cv.yml.

Usage: python 09_cv_photo_batch_round4.py
"""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).parent.parent
DEST = ROOT / "assets" / "cv"
DOCS = ROOT / "assets" / "documents"
MAX_EDGE = 1600
JPEG_QUALITY = 82

DROPBOX = Path.home() / "Dropbox"
DOWNLOADS = Path.home() / "Downloads"

# (source, destination filename, special-processing key or None)
JOBS = [
    (DROPBOX / "UK/Southampton/Applications/SES/Report/_MG_6139.jpg", "rgs-grant-fieldwork.jpg", None),
    (DROPBOX / "UK/Southampton/Applications/SES/Report/_MG_6261.jpg", "taa-award-fieldwork.jpg", None),
    (DROPBOX / "PICS/AUS/PNG-QLD Apr 2022/_MG_7097.JPG", "bspp-fellowship-fieldwork.jpg", None),
    (DROPBOX / "PICS/Instagram/_MG_1300.JPG", "nhm-young-systematists-award.jpg", None),
    (DROPBOX / "PICS/Instagram/_MG_9837.JPG", "c-roy-adair-scholar-award.jpg", None),
    (DROPBOX / "PICS/Instagram/IMG_8071.JPG", "anglia-trust-nepal-2.jpg", None),
    (DROPBOX / "PICS/PNG/PNG - Pics/PICS/PNG pics/_MG_6262.JPG", "heredity-fieldwork-grant.jpg", None),
    (DROPBOX / "PICS/ASA/_MG_3537.JPG", "nelson-yield-limiting-scholarship.jpg", None),
    (DROPBOX / "GoogleDrive/INSPIRE dTP/INSPIRE DTP - shared/PhD planning/Extractions trials - Dec 2021/IMG_3186 copy.jpg", "neof-extractions-trial.jpg", None),
    (DROPBOX / "PICS/Nepal/IMG_8212.JPG", "anglia-trust-nepal-1.jpg", None),
    (DOWNLOADS / "IMG-20260424-WA0003v.jpg", "kew-hosting-ethiopian-diplomats.jpg", None),
    (DOWNLOADS / "10_MG_0401.jpg", "extension-nt-photo-1.jpg", None),
    (DOWNLOADS / "20_MG_0579.jpg", "extension-nt-photo-2.jpg", None),
    (DOWNLOADS / "IMG-20241102-WA0006.jpg", "ammnet-symposium-dar-es-salaam.jpg", "brighten"),
    (DOWNLOADS / "496924556_10161310499156367_3464311569926305963_n.jpg", "rsb-stapledon-graduation.jpg", None),
    (DOWNLOADS / "52905704_2296811543703456_6537156373036138496_n.jpg", "phenome-travel-grant-tucson.jpg", None),
    (DOWNLOADS / "650050993_10163396464427773_2208370334915730167_n.jpg", "big-pitch-aru.jpg", "crop-height"),
    (DROPBOX / "PICS/Miami/_MG_1950B.jpg", "david-miller-corbana-miami.jpg", None),
    (DROPBOX / "PICS/Instagram/Greenhouse.jpg", "corteva-travel-award-minnesota.jpg", None),
    (DROPBOX / "UK/ARU/GOES/GOES magazine/GOES/BSB.JPG", "be-the-change-goes-module.jpg", None),
    (DROPBOX / "UK/ARU/GOES/GOES magazine/GOES/lucidpress.PNG", "andy-wilson-bursary-goes.png", None),
    (DROPBOX / "UK/ARU/RUBUS/20170712_111415_Richtone(HDR).jpg", "john-ray-summer-research.jpg", None),
    (DOWNLOADS / "Screenshot 2026-09-03 143417.png", "golden-opportunities-asa.png", None),
    (DROPBOX / "PICS/Camera Uploads/2020-02-26 09.02.31.jpg", "mres-presentation-slide-1.jpg", None),
    (DROPBOX / "PICS/Camera Uploads/2020-03-01 10.08.31-1.jpg", "mres-presentation-slide-2.jpg", None),
]

DOC_JOBS = [
    (DROPBOX / "UK/ARU/RUBUS/Phenome_poster/PhenomePoster_Ed7(3).pdf", "phenome-poster.pdf"),
]


def process(im: Image.Image, key: str | None) -> Image.Image:
    if key == "brighten":
        # Reader's WhatsApp photo was underexposed/flat — lift shadows and pop.
        im = ImageOps.autocontrast(im, cutoff=1)
        im = ImageEnhance.Brightness(im).enhance(1.18)
        im = ImageEnhance.Contrast(im).enhance(1.08)
    elif key == "crop-height":
        # Crop the tall Facebook photo down to a shorter strip, keeping heads
        # and the certificate but dropping the legs/feet at the bottom.
        w, h = im.size
        top = int(h * 0.06)
        target_h = int(h * 0.42)
        im = im.crop((0, top, w, top + target_h))
    return im


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    for src, name, key in JOBS:
        if not src.exists():
            print(f"  MISSING: {src}")
            continue
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)
            im = process(im, key)
            if max(im.size) > MAX_EDGE:
                im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
            out = DEST / name
            if name.lower().endswith(".png"):
                im.save(out, "PNG", optimize=True)
            else:
                im.convert("RGB").save(out, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        print(f"  {name}: {out.stat().st_size // 1024} KB  <- {src}")

    DOCS.mkdir(parents=True, exist_ok=True)
    for src, name in DOC_JOBS:
        if not src.exists():
            print(f"  MISSING: {src}")
            continue
        shutil.copyfile(src, DOCS / name)
        print(f"  {name}  <- {src}")


if __name__ == "__main__":
    main()
