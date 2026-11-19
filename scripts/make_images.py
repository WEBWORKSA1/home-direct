#!/usr/bin/env python3
"""One-off generator for Home.Direct brand images (requires Pillow). Output: assets/img/."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)
INK, CORAL, PAPER, TEAL = (13, 27, 42), (255, 90, 54), (251, 248, 243), (14, 124, 116)
FONT_DIR = Path("/usr/share/fonts/opentype/inter")


def font(name, size):
    try:
        return ImageFont.truetype(str(FONT_DIR / name), size)
    except Exception:
        return ImageFont.load_default()


def mark(size, bg=INK):
    s = size
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=int(s * 0.275), fill=bg)
    w = max(2, int(s * 0.075))
    d.line([(s * .225, s * .5125), (s * .5, s * .2875), (s * .775, s * .5125)], fill="white", width=w, joint="curve")
    d.line([(s * .3375, s * .4875), (s * .3375, s * .75), (s * .6625, s * .75), (s * .6625, s * .4875)], fill="white", width=w, joint="curve")
    r = s * .125
    d.ellipse([s * .7375 - r, s * .7375 - r, s * .7375 + r, s * .7375 + r], fill=CORAL)
    return im


for px, name in [(180, "apple-touch-icon.png"), (192, "logo-192.png"), (512, "logo-512.png")]:
    mark(px).save(OUT / name)

# Open Graph image 1200x630
og = Image.new("RGB", (1200, 630), PAPER)
d = ImageDraw.Draw(og)
d.ellipse([760, -260, 1460, 440], fill=(255, 228, 219))
d.ellipse([-260, 380, 380, 1020], fill=(222, 241, 238))
og.paste(mark(132), (80, 80), mark(132))
d.text((236, 104), "Home", font=font("Inter-ExtraBold.otf", 64), fill=INK)
w = d.textlength("Home", font=font("Inter-ExtraBold.otf", 64))
d.text((236 + w, 104), ".", font=font("Inter-ExtraBold.otf", 64), fill=CORAL)
w2 = d.textlength(".", font=font("Inter-ExtraBold.otf", 64))
d.text((236 + w + w2, 104), "Direct", font=font("Inter-ExtraBold.otf", 64), fill=INK)
d.text((80, 270), "Go direct. Every home decision,", font=font("Inter-Bold.otf", 58), fill=INK)
d.text((80, 340), "minus the middleman.", font=font("Inter-Bold.otf", 58), fill=(232, 67, 31))
d.text((80, 452), "24 cost guides  ·  12 calculators  ·  Pro quotes  ·  Sell direct  ·  Live rates", font=font("Inter-Medium.otf", 30), fill=(90, 102, 118))
d.rounded_rectangle([80, 520, 420, 580], radius=30, fill=CORAL)
d.text((112, 534), "Free for homeowners", font=font("Inter-Bold.otf", 28), fill="white")
og.save(OUT / "og-image.png", optimize=True)

svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect x=".5" y=".5" width="39" height="39" rx="11" fill="#0d1b2a"/>'
       '<path d="M9 20.5l11-9 11 9" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
       '<path d="M13.5 19.5V30h13V19.5" stroke="#fff" stroke-width="3" fill="none" stroke-linejoin="round"/><circle cx="29.5" cy="29.5" r="5" fill="#ff5a36"/></svg>')
(OUT / "favicon.svg").write_text(svg, encoding="utf-8")
print("images written to", OUT)
