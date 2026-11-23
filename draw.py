#!/usr/bin/env python3
"""news-image-20261123 — 'THE DAILY ORBIT': Monday 23 November 2026 in one image.

Dense broadsheet-style news poster drawn with Pillow. Fully deterministic:
no randomness, no timestamps, no network. Fonts are resolved from the
system Noto directory (the 20261122 build used the same). Output:
$MAKEFUN_OUTPUT_DIR/entry.png when that variable is set, else
/output/entry.png when /output exists, otherwise entry.png next to this
file. 1024x1024, < 1 MiB.

DATE DISCIPLINE: Monday 23 November 2026 is barely under way at build
time (07:30 WIB), so the lead stories are Monday's own events and
Monday developments of weekend stories: the Shah–Modi talks in Delhi,
the search resuming at dawn in Serang, the final day in Wellington.
Weekend stories are tagged SAT/SUN/FRI in their cards and appear only
as Monday's context. Every figure below was cross-checked against wire
reports (Reuters, AP, BBC, UN News, ESPNcricinfo) on 23 Nov 2026.
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants
W, H = 1024, 1024
M = 24                      # page margin
CW = W - 2 * M              # content width

PAPER = (247, 243, 233)
PANEL = (253, 251, 245)
INK = (26, 24, 20)
GRAY = (88, 82, 72)
HAIR = (168, 160, 144)
RED = (178, 30, 30)
DRED = (138, 20, 20)
NAVY = (24, 42, 74)
GREEN = (22, 92, 54)
GOLD = (146, 108, 20)

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIRS = (os.path.join(HERE, "fonts"), "/usr/share/fonts/truetype/noto")
SERIF_BLACK = "NotoSerifDisplay-Black.ttf"
SERIF_XB = "NotoSerifDisplay-ExtraBold.ttf"
SERIF_B = "NotoSerifDisplay-Bold.ttf"
SANS_CB = "NotoSans-CondensedBold.ttf"
SANS_CSB = "NotoSans-CondensedSemiBold.ttf"
SANS_CM = "NotoSans-CondensedMedium.ttf"
SANS_C = "NotoSans-Condensed.ttf"

_cache = {}


def F(name, size):
    key = (name, size)
    if key not in _cache:
        font = None
        for d in FONT_DIRS:
            p = os.path.join(d, name)
            if os.path.isfile(p):
                font = ImageFont.truetype(p, size)
                break
        if font is None:
            font = ImageFont.load_default()
        _cache[key] = font
    return _cache[key]


# ---------------------------------------------------------------- helpers
def tw(d, text, font):
    return d.textlength(text, font=font)


def fit(d, text, path, max_w, start, floor=8):
    """Largest font size <= start whose text fits max_w."""
    s = start
    while s > floor and tw(d, text, F(path, s)) > max_w:
        s -= 1
    return F(path, s)


def tracked(d, xy, text, font, fill, track=2):
    """Draw letterspaced text; returns total width."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += tw(d, ch, font) + track
    return x - track - xy[0]


