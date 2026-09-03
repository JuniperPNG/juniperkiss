"""Dump the visible text + image order of the archived Wix CV page.

Used to recover the original page structure (story notes, image placement)
that the first rebuild flattened.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

RAW = Path(__file__).parent / "raw_pages" / "cv.html"
OUT = Path(__file__).parent / "cv_structure.txt"

soup = BeautifulSoup(RAW.read_text(encoding="utf-8"), "html.parser")

for bad in soup(["script", "style", "noscript"]):
    bad.decompose()

lines: list[str] = []
seen: set[str] = set()

body = soup.find("body") or soup


def walk(node: Tag) -> None:
    for child in node.children:
        if isinstance(child, NavigableString):
            continue
        if not isinstance(child, Tag):
            continue

        if child.name == "img":
            src = child.get("src") or ""
            alt = (child.get("alt") or "").strip()
            key = "IMG" + src[:120]
            if key not in seen:
                seen.add(key)
                lines.append(f"[IMG] alt={alt!r}  src={src[:160]}")
            continue

        if child.name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            text = " ".join(child.get_text(" ", strip=True).split())
            if text and text not in seen:
                seen.add(text)
                lines.append(f"[{child.name.upper()}] {text}")
            continue

        if child.name in {"p", "li", "blockquote"}:
            text = " ".join(child.get_text(" ", strip=True).split())
            if text and text not in seen:
                seen.add(text)
                lines.append(f"[{child.name}] {text}")
            # still descend for nested imgs
        walk(child)


walk(body)

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"{len(lines)} lines -> {OUT}")
