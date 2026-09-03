"""Resize migrated images for the web.

Wix served transformed derivatives; the migration pulled the full-resolution
originals, which are far too heavy for a mobile connection. This caps the long
edge and re-encodes.

Usage: python 05_optimise_images.py [folder-under-assets] [max-edge]
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageOps

FOLDER = sys.argv[1] if len(sys.argv) > 1 else "blog"
MAX_EDGE = int(sys.argv[2]) if len(sys.argv) > 2 else 1600
ASSETS = Path(__file__).parent.parent / "assets" / FOLDER
JPEG_QUALITY = 82

before = after = 0

for path in sorted(ASSETS.rglob("*")):
    if not path.is_file() or path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        continue

    size_before = path.stat().st_size
    before += size_before

    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im)
        if max(im.size) > MAX_EDGE:
            im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)

        if path.suffix.lower() in {".jpg", ".jpeg"}:
            im.convert("RGB").save(path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
        elif path.suffix.lower() == ".png":
            im.save(path, "PNG", optimize=True)
        else:
            im.save(path, "WEBP", quality=JPEG_QUALITY, method=6)

    size_after = path.stat().st_size
    after += size_after
    print(f"  {path.name}: {size_before // 1024} KB -> {size_after // 1024} KB")

print(f"\nTotal: {before / 1024 / 1024:.1f} MB -> {after / 1024 / 1024:.1f} MB")
