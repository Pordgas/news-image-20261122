#!/usr/bin/env python3
"""Draw the 22 November 2026 front page: 'THE WORLD IN ONE DAY'.

Fresh implementation (rewritten from the BUILD-NOTES spec and the target
image). Uses only PIL + the DejaVu fonts shipped with the system. The
picture is 1024x1024 and is written to entry.png next to this script.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

CANVAS_W, CANVAS_H = 1024, 1024

CREAM = (248, 243, 228)
INK = (22, 22, 22)
NAVY = (24, 38, 77)
RED = (176, 30, 30)
GREY = (84, 84, 84)
PANEL_BG = (255, 255, 255)
PANEL_EDGE = (198, 190, 170)

SERIF = FONT_DIR / "DejaVuSerif-Bold.ttf"
SERIF_REG = FONT_DIR / "DejaVuSerif.ttf"
SANS = FONT_DIR / "DejaVuSans.ttf"
SANS_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(str(path), size)


def split_lines(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def starburst(draw, cx, cy, outer, inner, spikes, color):
    """A simple explosion star: alternating outer/inner points."""
    pts = []
    for i in range(spikes * 2):
        radius = outer if i % 2 == 0 else inner
        angle = math.pi * i / spikes - math.pi / 2
        pts.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    draw.polygon(pts, fill=color)


def art_globe(draw, box):
    """Blue globe with a red crack and a NO DEAL label."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(220, 234, 217))
    cx, cy = (x0 + x1) // 2 - 10, (y0 + y1) // 2
    r = 42
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 110, 180),
                 outline=(255, 255, 255), width=3)
    draw.ellipse([cx - 16, cy - r, cx + 16, cy + r], outline=(255, 255, 255), width=2)
    draw.line([x0 + 8, cy, x1 - 8, cy], fill=(255, 255, 255), width=2)
    draw.line([cx - 34, cy - 26, cx + 6, cy - 4, cx - 8, cy + 12, cx + 26, cy + 34],
              fill=(200, 30, 30), width=4)
    label = font(SANS_BOLD, 20)
    draw.text((x0 + 10, y1 - 30), "NO DEAL", font=label, fill=(200, 30, 30))


def art_capitol(draw, box):
    """White domed capitol on a pale lavender field."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(228, 230, 245))
    cx = (x0 + x1) // 2
    base_y = y1 - 12
    # dome (kept short so the finial stays inside the picture box)
    draw.pieslice([cx - 52, base_y - 86, cx + 52, base_y - 4],
                  start=180, end=360, fill=(255, 255, 255), outline=(90, 90, 90))
    draw.ellipse([cx - 5, base_y - 96, cx + 5, base_y - 86], fill=(212, 175, 55))
    draw.line([cx, base_y - 86, cx, base_y - 82], fill=(90, 90, 90), width=2)
    # drum + columns
    draw.rectangle([cx - 46, base_y - 58, cx + 46, base_y - 8],
                   fill=(255, 255, 255), outline=(90, 90, 90))
    for off in (-32, -16, 0, 16, 32):
        draw.line([cx + off, base_y - 54, cx + off, base_y - 12],
                  fill=(120, 120, 120), width=3)
    # steps
    draw.rectangle([cx - 62, base_y - 8, cx + 62, base_y], fill=(235, 235, 235),
                   outline=(90, 90, 90))


def art_tanker(draw, box):
    """Red supertanker on a blue sea, explosion at the bow."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(215, 230, 242))
    sea_y = y1 - 26
    draw.rectangle([x0, sea_y, x1, y1], fill=(38, 84, 140))
    for wx in range(x0 + 14, x1 - 6, 26):
        draw.arc([wx - 8, sea_y - 4, wx + 8, sea_y + 10], start=180, end=360,
                 fill=(255, 255, 255), width=2)
    # hull: dark deck over a red trapezoid hull
    draw.polygon([(x0 + 52, sea_y - 34), (x1 - 40, sea_y - 34),
                  (x1 - 66, sea_y + 2), (x0 + 78, sea_y + 2)],
                 fill=(176, 32, 32))
    draw.rectangle([x0 + 52, sea_y - 52, x1 - 40, sea_y - 34], fill=(58, 58, 58))
    draw.rectangle([x1 - 96, sea_y - 74, x1 - 56, sea_y - 52], fill=(240, 240, 240))
    draw.line([x1 - 76, sea_y - 92, x1 - 76, sea_y - 74], fill=(40, 40, 40), width=3)
    starburst(draw, x0 + 42, sea_y - 44, 22, 9, 8, (255, 196, 0))


