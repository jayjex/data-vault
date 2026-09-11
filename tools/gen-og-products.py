#!/usr/bin/env python3
"""Generate product OG banners (1200x630) for catalog products without pages.

Same template as tools/gen-og.py (dark bg, accent bar/label, big bold title,
domain footer), plus a price band: "<price> - <store>". Titles verbatim from
state/portfolio.json product names. Output only: assets/og/<slug>.png.
No meta patching here: these products have no dedicated pages yet, so the
banners ship as ready-to-use assets (future product pages / store listings).
"""
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
W, H = 1200, 630
BG = (13, 17, 23)          # #0d1117
FG = (240, 246, 252)       # #f0f6fc
MUTED = (139, 148, 158)    # #8b949e
ACCENT = (240, 136, 62)    # PRODUCTS orange, matches gen-og.py

# slug -> (product title, price label, store label)
PRODUCTS = [
    ("agent-prompt-pack-vol1",
     "Agent Prompt Pack Vol.1: 23 Production-Tested Prompts",
     "$9", "Getly"),
    ("agent-prompt-pack-vol2",
     "QA Agent Prompt Pack Vol.2: 10 QA Agent Prompts (Role + Steps + Output Format + Test Plan)",
     "$9", "Getly"),
    ("airbnb-pack-vol2",
     "US Airbnb Listings Pack Vol 2: 8 Cities, 90,746 Rows, June 2026 Snapshots (CSV)",
     "$12", "Fourthwall"),
    ("wallpaper-pack-vol4",
     "Wallpaper Pack Vol.4 - 10 Minimal AI Walls (Nordic Fog + Riso Botanical)",
     "$12", "Fourthwall"),
]


def wrap(draw, text, font, max_w):
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


def render(title, price, store, out):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # accent top bar
    d.rectangle([0, 0, W, 10], fill=ACCENT)
    # wordmark + category label
    f_small = ImageFont.truetype(FONT_BOLD, 30)
    d.text((80, 58), "DATA VAULT", font=f_small, fill=ACCENT)
    lw = d.textlength("PRODUCT", font=f_small)
    d.text((W - 80 - lw, 58), "PRODUCT", font=f_small, fill=MUTED)
    d.rectangle([80, 118, W - 80, 120], fill=(48, 54, 61))
    # title: start big, shrink until it fits the reserved block
    size = 72
    while size >= 36:
        f_title = ImageFont.truetype(FONT_BOLD, size)
        lines = wrap(d, title, f_title, W - 160)
        line_h = size + 16
        block_h = len(lines) * line_h
        if block_h <= 270 and all(d.textlength(ln, font=f_title) <= W - 160 for ln in lines):
            break
        size -= 4
    y = 170
    for ln in lines:
        d.text((80, y), ln, font=f_title, fill=FG)
        y += line_h
    # price band
    f_price = ImageFont.truetype(FONT_BOLD, 40)
    d.text((80, 462), f"{price} - {store}", font=f_price, fill=ACCENT)
    # footer domain
    f_foot = ImageFont.truetype(FONT_REG, 28)
    d.text((80, H - 78), "jayjex.github.io/data-vault", font=f_foot, fill=MUTED)
    # accent bottom-right tick
    d.rectangle([W - 80 - 60, H - 84, W - 80, H - 80], fill=ACCENT)
    img.save(out, "PNG", optimize=True)


def main():
    os.makedirs(os.path.join(ROOT, "assets", "og"), exist_ok=True)
    for slug, title, price, store in PRODUCTS:
        out = os.path.join(ROOT, "assets", "og", f"{slug}.png")
        render(title, price, store, out)
        kb = os.path.getsize(out) / 1024
        print(f"{slug}.png {kb:.0f}KB price={price} store={store} title={title[:50]!r}")


if __name__ == "__main__":
    main()
