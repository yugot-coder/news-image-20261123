#!/usr/bin/env python3
"""Render the 23 November 2026 news poster (1024x1024 PNG).

Written from scratch for the news-image-20261123 edition. All facts come
from NEWS-RESEARCH-20261123.md. Pillow is only needed here; the shipped
main.py is pure stdlib and just copies the rendered entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))

PAPER = (247, 242, 232)
INK = (20, 24, 31)
INK_SOFT = (74, 80, 92)
RED = (178, 39, 30)
BLUE = (29, 78, 137)
GOLD = (176, 124, 24)
CARD = (255, 253, 247)
LINE = (196, 186, 168)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, color, max_w, leading):
    """Draw wrapped paragraph, return y just below the last line."""
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, y, x1, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- data
HEROES = [
    {
        "kicker": "DELHI  •  DIPLOMACY",
        "color": BLUE,
        "head": "Shah meets Modi as Nepal opens its first state visit",
        "body": "Delegation talks in Delhi on Monday: MoUs on education, health, "
                "agriculture and energy, plus a joint press conference. "
                "Shah also calls on President Murmu and visits Rajghat.",
    },
    {
        "kicker": "SERANG  •  RESCUE",
        "color": RED,
        "head": "Search resumes at 07:00 in the Cikande candy factory fire",
        "body": "24 body bags were recovered on Sunday; about 29 workers are still "
                "missing and 8 unaccounted for. DNA identification takes two "
                "to three weeks; the fire began in a cooling unit.",
    },
    {
        "kicker": "WELLINGTON  •  CRICKET",
        "color": GOLD,
        "head": "India 720/9 declared — the final day belongs to New Zealand",
        "body": "A record total in New Zealand, with Rahul 136 and Pant 128. The "
                "hosts closed on 119/2, still 233 behind, with Conway 59 "
                "not out as the Test reaches its final day.",
    },
]

STATS = [
    ("720/9", "India's record total\nin New Zealand"),
    ("24", "body bags recovered\nin Serang on Sunday"),
    ("14–15", "missing in Dymer,\nincluding 2 children"),
    ("194", "parties at COP31 —\nno fossil-fuel text"),
    ("2,700", "drones launched by\nRussia in one week"),
    ("−5.3%", "Nasdaq's week —\nworst since 2020"),
]

# (place, day-tag, headline, subline)
CARDS = [
    ("DYMER", "MON", "Rescue goes on in Dymer after the drone strike",
     "1–2 dead, 14–15 missing in Dymer."),
    ("CLIMATE", "MON", "The morning after COP31 collapsed",
     "Guterres disappointed; COP32 next."),
    ("BALTIC", "MON", "Russian freighter Sparta II still burning",
     "Hit by two drones; fire may last days."),
    ("ASEAN", "SAT", "Myanmar calls the Manila summit 'unfair'",
     "Naypyidaw rejects the Manila outcome."),
    ("MARKETS", "FRI", "Wall Street slides into Monday",
     "Nasdaq −5.3%; Nvidia down 14%."),
    ("DELHI", "MON", "Shah meets President Murmu, visits Rajghat",
     "Audience with Murmu; Rajghat."),
    ("EUROPE", "MON", "India–Bulgaria talk ties, IMEC, Black Sea",
     "Bilateral talks on the Delhi sidelines."),
    ("INDIA", "MON", "Shah pushes ₹4,000 crore for Arunachal",
     "Infra drive for the north-eastern state."),
    ("INDIA", "MON", "Rajya Sabha MP Ramrao Wadkute dies",
     "BJP member's heart attack in Delhi."),
    ("INDIA", "MON", "Nine pilgrims killed in Kota crash",
     "Vehicle hit a truck in Rajasthan."),
    ("INDIA", "MON", "Hyderabad students protest",
     "Students demand lecturer dismissed."),
    ("INDIA", "MON", "Kashmir saffron fields used as a dump",
     "Fields served as a tip for three years."),
    ("CINEMA", "MON", "IFFI 2026 hosts a BRICS roundtable",
     "Film festival gathering in Goa."),
    ("SPORT", "MON", "Anupama keeps her world snooker crown",
     "Defends the IBSF World Women's title."),
    ("SPORT", "MON", "World chess championship in focus",
     "Feature coverage of the title match."),
    ("SPORT", "SUN", "Jurel's 78 caps India's 720/9",
     "Six other fifty-makers in the 720/9."),
    ("USA", "FRI", "FBI crime database hacked, Trump says 'not good'",
     "Breach of the NCIC system reported."),
    ("GENEVA", "SAT", "Killer-robot talks end with no binding rules",
     "Two more years of talks in Geneva."),
    ("EUROPE", "SAT", "Thousands march in Lisbon in heavy rain",
     "CGTP rally; inflation 3.8%."),
    ("SEOUL", "SUN", "South Korea's finance minister resigns",
     "Quits over AI exam scandal."),
    ("MEXICO", "FRI", "El Chapo Isidro captured in Guasave",
     "FBI Top-10 fugitive taken; 11 killed."),
    ("GULF", "SAT", "Iran claims strike on Bahrain Patriot site",
     "IRGC claim; two people hurt at Al-Riffa."),
    ("GULF", "FRI–SAT", "Saudi coalition intercepts Houthi missiles",
     "Missiles aimed at Riyadh downed."),
    ("TECH", "MON", "The Nvidia chip-smuggling network",
     "FT traces H-series chips reaching China."),
    ("USA", "MON", "Waymo still grounded nationwide",
     "DMV ban stands; pause since mid-Nov."),
    ("INDIA", "MON", "Six sent to juvenile home after Mumbai assault",
     "Six sent to juvenile home in Mumbai."),
    ("EUROPE", "TUE", "Portugal's budget vote looms",
     "Parliament votes Tuesday."),
]

# Dot-matrix map: rough continent blobs as ellipses in map coords.
# Map inner area in pixels: 584 wide x 96 tall (dots step 12).
BLOBS = [
    # (cx, cy, rx, ry) in 0..584 x 0..96 map space
    (70, 52, 62, 36),    # North America
    (128, 84, 32, 14),   # Central America
    (182, 70, 24, 24),   # South America
    (298, 34, 32, 22),   # Europe
    (318, 66, 40, 28),   # Africa
    (428, 40, 88, 30),   # Asia
    (516, 86, 28, 12),   # Oceania
]
# (label, px, py, label_dx, label_dy) — label offset keeps text in-bounds
PINS = [
    ("Helsinki", 312, 12, 8, -6),
    ("Dymer", 316, 30, 8, -6),
    ("Lisbon", 284, 50, 8, -6),
    ("Antalya", 340, 46, 8, -6),
    ("Riyadh", 368, 64, 8, -6),
    ("Delhi", 442, 54, 8, -6),
    ("Seoul", 508, 44, 8, -6),
    ("Serang", 488, 88, -52, -6),
    ("Wellington", 556, 90, -72, -6),
]

DATE_CHECK = (
    "DATE CHECK — Monday is only hours old, so verified all-Monday news "
    "is still thin. The three leads are confirmed Monday events: the "
    "Shah–Modi talks, the 07:00 Serang search, the final day in "
    "Wellington. Weekend items are marked SAT / SUN / FRI — context "
    "only, never presented as 23 Nov news."
)


# ---------------------------------------------------------------- draw
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Frame
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([22, 22, W - 23, H - 23], outline=LINE, width=1)

    # ---- Masthead
    d.text((W // 2, 34), "THE DAILY ORBIT", font=font(SERIF, 56),
           fill=INK, anchor="ma")
    rule(d, 60, 108, W - 60, RED, 3)
    d.text((W // 2, 118), "MONDAY 23 NOVEMBER 2026   •   30 STORIES   •   ONE PAGE",
           font=font(SANS_B, 15), fill=INK_SOFT, anchor="ma")

    # ---- Hero row: three columns
    hx, hy, hw, hh, gap = 40, 146, 304, 190, 16
    for i, hero in enumerate(HEROES):
        x = hx + i * (hw + gap)
        d.rounded_rectangle([x, hy, x + hw, hy + hh], radius=6,
                            fill=CARD, outline=LINE, width=1)
        d.rectangle([x, hy, x + hw, hy + 6], fill=hero["color"])
        y = hy + 18
        d.text((x + 14, y), hero["kicker"], font=font(SANS_B, 12),
               fill=hero["color"])
        y += 22
        y = para(d, (x + 14, y), hero["head"], font(SANS_B, 19), INK,
                 hw - 28, 22)
        y += 6
        para(d, (x + 14, y), hero["body"], font(SANS, 12), INK_SOFT,
             hw - 28, 15)

    # ---- Stats strip
    sy, sh = 348, 72
    sw = (W - 80 - 5 * 10) / 6
    for i, (num, label) in enumerate(STATS):
        x = 40 + i * (sw + 10)
        d.rounded_rectangle([x, sy, x + sw, sy + sh], radius=6,
                            fill=INK, outline=INK)
        d.text((x + sw / 2, sy + 8), num, font=font(SANS_B, 24),
               fill=(255, 255, 255), anchor="ma")
        for j, line in enumerate(label.split("\n")):
            d.text((x + sw / 2, sy + 40 + j * 13), line,
                   font=font(SANS, 10), fill=(214, 210, 198), anchor="ma")

    # ---- Dot-matrix map
    mx0, my0, mx1, my1 = 40, 450, 640, 570
    d.text((mx0, 430), "WHERE IT HAPPENED — 9 PINS",
           font=font(SANS_B, 12), fill=INK)
    d.rounded_rectangle([mx0, my0, mx1, my1], radius=6,
                        fill=CARD, outline=LINE, width=1)
    ox, oy = mx0 + 8, my0 + 8
    for gx in range(0, 584, 12):
        for gy in range(0, 96, 12):
            inside = any(((gx - cx) / rx) ** 2 + ((gy - cy) / ry) ** 2 <= 1
                         for cx, cy, rx, ry in BLOBS)
            if inside:
                d.ellipse([ox + gx - 2, oy + gy - 2, ox + gx + 2, oy + gy + 2],
                          fill=(150, 158, 172))
    for name, px, py, ldx, ldy in PINS:
        cx, cy = ox + px, oy + py
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((cx + ldx, cy + ldy), name, font=font(SANS_B, 10), fill=RED)

    # ---- Date check box
    bx0, by0, bx1, by1 = 664, 450, 984, 570
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=6,
                        fill=(255, 244, 224), outline=GOLD, width=2)
    d.text((bx0 + 14, by0 + 12), "DATE CHECK", font=font(SANS_B, 13),
           fill=GOLD)
    para(d, (bx0 + 14, by0 + 34), DATE_CHECK, font(SANS, 11),
         INK_SOFT, bx1 - bx0 - 28, 14)

    # ---- Cards grid: 3 columns x 9 rows
    rule(d, 40, 582, W - 40, INK, 2)
    d.text((40, 590), "THE REST OF THE DAY — 27 MORE STORIES",
           font=font(SANS_B, 13), fill=INK)
    d.text((W - 40, 590), "4–30", font=font(SANS_B, 13), fill=RED,
           anchor="ra")
    cw = 304
    gy0 = 614
    head_f = font(SANS_B, 11)
    sub_f = font(SANS, 10)
    tag_f = font(SANS_B, 9)
    for i, (place, day, head, sub) in enumerate(CARDS):
        col, row = i % 3, i // 3
        x = 40 + col * (cw + 16)
        y = gy0 + row * 40
        d.text((x, y), f"{i + 4:>2}.", font=font(SANS_B, 11), fill=RED)
        tx = x + 26
        # Headline, wrapped to at most 2 lines inside the column.
        lines = wrap(d, head, head_f, cw - 26)[:2]
        for j, line in enumerate(lines):
            d.text((tx, y + j * 13), line, font=head_f, fill=INK)
        # Subline: place/day tag first, then the summary, truncated.
        sy2 = y + len(lines) * 13 + 2
        tag_txt = f"{place} · {day}  "
        d.text((tx, sy2), tag_txt, font=tag_f, fill=RED)
        tag_w = d.textlength(tag_txt, font=tag_f)
        avail = cw - 26 - tag_w
        shown = sub
        while shown and d.textlength(shown + "…", font=sub_f) > avail:
            shown = shown[:-1]
        if shown != sub:
            shown += "…"
        d.text((tx + tag_w, sy2), shown, font=sub_f, fill=INK_SOFT)

    # ---- Footer
    rule(d, 40, 984, W - 40, LINE, 1)
    d.text((40, 990), "THE DAILY ORBIT — drawn from verified wire reporting; "
                        "weekend items are marked with their day.",
           font=font(SANS, 10), fill=INK_SOFT)

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
