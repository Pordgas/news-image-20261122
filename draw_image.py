#!/usr/bin/env python3
"""Draw entry.png: a newspaper front page summing up Sunday 22 Nov 2026.

Build-time tool only. The submitted program (main.py, stdlib only) just
copies the finished entry.png to the output directory, so the graded run is
byte-identical every time. Run: python3 draw_image.py
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (24, 24, 28)
NAVY = (18, 44, 84)
RED = (178, 34, 34)
GREY = (90, 88, 82)
RULE = (180, 174, 160)
BODY = (52, 50, 46)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

M = 26  # margin


def wrap(text, fnt, max_w):
    """Wrap text into lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 4


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 8], fill=NAVY)
centered(16, "THE WORLD IN ONE DAY", SERIF_B(56), NAVY)
centered(80, "One day's world news — in one picture", SANS(21), GREY)
# The date: the single most prominent line on the page.
centered(112, "SUNDAY, 22 NOVEMBER 2026", SANS_B(44), RED)
d.line([M, 172, W - M, 172], fill=INK, width=3)
d.line([M, 177, W - M, 177], fill=INK, width=1)

# ---------------------------------------------------------------- stories
# (kicker, headline, summary, accent colour, icon key)
STORIES = [
    ("CLIMATE  ·  ANTALYA",
     "Climate talks collapse with no deal",
     "COP31 ends in failure as nations split over naming fossil fuels.",
     (16, 96, 66), "globe"),
    ("POLITICS  ·  WASHINGTON",
     "Democrats win biggest House majority since 1992",
     "A North Carolina recount flips the last seat: 258 seats to 173.",
     (18, 44, 84), "capitol"),
    ("GULF  ·  STRAIT OF HORMUZ",
     "Two supertankers hit mines near Hormuz",
     "Iran says the ships struck mines; Trump weighs new strikes.",
     (140, 28, 28), "tanker"),
    ("LIBYA  ·  BENGHAZI",
     "Drone strike hits Russian warship in port",
     "Explosion and fire aboard the corvette Merkury at Benghazi base.",
     (96, 58, 120), "ship"),
    ("WAR  ·  KYIV",
     "Russian attack near Kyiv kills three",
     "A strike on an apartment building buries residents in rubble.",
     (122, 74, 18), "building"),
    ("TRAVEL  ·  UNITED STATES",
     "Delta outage delays 1,600+ flights",
     "A weight-and-balance system failure grounds planes for hours.",
     (16, 96, 130), "plane"),
]

GX, GY = M, 192
CW = (W - 2 * M - 2 * 14) // 3   # column width
CH = 352                          # panel height
GAP = 14


def burst(cx, cy, r1, r2, fill):
    for ang in range(0, 360, 30):
        r = r1 if ang % 60 == 0 else r2
        x2 = cx + r * math.cos(math.radians(ang))
        y2 = cy + r * math.sin(math.radians(ang))
        d.line([cx, cy, x2, y2], fill=fill, width=4)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 220, 90))


def icon_globe(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 232, 222))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 180))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(24, 24, 28), width=3)
    d.arc([cx - r, cy - r, cx + r, cy + r], 90, 270, fill=(255, 255, 255), width=3)
    d.ellipse([cx - 14, cy - r, cx + 14, cy + r], outline=(255, 255, 255), width=3)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=3)
    # crack across the globe
    d.line([(cx - 30, cy - 30), (cx - 8, cy - 6), (cx - 22, cy + 14),
            (cx + 2, cy + 30)], fill=(178, 34, 34), width=4)
    d.text((x0 + 8, y1 - 24), "NO DEAL", font=SANS_B(20), fill=(178, 34, 34))


def icon_capitol(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(222, 228, 240))
    cx = (x0 + x1) // 2
    base = y1 - 8
    # dome (kept inside the box: top at base-92)
    d.pieslice([cx - 36, base - 92, cx + 36, base - 24], 180, 360,
               fill=(240, 240, 240), outline=INK, width=2)
    d.rectangle([cx - 3, base - 102, cx + 3, base - 92], fill=INK)
    d.ellipse([cx - 5, base - 108, cx + 5, base - 98], fill=(200, 170, 30))
    # columns and base
    d.rectangle([cx - 52, base - 28, cx + 52, base], fill=(240, 240, 240),
                outline=INK, width=2)
    for i in range(-2, 3):
        px = cx + i * 20
        d.line([px, base - 62, px, base - 28], fill=INK, width=4)
    d.rectangle([cx - 60, base - 66, cx + 60, base - 58], fill=(240, 240, 240),
                outline=INK, width=2)


def icon_tanker(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(196, 216, 232))
    # sea
    d.rectangle([x0, y1 - 30, x1, y1], fill=(40, 90, 140))
    for wx in range(x0 + 6, x1 - 6, 26):
        d.arc([wx, y1 - 38, wx + 22, y1 - 22], 0, 180, fill=(255, 255, 255), width=3)
    # hull
    d.polygon([(x0 + 26, y1 - 62), (x1 - 26, y1 - 62), (x1 - 40, y1 - 34),
               (x0 + 40, y1 - 34)], fill=(140, 28, 28))
    # deck + bridge
    d.rectangle([x0 + 40, y1 - 84, x1 - 110, y1 - 62], fill=(60, 60, 60))
    d.rectangle([x1 - 104, y1 - 100, x1 - 60, y1 - 62], fill=(240, 240, 240))
    d.line([x1 - 82, y1 - 118, x1 - 82, y1 - 100], fill=INK, width=3)
    # explosion at the bow
    burst(x0 + 46, y0 + 30, 22, 13, (255, 140, 30))