def art_warship(draw, box):
    """Grey warship with a mid-ship blast, dark sea below."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(219, 232, 242))
    sea_y = y1 - 24
    draw.rectangle([x0, sea_y, x1, y1], fill=(44, 84, 128))
    # hull
    draw.polygon([(x0 + 34, sea_y - 22), (x1 - 30, sea_y - 22),
                  (x1 - 58, sea_y + 4), (x0 + 62, sea_y + 4)], fill=(96, 104, 112))
    # superstructure + mast
    draw.rectangle([x0 + 118, sea_y - 52, x0 + 186, sea_y - 22], fill=(70, 78, 86))
    draw.rectangle([x0 + 140, sea_y - 64, x0 + 164, sea_y - 52], fill=(52, 58, 64))
    draw.line([x1 - 52, sea_y - 66, x1 - 52, sea_y - 22], fill=(40, 40, 40), width=3)
    starburst(draw, x0 + 152, sea_y - 30, 24, 10, 8, (255, 196, 0))


def art_skyline(draw, box):
    """Night skyline with lit windows, a missile trail and a blast."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(28, 36, 64))
    towers = [(8, 44, 34), (52, 26, 40), (104, 52, 30), (146, 32, 44),
              (200, 58, 30), (240, 40, 36)]
    for tx, top, tw in towers:
        draw.rectangle([x0 + tx, y0 + top, x0 + tx + tw, y1],
                       fill=(48, 56, 92))
        for wy in range(y0 + top + 8, y1 - 8, 16):
            for wx in (x0 + tx + 7, x0 + tx + tw - 13):
                draw.rectangle([wx, wy, wx + 5, wy + 6], fill=(255, 214, 90))
    draw.line([x0 + 16, y0 + 18, x0 + 74, y0 + 44], fill=(255, 255, 255), width=2)
    starburst(draw, x1 - 34, y0 + 30, 22, 9, 8, (255, 196, 0))


