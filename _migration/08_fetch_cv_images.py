"""Download the CV page photographs from Wix at full resolution.

The original CV was a photo essay: every experience had one or more images with
descriptive alt text. Filenames are derived from that alt text so the YAML is
readable.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
RAW = Path(__file__).parent / "raw_pages" / "cv.html"
OUT = ROOT / "assets" / "cv"
OUT.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (site migration)"}


def original_media_url(url: str) -> str:
    """Strip the Wix /v1/<transform>/ suffix to get the untouched upload."""
    return re.sub(r"/v1/.*$", "", url)


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    value = re.sub(r"[\s_-]+", "-", value)
    return value[:60].strip("-")


soup = BeautifulSoup(RAW.read_text(encoding="utf-8"), "html.parser")

seen: set[str] = set()
rows: list[tuple[str, str, str]] = []

for img in soup.find_all("img"):
    src = img.get("src") or ""
    if "static.wixstatic.com/media/" not in src:
        continue
    original = original_media_url(src)
    if original in seen:
        continue
    seen.add(original)

    alt = (img.get("alt") or "").strip()
    media_id = urlparse(original).path.rsplit("/", 1)[-1]
    ext = Path(media_id).suffix.lower() or ".jpg"
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        ext = ".jpg"

    # Skip the tiny social/nav icons.
    if re.fullmatch(r"[0-9a-f]{32}\.\w+", media_id):
        continue

    stem = slugify(alt) if alt and not re.match(r"^[\w.]+\.(jpg|png|jpeg|webp)$", alt, re.I) else ""
    if not stem:
        stem = "cv-" + media_id[:12]
    rows.append((original, f"{stem}{ext}", alt))

print(f"{len(rows)} images")

for url, filename, alt in rows:
    dest = OUT / filename
    if dest.exists():
        print(f"  have {filename}")
        continue
    try:
        r = requests.get(url, headers=HEADERS, timeout=60)
        r.raise_for_status()
        dest.write_bytes(r.content)
        print(f"  {filename}  ({len(r.content) // 1024} KB)  alt={alt!r}")
    except Exception as exc:  # noqa: BLE001
        print(f"  FAILED {filename}: {exc}")

manifest = Path(__file__).parent / "cv_images.txt"
manifest.write_text(
    "\n".join(f"{fn}\t{alt}" for _, fn, alt in rows), encoding="utf-8"
)
print(f"manifest -> {manifest}")
