#!/usr/bin/env python3
"""Generate per-page OG images (1200x630) for key data-vault pages.

Template: dark solid bg + accent bar/label per category + big bold page title
(verbatim <title> text) + domain footer. Pure PIL, DejaVu Sans Bold.
Output: assets/og/<slug>.png, then rewrite og:image + og:image:alt in pages.
"""
import html
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
W, H = 1200, 630
BG = (13, 17, 23)          # #0d1117
FG = (240, 246, 252)       # #f0f6fc
MUTED = (139, 148, 158)    # #8b949e
BASE = "https://jayjex.github.io/data-vault"

# page path -> (slug, category label, accent RGB)
PAGES = [
    ("index.html",                        "index",                        "HOME",      (88, 166, 255)),
    ("products.html",                     "products",                     "PRODUCTS",  (240, 136, 62)),
    ("portfolio.html",                    "portfolio",                    "PORTFOLIO", (188, 140, 255)),
    ("free-printables-index.html",        "free-printables-index",        "PRINTABLES",(63, 185, 80)),
    ("guides/hud-fmr-2027.html",          "guide-hud-fmr-2027",           "GUIDE",     (227, 179, 65)),
    ("guides/dataset-license-guide.html", "guide-dataset-license",        "GUIDE",     (227, 179, 65)),
    ("guides/osm-civic-data-guide.html",  "guide-osm-civic-data",         "GUIDE",     (227, 179, 65)),
    ("datasets/hud-fmr-by-zip-2027.html", "dataset-hud-fmr-by-zip-2027",  "DATASET",   (57, 197, 207)),
    ("datasets/hud-fmr-2026.html",        "dataset-hud-fmr-2026",         "DATASET",   (57, 197, 207)),
    ("datasets/hud-fmr-metro-2027.html",  "dataset-hud-fmr-metro-2027",   "DATASET",   (57, 197, 207)),
]

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S)
OG_TITLE_RE = re.compile(r'(<meta property="og:title" content=")([^"]*)(">)')
OG_IMG_RE = re.compile(r'(<meta property="og:image" content=")([^"]*)(">)')
OG_ALT_RE = re.compile(r'(<meta property="og:image:alt" content=")([^"]*)(">)')


def extract_title(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        m = TITLE_RE.search(f.read())
    if not m:
        sys.exit(f"no <title> in {path}")
    return html.unescape(m.group(1)).strip()


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render(title: str, label: str, accent, out: str):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # accent top bar
    d.rectangle([0, 0, W, 10], fill=accent)
    # wordmark + category label
    f_small = ImageFont.truetype(FONT_BOLD, 30)
    d.text((80, 58), "DATA VAULT", font=f_small, fill=accent)
    lw = d.textlength(label, font=f_small)
    d.text((W - 80 - lw, 58), label, font=f_small, fill=MUTED)
    d.rectangle([80, 118, W - 80, 120], fill=(48, 54, 61))
    # title: start big, shrink until it fits 5 lines
    size = 76
    while size >= 40:
        f_title = ImageFont.truetype(FONT_BOLD, size)
        lines = wrap(d, title, f_title, W - 160)
        line_h = size + 18
        block_h = len(lines) * line_h
        if block_h <= 330 and all(d.textlength(ln, font=f_title) <= W - 160 for ln in lines):
            break
        size -= 4
    y = 190
    for ln in lines:
        d.text((80, y), ln, font=f_title, fill=FG)
        y += line_h
    # footer domain
    f_foot = ImageFont.truetype(FONT_REG, 28)
    d.text((80, H - 78), "jayjex.github.io/data-vault", font=f_foot, fill=MUTED)
    # accent bottom-right tick
    d.rectangle([W - 80 - 60, H - 84, W - 80, H - 80], fill=accent)
    img.save(out, "PNG", optimize=True)


def patch_meta(path: str, img_url: str, alt: str):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    esc = alt.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")
    src, n_img = OG_IMG_RE.subn(rf"\g<1>{img_url}\g<3>", src)
    src, n_alt = OG_ALT_RE.subn(rf"\g<1>{esc}\g<3>", src)
    if n_img == 0:
        sys.exit(f"og:image not found in {path}")
    if n_alt == 0:
        # insert after og:image:height
        src = src.replace(
            '<meta property="og:image:height" content="630">',
            '<meta property="og:image:height" content="630">\n'
            f'<meta property="og:image:alt" content="{esc}">',
            1,
        )
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    return n_img, n_alt


def main():
    os.makedirs(os.path.join(ROOT, "assets", "og"), exist_ok=True)
    for page, slug, label, accent in PAGES:
        title = extract_title(os.path.join(ROOT, page))
        out = os.path.join(ROOT, "assets", "og", f"{slug}.png")
        render(title, label, accent, out)
        kb = os.path.getsize(out) / 1024
        n_img, n_alt = patch_meta(
            os.path.join(ROOT, page), f"{BASE}/assets/og/{slug}.png", title
        )
        print(f"{page}: {slug}.png {kb:.0f}KB title={title[:60]!r} img={n_img} alt={n_alt}")


if __name__ == "__main__":
    main()
