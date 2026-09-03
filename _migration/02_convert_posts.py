"""Convert downloaded Wix blog post HTML into Jekyll posts + local images.

Reads   _migration/raw/<slug>.html
Writes  _posts/<YYYY-MM-DD>-<slug>.md
        assets/blog/<slug>/<n>-<name>.<ext>
"""

from __future__ import annotations

import json
import re
import shutil
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

MIGRATION = Path(__file__).parent
ROOT = MIGRATION.parent
RAW = MIGRATION / "raw"
POSTS = ROOT / "_posts"
ASSETS = ROOT / "assets" / "blog"

# Inline tags kept inside a block; everything else is unwrapped.
INLINE_KEEP = {"a", "strong", "b", "em", "i", "u", "s", "code", "br", "sup", "sub"}
# Blocks copied verbatim rather than descended into.
ATOMIC = {"ul", "ol", "blockquote", "pre", "table"}
TEXT_BLOCK = {"p", "h1", "h2", "h3", "h4", "h5", "h6"}

UA = {"User-Agent": "Mozilla/5.0 (site migration; juniperkiss.com owner)"}


def original_media_url(url: str) -> str:
    """Strip Wix's on-the-fly resize transform to get the full-resolution original."""
    url = url.split("?")[0]
    marker = "/v1/"
    if marker in url:
        url = url[: url.index(marker)]
    return url


def slugify_filename(url: str) -> str:
    name = urllib.parse.unquote(url.rsplit("/", 1)[-1])
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-.")
    if "." not in name:
        name += ".jpg"
    stem, ext = name.rsplit(".", 1)
    return f"{stem[:60]}.{ext.lower()}"


def download(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=120) as r, dest.open("wb") as f:
            shutil.copyfileobj(r, f)
        return True
    except Exception as exc:  # noqa: BLE001 - migration script, report and carry on
        print(f"      ! image failed {url}: {exc}")
        return False


def clean_inline(node: Tag) -> None:
    """Strip Wix attributes and unwrap presentational tags, in place."""
    for el in list(node.find_all(True)):
        if el.name == "span":
            el.unwrap()
            continue
        if el.name not in INLINE_KEEP and el.name not in ATOMIC | TEXT_BLOCK | {"li", "img", "figure", "figcaption"}:
            el.unwrap()
            continue
        keep = {}
        if el.name == "a":
            href = el.get("href", "")
            if href:
                keep["href"] = rewrite_link(href)
            if href.startswith("http") and "juniperkiss.com" not in href:
                keep["rel"] = "noopener"
        if el.name == "img":
            keep["src"] = el.get("src", "")
            keep["alt"] = el.get("alt", "")
        el.attrs = keep


def rewrite_link(href: str) -> str:
    """Keep internal post links working after migration."""
    m = re.match(r"^https?://(www\.)?juniperkiss\.com(/.*)?$", href)
    if m:
        return m.group(2) or "/"
    return href


def collect_images(node: Tag) -> list[tuple[str, str]]:
    out = []
    for img in node.find_all("img"):
        src = img.get("src") or ""
        if "wixstatic.com" not in src:
            continue
        out.append((original_media_url(src), (img.get("alt") or "").strip()))
    return out


def has_text_block(node: Tag) -> bool:
    return node.find(lambda t: isinstance(t, Tag) and t.name in TEXT_BLOCK | ATOMIC) is not None


def extract_blocks(section: Tag, skip_images: set[str] | None = None) -> list[Tag | tuple[str, str]]:
    """Walk the Wix wrapper divs and return content blocks in document order."""
    blocks: list[Tag | tuple[str, str]] = []
    seen_images: set[str] = set(skip_images or ())

    def walk(node: Tag) -> None:
        for child in node.children:
            if not isinstance(child, Tag):
                continue
            if child.name in ATOMIC:
                blocks.append(child)
            elif child.name in TEXT_BLOCK:
                if has_text_block(child):
                    walk(child)
                elif child.get_text(strip=True):
                    blocks.append(child)
            elif child.name in {"img", "figure"} or (
                not has_text_block(child) and child.find("img") is not None
            ):
                for url, alt in collect_images(child):
                    if url not in seen_images:
                        seen_images.add(url)
                        blocks.append((url, alt))
            else:
                walk(child)

    walk(section)
    return blocks


def render(blocks, slug: str) -> str:
    out: list[str] = []
    img_n = 0
    for block in blocks:
        if isinstance(block, tuple):
            img_n += 1
            url, alt = block
            fname = f"{img_n:02d}-{slugify_filename(url)}"
            dest = ASSETS / slug / fname
            if download(url, dest):
                alt_attr = alt.replace('"', "&quot;")
                cap = f"\n  <figcaption>{alt}</figcaption>" if alt else ""
                out.append(
                    f'<figure class="post-figure">\n'
                    f'  <img src="/assets/blog/{slug}/{fname}" alt="{alt_attr}" loading="lazy" decoding="async" />{cap}\n'
                    f"</figure>"
                )
            continue

        clean_inline(block)
        block.attrs = {}
        html = block.decode()
        html = re.sub(r"\s+", " ", html).replace("> <", "><").strip()
        if block.name == "p" and not block.get_text(strip=True):
            continue
        out.append(html)
    return "\n\n".join(out)


def yaml_escape(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def convert(path: Path) -> None:
    slug = path.stem
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

    ld = json.loads(soup.find("script", type="application/ld+json").string)
    title = ld.get("headline", slug)
    published = datetime.fromisoformat(ld["datePublished"].replace("Z", "+00:00")).astimezone(timezone.utc)
    description = re.sub(r"\s+", " ", ld.get("description", "")).strip()[:300]
    hero = (ld.get("image") or {}).get("url")

    section = soup.find("section", attrs={"data-hook": "post-description"})

    front = [
        "---",
        "layout: post",
        f"title: {yaml_escape(title)}",
        f"date: {published.strftime('%Y-%m-%d %H:%M:%S')} +0000",
        f"slug: {slug}",
        f"description: {yaml_escape(description)}",
    ]
    skip: set[str] = set()
    if hero:
        hero_url = original_media_url(hero)
        skip.add(hero_url)
        hero_name = f"00-hero-{slugify_filename(hero_url)}"
        if download(hero_url, ASSETS / slug / hero_name):
            front.append(f"image: /assets/blog/{slug}/{hero_name}")

    body = render(extract_blocks(section, skip), slug)
    front += ["migrated_from: " + f"https://www.juniperkiss.com/post/{slug}", "---", ""]

    POSTS.mkdir(exist_ok=True)
    out = POSTS / f"{published.strftime('%Y-%m-%d')}-{slug}.md"
    out.write_text("\n".join(front) + body + "\n", encoding="utf-8")
    print(f"  -> {out.name}  ({len(body)} chars)")


def main() -> None:
    for path in sorted(RAW.glob("*.html")):
        print(path.stem)
        convert(path)


if __name__ == "__main__":
    main()
