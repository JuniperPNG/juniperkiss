"""Convert opaque PNG blog images to JPEG and rewrite the references in _posts.

Many migrated images are photographs that Wix happened to store as PNG. At
~1 MB each they dominate the page weight of the longer posts. Images with real
transparency are left alone.
"""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).parent.parent
ASSETS = ROOT / "assets" / "blog"
POSTS = ROOT / "_posts"
QUALITY = 82
MIN_BYTES = 150 * 1024  # leave small PNGs (logos, diagrams) alone

renames: dict[str, str] = {}

for path in sorted(ASSETS.rglob("*.png")):
    if path.stat().st_size < MIN_BYTES:
        continue

    with Image.open(path) as im:
        if im.mode in ("RGBA", "LA", "P") and im.convert("RGBA").getchannel("A").getextrema()[0] < 255:
            print(f"  skip (transparent): {path.name}")
            continue
        target = path.with_suffix(".jpg")
        im.convert("RGB").save(target, "JPEG", quality=QUALITY, optimize=True, progressive=True)

    saved = path.stat().st_size - target.stat().st_size
    print(f"  {path.name}: saved {saved // 1024} KB")
    path.unlink()

    rel = path.relative_to(ROOT).as_posix()
    renames["/" + rel] = "/" + target.relative_to(ROOT).as_posix()

for md in sorted(POSTS.glob("*.md")):
    text = original = md.read_text(encoding="utf-8")
    for old, new in renames.items():
        text = text.replace(old, new)
    if text != original:
        md.write_text(text, encoding="utf-8")
        print(f"  updated refs in {md.name}")

total = sum(p.stat().st_size for p in ASSETS.rglob("*") if p.is_file())
print(f"\nassets/blog now {total / 1024 / 1024:.1f} MB")
