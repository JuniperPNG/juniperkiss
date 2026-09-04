# 2026-09-03
# One-off: turn the user-supplied bramble/fruit/flags illustration into the
# site logo. Flood-fills the plain white background to transparent (seeded
# from the border only, so white regions inside flags/leaves are untouched)
# and produces a couple of resized PNGs for the masthead.
from PIL import Image, ImageDraw

SRC = r"C:\Users\junip\Dropbox\PC\Downloads\2afc7549-31ff-486f-90e4-94d464524db9.png"
OUT_DIR = r"c:\Users\junip\Dropbox\Website\juniperkiss.com\assets\brand"

WHITE_THRESHOLD = 10  # tolerance for near-white background pixels


def make_transparent(img: Image.Image) -> Image.Image:
    rgba = img.convert("RGBA")
    w, h = rgba.size
    seeds = [
        (0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
        (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2),
    ]
    for seed in seeds:
        if rgba.getpixel(seed)[3] == 0:
            continue  # already made transparent by an earlier seed
        ImageDraw.floodfill(rgba, seed, (255, 255, 255, 0), thresh=WHITE_THRESHOLD)
    return rgba


def main():
    src = Image.open(SRC)
    cutout = make_transparent(src)

    bbox = cutout.getbbox()
    if bbox:
        cutout = cutout.crop(bbox)

    cutout.save(f"{OUT_DIR}/logo-full.png")

    for name, height in (("logo-mark@2x.png", 160), ("logo-mark.png", 80)):
        ratio = height / cutout.height
        resized = cutout.resize((max(1, round(cutout.width * ratio)), height), Image.LANCZOS)
        resized.save(f"{OUT_DIR}/{name}")

    print("Saved:", cutout.size, "-> assets/brand/logo-full.png, logo-mark.png, logo-mark@2x.png")


if __name__ == "__main__":
    main()