def art_plane(draw, box):
    """Top-down airliner with a red clock at the right."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(217, 233, 244))
    cx, cy = (x0 + x1) // 2 - 30, (y0 + y1) // 2
    # fuselage
    draw.ellipse([cx - 16, y0 + 8, cx + 16, y1 - 8], fill=(255, 255, 255),
                 outline=(120, 130, 140))
    # swept wings on both sides + tail fins
    draw.polygon([(cx - 12, cy - 8), (cx - 12, cy + 10), (cx - 74, cy + 30),
                  (cx - 74, cy + 8)], fill=(235, 238, 242), outline=(120, 130, 140))
    draw.polygon([(cx + 12, cy - 8), (cx + 12, cy + 10), (cx + 74, cy + 30),
                  (cx + 74, cy + 8)], fill=(235, 238, 242), outline=(120, 130, 140))
    draw.polygon([(cx - 12, y1 - 18), (cx - 12, y1 - 8), (cx - 34, y1 - 30),
                  (cx - 34, y1 - 40)], fill=(235, 238, 242), outline=(120, 130, 140))
    draw.polygon([(cx + 12, y1 - 18), (cx + 12, y1 - 8), (cx + 34, y1 - 30),
                  (cx + 34, y1 - 40)], fill=(235, 238, 242), outline=(120, 130, 140))
    for wy in range(y0 + 26, y1 - 22, 14):
        draw.ellipse([cx - 4, wy, cx + 4, wy + 7], fill=(40, 70, 110))
    # clock
    ccx, ccy, cr = x1 - 34, y1 - 32, 20
    draw.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], outline=(176, 30, 30),
                 width=3, fill=(255, 255, 255))
    draw.line([ccx, ccy, ccx, ccy - 11], fill=(176, 30, 30), width=2)
    draw.line([ccx, ccy, ccx + 9, ccy + 4], fill=(176, 30, 30), width=2)


PANELS = [
    dict(kicker="CLIMATE · ANTALYA", accent=(23, 114, 69), art_bg=None,
         art=art_globe,
         headline="Climate talks collapse with no deal",
         standfirst="COP31 ends in failure as nations split over naming fossil fuels."),
    dict(kicker="POLITICS · WASHINGTON", accent=(31, 58, 110), art_bg=None,
         art=art_capitol,
         headline="Democrats win biggest House majority since 1992",
         standfirst="A North Carolina recount flips the last seat: 258 seats to 173."),
    dict(kicker="GULF · STRAIT OF HORMUZ", accent=(142, 31, 31), art_bg=None,
         art=art_tanker,
         headline="Two supertankers hit mines near Hormuz",
         standfirst="Iran says the ships struck mines; Trump weighs new strikes."),
    dict(kicker="LIBYA · BENGHAZI", accent=(94, 42, 132), art_bg=None,
         art=art_warship,
         headline="Drone strike hits Russian warship in port",
         standfirst="Explosion and fire aboard the corvette Merkury at Benghazi base."),
    dict(kicker="WAR · KYIV", accent=(122, 74, 18), art_bg=None,
         art=art_skyline,
         headline="Russian attack near Kyiv kills three",
         standfirst="A strike on an apartment building buries residents in rubble."),
    dict(kicker="TRAVEL · UNITED STATES", accent=(15, 106, 122), art_bg=None,
         art=art_plane,
         headline="Delta outage delays 1,600+ flights",
         standfirst="A weight-and-balance system failure grounds planes for hours."),
]

FOOTER_TEXT = (
    "ALSO TODAY: Settlers torch vehicles and homes in West Bank villages · "
    "Europe's cost-of-living protests enter a third day · Thousands march in "
    "Istanbul over the seizure of Sözcü TV"
)
SOURCES_TEXT = "Sources: AP, KPFA, dpa-AFX, Public Radio East, Daily Summary of World."


def draw_panel(draw, x, y, spec):
    """One story panel: accent bar, kicker, picture, headline, standfirst."""
    w, h = 316, 336
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=PANEL_EDGE, width=1)
    draw.rectangle([x, y, x + w, y + 7], fill=spec["accent"])
    kick_font = font(SANS_BOLD, 18)
    draw.text((x + 12, y + 15), spec["kicker"], font=kick_font, fill=spec["accent"])
    spec["art"](draw, (x + 12, y + 44, x + w - 12, y + 152))
    head_font = font(SANS_BOLD, 24)
    sub_font = font(SANS, 18)
    lines = split_lines(draw, spec["headline"], head_font, w - 24)
    ty = y + 164
    for line in lines:
        draw.text((x + 12, ty), line, font=head_font, fill=INK)
        ty += 29
    ty += 4
    for line in split_lines(draw, spec["standfirst"], sub_font, w - 24):
        draw.text((x + 12, ty), line, font=sub_font, fill=(63, 63, 63))
        ty += 22


def build_page():
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), CREAM)
    draw = ImageDraw.Draw(canvas)

    # Top navy strip.
    draw.rectangle([0, 0, CANVAS_W, 12], fill=NAVY)

    # Masthead.
    title_font = font(SERIF, 62)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=title_font)
    draw.text(((CANVAS_W - tw) / 2, 30), title, font=title_font, fill=NAVY)
    tag_font = font(SERIF_REG, 23)
    tag = "One day's world news — in one picture"
    tw = draw.textlength(tag, font=tag_font)
    draw.text(((CANVAS_W - tw) / 2, 102), tag, font=tag_font, fill=GREY)
    date_font = font(SERIF, 44)
    date = "SUNDAY, 22 NOVEMBER 2026"
    tw = draw.textlength(date, font=date_font)
    draw.text(((CANVAS_W - tw) / 2, 132), date, font=date_font, fill=RED)
    draw.line([24, 190, CANVAS_W - 24, 190], fill=NAVY, width=2)
    draw.line([24, 195, CANVAS_W - 24, 195], fill=NAVY, width=1)

    # Story grid: 3 columns x 2 rows.
    for i, spec in enumerate(PANELS):
        col, row = i % 3, i // 3
        px = 24 + col * (316 + 14)
        py = 210 + row * (336 + 14)
        draw_panel(draw, px, py, spec)

    # Footer strip.
    draw.line([24, 908, CANVAS_W - 24, 908], fill=NAVY, width=2)
    foot_font = font(SANS_BOLD, 19)
    fy = 918
    for line in split_lines(draw, FOOTER_TEXT, foot_font, CANVAS_W - 48):
        draw.text((24, fy), line, font=foot_font, fill=NAVY)
        fy += 24
    src_font = font(SANS, 15)
    draw.text((24, 988), SOURCES_TEXT, font=src_font, fill=GREY)

    return canvas


if __name__ == "__main__":
    page = build_page()
    out = HERE / "entry.png"
    page.save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