def tracked_w(d, text, font, track=2):
    return sum(tw(d, ch, font) for ch in text) + track * (len(text) - 1)


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(d, xy, text, font, fill, max_w, leading, max_lines=None):
    """Draw wrapped text; returns y after the block."""
    x, y = xy
    lines = wrap(d, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def rule(d, x0, x1, y, fill=INK, wdt=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


# ---------------------------------------------------------------- content
RED_STRIP = ("SHAH MEETS MODI IN DELHI  \u2022  SEARCH RESUMES IN SERANG  "
             "\u2022  FINAL DAY IN WELLINGTON")

STATS = [
    ("720/9", "INDIA\u2019S RECORD TOTAL IN NZ\nHIGHEST EVER ON NZ SOIL"),
    ("24", "BODY BAGS REMOVED FROM\nTHE SERANG FACTORY RUINS"),
    ("14", "STILL MISSING IN DYMER\nAFTER SUNDAY\u2019S DRONE HIT"),
    ("194", "COP31 PARTIES, NO DEAL\nLONGEST CLIMATE SUMMIT EVER"),
    ("2", "DAYS OF COP31 OVERTIME\nBEFORE THE PACT COLLAPSED"),
    ("35%", "ELECTRIFICATION TARGET\n\u201835 BY 35\u2019 SURVIVES THE WRECK"),
]

HEROES = [
    dict(
        accent=NAVY, kick="NEW DELHI \u2022 NEPAL\u2013INDIA \u2022 MONDAY",
        head="SHAH & MODI TALK TRADE, ENERGY AND TIES",
        body=("Nepal PM Balendra Shah holds delegation-level talks with PM "
              "Narendra Modi in Delhi on Monday \u2014 his first bilateral "
              "trip abroad since taking office in March. MoUs on education, "
              "health, agriculture and energy, a joint press conference and "
              "a luncheon hosted by Modi. Shah also calls on President "
              "Murmu and lays a wreath at Rajghat."),
        foot="34-member delegation \u2022 State visit 22\u201323 Nov",
    ),
    dict(
        accent=DRED, kick="SERANG, BANTEN \u2022 INDONESIA \u2022 MONDAY",
        head="SEARCH RESUMES AT DAWN IN THE FACTORY RUINS",
        body=("Rescue crews return at 7 a.m. Monday to the PT Fonusa Agung "
              "Mulia candy factory in Cikande, where a fire broke out "
              "Saturday at 5 p.m. with 300 workers inside. Police removed "
              "24 body bags on Sunday; the factory says 29 are still "
              "missing and 8 unaccounted for. DNA identification may take "
              "two to three weeks."),
        foot="Flames \u2018began in a cooling unit\u2019, survivors say",
    ),
    dict(
        accent=GREEN, kick="WELLINGTON \u2022 CRICKET \u2022 FINAL DAY",
        head="INDIA\u2019S 720 SETS UP A FINAL-DAY FINISH",
        body=("India declared on a record 720 for 9 \u2014 the highest Test "
              "total ever in New Zealand, with the first seven partnerships "
              "all passing 50 for the first time in Test history. Rahul "
              "136, Pant 128. New Zealand closed on 119 for 2, still 233 "
              "behind, with one day left to save the match."),
        foot=None,  # top-score bars instead
    ),
]

BARS = [("RAHUL", 136), ("PANT", 128), ("GILL", 98), ("JAISWAL", 85),
        ("PADIKKAL", 80), ("JUREL", 78)]

CARDS = [
    ("DYMER RESCUE GOES ON",
     "2 dead, 14\u201315 missing incl. 2 children after Sunday\u2019s drone hit; Zelensky renews his plea for Patriot interceptors."),
    ("COP31: THE DAY AFTER",
     "Guterres \u2018deeply disappointed\u2019; focus shifts to COP32 in Addis Ababa after the EU and UK rejected a text with no fossil-fuel mention."),
    ("SPARTA II STILL SMOULDERS",
     "Baltic blaze cooling into Monday; 16 crew evacuated, 1 hurt; the sanctioned ship lies at anchor in Finnish waters."),
    ("MYANMAR WEIGHS ASEAN TIES (SAT)",
     "Junta calls summit exclusion \u2018unfair and imbalanced\u2019 days after the ICJ found it guilty of genocide against the Rohingya."),
    ("WALL ST LIMPS INTO MONDAY",
     "After the Nasdaq\u2019s worst week since 2020 (\u22125.3%): S&P \u22123.7%, seven straight down days, Nvidia \u221214%."),
    ("SHAH CALLS ON MURMU",
     "Nepal PM meets President Droupadi Murmu and External Affairs Minister Jaishankar during his Delhi stay."),
    ("INDIA\u2013BULGARIA TALKS",
     "Delhi discusses bilateral ties, the IMEC corridor and the Black Sea situation with Sofia."),
    ("SHAH\u2019S \u20b94,000-CR PUSH",
     "Home minister launches a \u20b94,000-crore infrastructure push in Arunachal Pradesh."),
    ("MP WADKUTE DIES",
     "BJP Rajya Sabha MP Ramrao Wadkute dies of cardiac arrest in Delhi."),
    ("RAJASTHAN PILGRIM CRASH",
     "9 killed as a vehicle carrying pilgrims rams a truck in Kota."),
    ("HYDERABAD STUDENTS PROTEST",
     "University students demand a faculty sacking over alleged casteist remarks."),
    ("KASHMIR SAFFRON FIELDS",
     "Saffron fields used as dumping grounds for three years, Mehbooba Mufti says."),
    ("IFFI BRICS ROUNDTABLE",
     "Goa film festival hosts a BRICS roundtable to boost industry ties."),
    ("SNOOKER: ANUPAMA DEFENDS",
     "Anupama retains the IBSF World Women\u2019s Snooker crown."),
    ("CHESS: GENIUSES AT WORK",
     "World championship coverage: \u2018geniuses who wielded their magic\u2019."),
    ("JUREL SEES A CHANCE",
     "India keep hope alive on a slowing Basin Reserve pitch, day four reports say."),
    ("FBI PROBES NCIC BREACH (FRI)",
     "FBI investigates an apparent hack of the US national crime database; Trump: \u2018not good\u2019."),
    ("KILLER-ROBOT TALKS FALTER (SAT)",
     "UN Geneva talks end with two more years of talks, no binding rules on lethal autonomous weapons."),
    ("LISBON MARCHES ON (SAT)",
     "Thousands brave rain over living costs and housing; CGTP plans a parliament rally on 24 Nov."),
    ("SEOUL MINISTER QUITS (SUN)",
     "Education chief Choi Kyo-jin resigns over AI exam-cheating chaos; 111 cases caught in the CSAT."),
    ("EL CHAPO ISIDRO HELD (FRI)",
     "FBI Top-10 fugitive captured in Guasave; 11 dead \u2014 7 gunmen, 4 soldiers \u2014 in the firefights."),
    ("IRAN HITS BAHRAIN BASES (SAT)",
     "IRGC claims missile-drone strikes on US Patriot sites; a factory burns, 2 people hurt."),
    ("HOUTHIS HIT BACK (FRI\u2013SAT)",
     "Saudi coalition intercepts missiles and drones aimed at Riyadh and the southern region."),
    ("FT TRACES CHIP NETWORK",
     "Alice Huang linked to a network moving banned Nvidia chips into China, the FT finds."),
    ("WAYMO STAYS GROUNDED",
     "Robotaxis still off US freeways after California\u2019s DMV ban of 11 Nov over construction-zone incursions."),
    ("MUMBAI ASSAULT CASE",
     "Six sent to a juvenile home; a Maharashtra SP leader seeks an age change."),
    ("PORTUGAL BUDGET VOTE LOOMS",
     "Final 2027 budget vote due Tuesday 24 Nov; unions plan a parliament demonstration."),
]

ALSO = ("ALSO: Nepal\u2013India business forum in Delhi \u2022 Portugal\u2019s "
        "2027 budget vote Tuesday \u2022 World chess championship \u2022 "
        "Anupama\u2019s snooker defence \u2022 IFFI 2026 in Goa")

DATECHECK = ("Lead stories are Monday 23 November 2026 events or Monday "
             "developments (talks in Delhi, search resuming in Serang, the "
             "final day in Wellington). Weekend stories are tagged SAT, SUN "
             "or FRI and appear only as Monday\u2019s context. Cross-checked "
             "against wire reports (Reuters, AP, BBC, UN News) on Monday "
             "23 November 2026.")

# Dot-matrix world map: (row) -> list of (col_start, col_end) land spans.
MAP_ROWS = [
    [(8, 14), (18, 24), (28, 33), (58, 106)],
    [(4, 36), (54, 64), (66, 108)],
    [(6, 34), (53, 62), (64, 106)],
    [(8, 33), (52, 64), (66, 104)],
    [(10, 32), (52, 66), (68, 100), (102, 104)],
    [(12, 30), (50, 68), (70, 80), (84, 98)],
    [(13, 24), (50, 67), (74, 79), (82, 95)],
    [(15, 20), (51, 66), (75, 78), (83, 92)],
    [(31, 42), (53, 65), (84, 86), (89, 91), (93, 96)],
    [(32, 43), (55, 64), (86, 90), (93, 97)],
    [(33, 43), (56, 63), (89, 100)],
    [(34, 42), (57, 62), (90, 99)],
    [(35, 41), (58, 61), (91, 98)],
    [(36, 40), (104, 105)],
    [(37, 39)],
    [(37, 38)],
]
# (col, row): Dymer, Gulf of Finland, Antalya, Lisbon, Delhi, Seoul,
# Serang/Jakarta, Guasave, Wellington
PINS = [(59, 3), (60, 2), (63, 4), (48, 4), (76, 6), (93, 4),
        (88, 9), (13, 6), (104, 13)]


# ---------------------------------------------------------------- drawing
def masthead(d):
    y = 16
    rule(d, M, W - M, y, INK, 3)
    rule(d, M, W - M, y + 5, INK, 1)
    y += 12
    # side notes
    f_side = F(SANS_CSB, 11)
    d.text((M, y + 8), "GLOBAL EDITION", font=f_side, fill=GRAY)
    rtxt = "No. 328 \u2022 PRICE: ONE IMAGE"
    d.text((W - M - tw(d, rtxt, f_side), y + 8), rtxt, font=f_side, fill=GRAY)
    # paper name
    name = "THE DAILY ORBIT"
    fn = fit(d, name, SERIF_BLACK, 560, 54)
    d.text(((W - tw(d, name, fn)) / 2, y), name, font=fn, fill=INK)
    y += 48
    # giant date
    date = "MONDAY 23 NOVEMBER 2026"
    fd_ = fit(d, date, SERIF_BLACK, CW, 64)
    d.text(((W - tw(d, date, fd_)) / 2, y), date, font=fd_, fill=INK)
    y += 58
    rule(d, M, W - M, y, INK, 1)
    rule(d, M, W - M, y + 3, INK, 3)
    return y + 8


def red_strip(d, y):
    h = 30
    d.rectangle([M, y, W - M, y + h], fill=RED)
    fs = fit(d, RED_STRIP, SANS_CB, CW - 20, 17)
    d.text(((W - tw(d, RED_STRIP, fs)) / 2, y + 5), RED_STRIP, font=fs,
           fill=(255, 250, 240))
    return y + h + 4


def world_strip(d, y):
    h = 26
    d.rectangle([M, y, W - M, y + h], fill=INK)
    f1 = F(SANS_CB, 15)
    d.text((M + 10, y + 4), "THE WORLD IN ONE DAY", font=f1,
           fill=(255, 250, 240))
    f2 = F(SANS_CSB, 12)
    t = "30 STORIES \u2022 SIX CONTINENTS \u2022 ONE PAGE"
    d.text((W - M - 10 - tw(d, t, f2), y + 6), t, font=f2, fill=(230, 224, 208))
    return y + h + 6


def stats_strip(d, y):
    n = len(STATS)
    gap = 8
    bw = (CW - gap * (n - 1)) / n
    f_num = F(SERIF_XB, 25)
    f_lab = F(SANS_CSB, 9)
    rule(d, M, W - M, y, HAIR, 1)
    y += 6
    for i, (num, lab) in enumerate(STATS):
        x = M + i * (bw + gap)
        if i:
            d.line([(x - gap / 2, y + 2), (x - gap / 2, y + 44)], fill=HAIR,
                   width=1)
        d.text((x, y), num, font=f_num, fill=DRED)
        ly = y + 30
        for ln in lab.split("\n"):
            d.text((x, ly), ln, font=f_lab, fill=GRAY)
            ly += 10.5
    y += 52
    rule(d, M, W - M, y, HAIR, 1)
    return y + 8


def star(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.34
        pts.append((cx + rr * math.cos(ang), cy - rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def hero(d, x, y, wdt, hgt, idx, spec):
    d.rectangle([x, y, x + wdt, y + hgt], fill=PANEL)
    d.rectangle([x, y, x + wdt, y + 5], fill=spec["accent"])
    # number badge
    d.rectangle([x + 10, y + 13, x + 34, y + 37], fill=spec["accent"])
    fn_ = F(SANS_CB, 17)
    num = str(idx + 1)
    d.text((x + 22 - tw(d, num, fn_) / 2, y + 16), num, font=fn_,
           fill=(255, 250, 240))
    fk = F(SANS_CB, 12)
    d.text((x + 42, y + 19), spec["kick"], font=fk, fill=spec["accent"])
    # headline
    fh = F(SERIF_B, 20)
    hy = block(d, (x + 10, y + 44), spec["head"], fh, INK, wdt - 20, 23, 3)
    rule(d, x + 10, x + wdt - 10, hy + 1, HAIR, 1)
    # body
    fb = F(SANS_C, 11)
    by = block(d, (x + 10, hy + 6), spec["body"], fb, (44, 41, 36),
               wdt - 20, 13.5)
    if idx == 0:
        rule(d, x + 10, x + wdt - 10, y + hgt - 38, HAIR, 1)
        star(d, x + wdt - 30, y + hgt - 20, 12, NAVY)
        ff = F(SANS_CM, 9)
        block(d, (x + 10, y + hgt - 32), spec["foot"], ff, GRAY, wdt - 52,
              11, 2)
    elif idx == 1:
        rule(d, x + 10, x + wdt - 10, y + hgt - 38, HAIR, 1)
        fbadge = F(SERIF_XB, 17)
        d.text((x + 10, y + hgt - 33), "7 A.M.", font=fbadge, fill=DRED)
        ff = F(SANS_CM, 9)
        block(d, (x + 92, y + hgt - 30), spec["foot"], ff, GRAY, wdt - 102,
              11, 2)
    else:
        # top-score bars
        fy = by + 6
        fl = F(SANS_CSB, 10)
        fv = F(SANS_CB, 10)
        d.text((x + 10, fy), "TOP SCORES \u2014 INDIA 720/9:", font=fl, fill=GRAY)
        fy += 14
        maxv = 140.0
        for name, val in BARS:
            d.text((x + 10, fy), name, font=fl, fill=INK)
            bx = x + 76
            blen = (val / maxv) * (wdt - 140)
            d.rectangle([bx, fy + 2, bx + blen, fy + 10], fill=GREEN)
            vt = str(val)
            d.text((bx + blen + 5, fy), vt, font=fv, fill=GREEN)
            fy += 13
    d.rectangle([x, y, x + wdt, y + hgt], outline=HAIR, width=1)


def heroes(d, y):
    gap = 12
    wdt = (CW - 2 * gap) / 3
    hgt = 240
    for i, spec in enumerate(HEROES):
        hero(d, M + i * (wdt + gap), y, wdt, hgt, i, spec)
    return y + hgt + 10


def cards(d, y):
    cols, rows = 3, 9
    gap = 14
    wdt = (CW - (cols - 1) * gap) / cols
    rh = 41
    f_num = F(SANS_CB, 12)
    f_head = F(SANS_CB, 12)
    f_body = F(SANS_C, 9.5)
    for i, (head, body) in enumerate(CARDS):
        cx = M + (i % cols) * (wdt + gap)
        cy = y + (i // cols) * rh
        num = str(i + 4)
        d.rectangle([cx, cy + 1, cx + 17, cy + 18], fill=RED)
        d.text((cx + 8.5 - tw(d, num, f_num) / 2, cy + 3), num, font=f_num,
               fill=(255, 250, 240))
        hx = cx + 23
        hw = wdt - 23
        hl = wrap(d, head, f_head, hw)
        if len(hl) == 1 and tw(d, head, f_head) <= hw:
            d.text((hx, cy), head, font=f_head, fill=INK)
            by = cy + 15
        else:
            d.text((hx, cy), hl[0], font=f_head, fill=INK)
            if len(hl) > 1:
                d.text((hx, cy + 13), hl[1], font=f_head, fill=INK)
            by = cy + 28
        block(d, (hx, by), body, f_body, (58, 54, 48), hw, 10.5, 2)
        if i // cols < rows - 1:
            rule(d, cx, cx + wdt, cy + rh - 3, (216, 209, 192), 1)
    return y + rows * rh + 2


def draw_map(d, x, y, pitch=3.6, r=1.2):
    for ri, spans in enumerate(MAP_ROWS):
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                cx = x + c * pitch
                cy = y + ri * pitch
                d.ellipse([cx - r, cy - r, cx + r, cy + r],
                          fill=(150, 143, 126))
    for c, ri in PINS:
        cx = x + c * pitch
        cy = y + ri * pitch
        d.ellipse([cx - 3.4, cy - 3.4, cx + 3.4, cy + 3.4], fill=RED,
                  outline=(255, 250, 240), width=1)


def bottom_band(d, y):
    # ALSO ticker
    fa = fit(d, ALSO, SANS_CSB, CW, 12)
    d.text((M, y), ALSO, font=fa, fill=(44, 41, 36))
    y += 18
    rule(d, M, W - M, y, INK, 2)
    y += 8
    # map left
    d.text((M, y), "WHERE IT HAPPENED", font=F(SANS_CB, 11), fill=INK)
    draw_map(d, M + 2, y + 20)
    # date check box right
    bx = M + 420
    bw = W - M - bx
    d.rectangle([bx, y, bx + bw, y + 78], outline=RED, width=2)
    d.rectangle([bx, y, bx + bw, y + 20], fill=RED)
    fd_ = F(SANS_CB, 13)
    d.text((bx + 10, y + 3), "DATE CHECK", font=fd_, fill=(255, 250, 240))
    block(d, (bx + 10, y + 26), DATECHECK, F(SANS_C, 10.5), (44, 41, 36),
          bw - 20, 12.5, 4)
    # footer
    fy = y + 86
    ff = F(SANS_CM, 9)
    foot = ("Compiled Monday 23 November 2026 \u2022 Sources: Reuters, AP, BBC, "
            "UN News, ESPNcricinfo and wire reports \u2022 The Daily Orbit \u2014 "
            "the world in one day")
    d.text(((W - tw(d, foot, ff)) / 2, fy), foot, font=ff, fill=GRAY)
    return fy + 14


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = masthead(d)
    y = red_strip(d, y)
    y = world_strip(d, y)
    y = stats_strip(d, y)
    y = heroes(d, y)
    y = cards(d, y)
    bottom_band(d, y)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or (
        "/output" if os.path.isdir("/output") else HERE)
    out = os.path.join(out_dir, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