def icon_ship(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 228, 240))
    # sea
    d.rectangle([x0, y1 - 26, x1, y1], fill=(52, 92, 130))
    # warship hull
    d.polygon([(x0 + 22, y1 - 56), (x1 - 30, y1 - 56), (x1 - 52, y1 - 30),
               (x0 + 40, y1 - 30)], fill=(90, 96, 104))
    d.rectangle([x0 + 96, y1 - 76, x1 - 96, y1 - 56], fill=(70, 76, 84))
    d.line([x1 - 66, y1 - 76, x1 - 66, y1 - 96], fill=INK, width=3)
    # drone above
    dx, dy = (x0 + x1) // 2, y0 + 26
    d.ellipse([dx - 16, dy - 8, dx + 16, dy + 8], fill=(40, 40, 40))
    d.line([dx - 30, dy - 6, dx + 30, dy - 6], fill=INK, width=3)
    d.line([dx - 30, dy + 6, dx + 30, dy + 6], fill=INK, width=3)
    # explosion amidships
    burst((x0 + x1) // 2, y1 - 52, 20, 12, (255, 140, 30))


def icon_building(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(28, 32, 58))
    base = y1 - 6
    heights = [46, 70, 54, 82, 60, 74]
    bw = (x1 - x0) // len(heights)
    for i, hh in enumerate(heights):
        bx = x0 + i * bw + 2
        d.rectangle([bx, base - hh, bx + bw - 4, base], fill=(52, 58, 92))
        for wy in range(base - hh + 8, base - 6, 14):
            d.rectangle([bx + 5, wy, bx + 10, wy + 6], fill=(240, 210, 110))
    burst(x1 - 34, y0 + 28, 22, 13, (255, 170, 40))
    d.line([x0 + 14, y0 + 16, x0 + 54, y0 + 40], fill=(255, 255, 255), width=3)


def icon_plane(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(222, 234, 244))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    # simple top-view plane
    d.ellipse([cx - 14, cy - 52, cx + 14, cy + 52], fill=(250, 250, 250),
              outline=INK, width=2)
    d.polygon([(cx - 52, cy - 6), (cx - 12, cy - 18), (cx - 12, cy + 6)],
              fill=(250, 250, 250), outline=INK)
    d.polygon([(cx + 12, cy - 18), (cx + 12, cy + 6), (cx + 52, cy - 6)],
              fill=(250, 250, 250), outline=INK)
    d.polygon([(cx - 8, cy + 44), (cx + 8, cy + 44), (cx + 4, cy + 62),
               (cx - 4, cy + 62)], fill=(250, 250, 250), outline=INK)
    for wy in range(cy - 38, cy + 40, 14):
        d.ellipse([cx - 4, wy, cx + 4, wy + 6], fill=NAVY)
    # clock: delayed
    d.ellipse([x1 - 52, y1 - 52, x1 - 10, y1 - 10], fill=(255, 255, 255),
              outline=RED, width=3)
    d.line([x1 - 31, y1 - 31, x1 - 31, y1 - 44], fill=RED, width=3)
    d.line([x1 - 31, y1 - 31, x1 - 20, y1 - 26], fill=RED, width=3)


ICONS = {"globe": icon_globe, "capitol": icon_capitol, "tanker": icon_tanker,
         "ship": icon_ship, "building": icon_building, "plane": icon_plane}

for idx, (kicker, headline, summary, accent, icon) in enumerate(STORIES):
    col, row = idx % 3, idx // 3
    x = GX + col * (CW + GAP)
    y = GY + row * (CH + GAP)
    # panel card
    d.rectangle([x, y, x + CW, y + CH], fill=(255, 255, 255),
                outline=RULE, width=2)
    d.rectangle([x, y, x + CW, y + 5], fill=accent)
    # kicker
    d.text((x + 12, y + 14), kicker, font=SANS_B(17), fill=accent)
    # icon box
    ib = (x + 12, y + 42, x + CW - 12, y + 152)
    d.rectangle(ib, fill=(238, 234, 224), outline=RULE, width=1)
    ICONS[icon](ib)
    # headline
    hy = y + 164
    for line in wrap(headline, SANS_B(24), CW - 24):
        d.text((x + 12, hy), line, font=SANS_B(24), fill=INK)
        hy += 29
    # summary
    sy = hy + 6
    for line in wrap(summary, SANS(18), CW - 24):
        d.text((x + 12, sy), line, font=SANS(18), fill=BODY)
        sy += 23

# ---------------------------------------------------------------- footer
fy = GY + 2 * CH + GAP + 8
d.line([M, fy, W - M, fy], fill=INK, width=2)
footer = ("ALSO TODAY:  Settlers torch vehicles and homes in West Bank villages  ·  "
          "Europe's cost-of-living protests enter a third day  ·  Thousands march "
          "in Istanbul over the seizure of Sözcü TV")
for line in wrap(footer, SANS_B(18), W - 2 * M):
    d.text((M, fy + 10), line, font=SANS_B(18), fill=NAVY)
    fy += 24
d.text((M, H - 26),
       "Sources: AP, KPFA, dpa-AFX, Public Radio East, Daily Summary of World.",
       font=SANS(14), fill=GREY)

out = os.path.join(HERE, "entry.png")
img.save(out, "PNG", optimize=True)
print(out, img.size, os.path.getsize(out), "bytes")
