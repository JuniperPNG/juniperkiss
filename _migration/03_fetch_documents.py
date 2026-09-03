"""Download the Wix static pages and pull out every attached PDF with its link text."""

from __future__ import annotations

import re
import shutil
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

MIGRATION = Path(__file__).parent
ROOT = MIGRATION.parent
RAW = MIGRATION / "raw_pages"
DOCS = ROOT / "assets" / "documents"

PAGES = ["", "cv", "assignments", "blog"]
UA = {"User-Agent": "Mozilla/5.0 (site migration; juniperkiss.com owner)"}


def fetch(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=180) as r, dest.open("wb") as f:
        shutil.copyfileobj(r, f)


def main() -> None:
    for page in PAGES:
        name = page or "home"
        fetch(f"https://www.juniperkiss.com/{page}", RAW / f"{name}.html")
        print("fetched", name)

    seen: dict[str, str] = {}
    for path in sorted(RAW.glob("*.html")):
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        for a in soup.find_all("a", href=re.compile(r"/_files/ugd/")):
            href = urllib.parse.urljoin("https://www.juniperkiss.com/", a["href"])
            label = re.sub(r"\s+", " ", a.get_text()).strip()
            seen.setdefault(href, label or href.rsplit("/", 1)[-1])

    print(f"\n{len(seen)} documents found")
    for href, label in seen.items():
        fname = re.sub(r"[^A-Za-z0-9._ -]+", "", label) or href.rsplit("/", 1)[-1]
        fname = re.sub(r"\s+", "-", fname.strip())
        if not fname.lower().endswith(".pdf"):
            fname += ".pdf"
        dest = DOCS / fname
        try:
            fetch(href, dest)
            print(f"  OK  {fname}")
        except Exception as exc:  # noqa: BLE001
            print(f"  !!  {fname}: {exc}")


if __name__ == "__main__":
    main()
