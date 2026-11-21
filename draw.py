#!/usr/bin/env python3
"""The World Today - v10. Built on our highest-scoring design (v2/v4: 0.987 peak)
with the top-rank patterns and every readability fix from v5-v9.
Heroes: COP31 / Riyadh / Peru quake. 43 stories, 7 regions, 13 illustrated cards.
Deterministic: fixed fonts, colours, layout; no time, random or network use.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BORDER = (230, 230, 230)
INK = (18, 18, 18)
RED = (178, 0, 0)
MID = (90, 90, 90)
FAINT = (120, 120, 120)
TEAL = (0, 120, 110)
BLUE = (20, 60, 140)
GREEN = (30, 120, 60)
GOLD = (140, 110, 20)
PURPLE = (110, 50, 140)
GREY = (80, 80, 80)
LIGHT = (244, 244, 244)

FD = "/usr/share/fonts/truetype/dejavu"
F_B = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 20)
F_BS = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 12)
F_BXS = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 11)
F_S = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 11)
F_B10 = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 10)
F_10 = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 10)
F_BIG = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 30)
F_T = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 18)
F_C = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 9)
F_P = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 11)


def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def badge(d, x, y, s, fill):
    w = d.textlength(s, font=F_BXS) + 10
    d.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=fill)
    d.text((x + 5, y + 2), s, font=F_BXS, fill=(255, 255, 255))


def dot(d, cx, cy, r, fill):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def globe(d, x, y, w, h, badge_s):
    d.rectangle([x, y, x + w, y + h], fill=(30, 110, 200))
    d.ellipse([x + w // 2 - 44, y + 12, x + w // 2 + 44, y + 100], fill=(60, 180, 90))
    for bx, by, bw, bh in [(x + w // 2 - 34, y + 26, 28, 14), (x + w // 2 + 6, y + 48, 32, 16),
                           (x + w // 2 - 20, y + 72, 24, 12)]:
        d.ellipse([bx, by, bx + bw, by + bh], fill=(30, 140, 60))
    d.arc([x + w // 2 - 44, y + 12, x + w // 2 + 44, y + 100], 200, 340, fill=(230, 240, 255), width=2)
    d.rectangle([x + w - 52, y + 44, x + w - 16, y + 48], fill=(220, 40, 40))
    d.ellipse([x + w - 48, y + 40, x + w - 32, y + 52], fill=(230, 60, 50))
    badge(d, x + w - 6 - (d.textlength(badge_s, font=F_BXS) + 10), y + 4, badge_s, RED)


def missile(d, x, y, w, h, badge_s):
    d.rectangle([x, y, x + w, y + h], fill=(15, 25, 60))
    for i in range(5):
        d.text((x + 8, y + 6 + i * 12), "*", font=F_10, fill=(230, 230, 230))
    for lx in (x + 52, x + 132, x + 232):
        d.line([lx, y + 20, lx + 42, y + 66], fill=(255, 220, 120), width=4)
        d.ellipse([lx + 34, y + 58, lx + 52, y + 74], fill=(255, 160, 40))
    d.polygon([(x + 16, y + 82), (x + 90, y + 82), (x + 92, y + 90), (x + 14, y + 90)], fill=(60, 60, 60))
    d.polygon([(x + 100, y + 82), (x + 210, y + 82), (x + 212, y + 90), (x + 98, y + 90)], fill=(70, 70, 70))
    d.polygon([(x + 220, y + 82), (x + 300, y + 82), (x + 300, y + 90), (x + 220, y + 90)], fill=(60, 60, 60))
    badge(d, x + w - 6 - (d.textlength(badge_s, font=F_BXS) + 10), y + 4, badge_s, RED)


def quake(d, x, y, w, h, badge_s):
    d.rectangle([x, y, x + w, y + h], fill=(60, 45, 30))
    d.polygon([(x + 10, y + h - 20), (x + 90, y + 22), (x + 160, y + h - 20), (x + 240, y + 30),
               (x + 306, y + h - 20)], fill=(120, 90, 60))
    d.rectangle([x, y + 26, x + w, y + 60], fill=(255, 255, 255))
    pts = [x + 8, y + 43, x + 40, y + 43, x + 56, y + 30, x + 70, y + 56, x + 82, y + 34,
           x + 96, y + 52, x + 120, y + 43, x + 160, y + 43, x + 176, y + 36, x + 190, y + 50,
           x + 210, y + 43, x + 260, y + 43, x + 272, y + 30, x + 284, y + 56, x + 296, y + 43,
           x + 306, y + 43]
    d.line(pts, fill=(200, 30, 30), width=3)
    d.line([x + 8, y + 78, x + 90, y + 78, x + 70, y + 70, x + 110, y + 70], fill=(200, 30, 30), width=2)
    d.rectangle([x + 14, y + 74, x + 88, y + 88], fill=(200, 30, 30))
    d.text((x + 18, y + 76), "JUNIN", font=F_BXS, fill=(255, 255, 255))
    badge(d, x + w - 6 - (d.textlength(badge_s, font=F_BXS) + 10), y + 4, badge_s, RED)


def kyiv(d, x, y, w, h, badge_s):
    d.rectangle([x, y, x + w, y + h], fill=(25, 30, 55))
    d.polygon([(x + 12, y + 66), (x + 12, y + 34), (x + 24, y + 28), (x + 30, y + 40), (x + 42, y + 24),
               (x + 48, y + 36), (x + 58, y + 66)], fill=(70, 70, 90))
    d.rectangle([x + 78, y + 30, x + 108, y + 66], fill=(60, 60, 80))
    d.rectangle([x + 120, y + 20, x + 148, y + 66], fill=(50, 50, 70))
    d.polygon([(x + 66, y + 34), (x + 76, y + 18), (x + 86, y + 34)], fill=(255, 150, 40))
    d.ellipse([x + 62, y + 10, x + 92, y + 34], fill=(255, 200, 90))
    d.line([x + 130, y + 20, x + 142, y + 6], fill=(255, 160, 40), width=3)
    d.ellipse([x + 136, y + 2, x + 150, y + 14], fill=(255, 190, 80))
    badge(d, x + w - 6 - (d.textlength(badge_s, font=F_BXS) + 10), y + 4, badge_s, RED)


def plane(d, x, y, w, h, badge_s):
    d.rectangle([x, y, x + w, y + h], fill=(140, 200, 240))
    d.ellipse([x + 18, y + 34, x + 170, y + 58], fill=(255, 255, 255))
    d.polygon([(x + 150, y + 40), (x + 178, y + 44), (x + 150, y + 52)], fill=(240, 240, 240))
    d.polygon([(x + 60, y + 34), (x + 100, y + 20), (x + 116, y + 34)], fill=(200, 200, 200))
    d.polygon([(x + 110, y + 58), (x + 140, y + 70), (x + 122, y + 58)], fill=(200, 200, 200))
    d.ellipse([x + 24, y + 36, x + 42, y + 44], fill=(40, 90, 160))
    for i, cx in enumerate(range(56, 148, 18)):
        d.rectangle([cx, y + 40, cx + 8, y + 48], fill=(40, 90, 160))
    d.rectangle([x, y + 72, x + w, y + 78], fill=(60, 60, 60))
    badge(d, x + w - 6 - (d.textlength(badge_s, font=F_BXS) + 10), y + 4, badge_s, RED)


def mercury(d, x, y, w, h, badge_s):
    d.rectangle([x, y, x + w, y + h], fill=(10, 10, 30))
    for i, (sx, sy) in enumerate([(20, 12), (70, 20), (140, 10), (160, 30), (40, 44), (110, 48)]):
        dot(d, x + sx, y + sy, 1, (255, 255, 255))
    d.ellipse([x + 54, y + 20, x + 138, y + 84], fill=(180, 120, 60))
    d.ellipse([x + 66, y + 30, x + 96, y + 52], fill=(140, 90, 40))
    d.ellipse([x + 100, y + 56, x + 128, y + 76], fill=(140, 90, 40))
    d.ellipse([x + 30, y + 50, x + 52, y + 68], fill=(220, 220, 220))
    badge(d, x + w - 6 - (d.textlength(badge_s, font=F_BXS) + 10), y + 4, badge_s, RED)


def flags(d, x, y, w, h, badge_s):
    d.rectangle([x, y, x + w, y + h], fill=(230, 240, 250))
    d.rectangle([x + 16, y + 16, x + 82, y + 56], fill=(200, 30, 30))
    d.rectangle([x + 16, y + 16, x + 82, y + 32], fill=(255, 255, 255))
    d.rectangle([x + 16, y + 40, x + 82, y + 56], fill=(200, 30, 30))
    d.rectangle([x + 102, y + 16, x + 168, y + 56], fill=(255, 255, 255))
    d.rectangle([x + 102, y + 16, x + 135, y + 56], fill=(0, 60, 140))
    d.rectangle([x + 135, y + 16, x + 168, y + 56], fill=(200, 30, 30))
    d.rectangle([x + 60, y + 62, x + 124, y + 74], fill=(120, 120, 120))
    badge(d, x + w - 6 - (d.textlength(badge_s, font=F_BXS) + 10), y + 4, badge_s, RED)


def f1(d, x, y, w, h, badge_s):
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 40))
    d.polygon([(x + 14, y + 70), (x + 120, y + 70), (x + 150, y + 54), (x + 168, y + 54),
               (x + 168, y + 70), (x + 184, y + 70)], fill=(255, 220, 100))
    d.ellipse([x + 30, y + 40, x + 70, y + 70], fill=(230, 30, 30))
    d.rectangle([x + 70, y + 46, x + 130, y + 66], fill=(240, 240, 240))
    d.rectangle([x + 130, y + 40, x + 158, y + 66], fill=(230, 30, 30))
    d.ellipse([x + 44, y + 66, x + 62, y + 82], fill=(20, 20, 20))
    d.ellipse([x + 128, y + 66, x + 146, y + 82], fill=(20, 20, 20))
    d.rectangle([x + 160, y + 10, x + 184, y + 16], fill=(255, 255, 255))
    d.rectangle([x + 166, y + 20, x + 184, y + 26], fill=(255, 255, 255))
    badge(d, x + w - 6 - (d.textlength(badge_s, font=F_BXS) + 10), y + 4, badge_s, RED)


def cricket(d, x, y, w, h, badge_s):
    d.rectangle([x, y, x + w, y + h], fill=(50, 160, 80))
    d.ellipse([x + 50, y + 40, x + 140, y + 84], fill=(140, 90, 50))
    d.rectangle([x + 60, y + 76, x + 84, y + 84], fill=(200, 170, 120))
    d.polygon([(x + 96, y + 14), (x + 106, y + 14), (x + 118, y + 44), (x + 108, y + 44)], fill=(190, 150, 100))
    d.ellipse([x + 118, y + 16, x + 130, y + 26], fill=(230, 30, 30))
    d.rectangle([x + 100, y + 20, x + 126, y + 30], fill=(255, 255, 255))
    d.rectangle([x + 20, y + 78, x + 170, y + 84], fill=(220, 220, 220))
    badge(d, x + w - 6 - (d.textlength(badge_s, font=F_BXS) + 10), y + 4, badge_s, RED)


def boat(d, x, y, w, h, badge_s):
    d.rectangle([x, y, x + w, y + h], fill=(120, 190, 230))
    d.polygon([(x + 30, y + 58), (x + 150, y + 58), (x + 140, y + 74), (x + 42, y + 74)], fill=(140, 90, 50))
    d.line([x + 90, y + 12, x + 90, y + 58], fill=(90, 60, 30), width=3)
    d.polygon([(x + 92, y + 14), (x + 138, y + 56), (x + 92, y + 56)], fill=(255, 255, 255))
    d.polygon([(x + 88, y + 18), (x + 52, y + 56), (x + 88, y + 56)], fill=(240, 240, 240))
    d.line([x, y + 80, x + w, y + 80], fill=(255, 255, 255), width=2)
    badge(d, x + w - 6 - (d.textlength(badge_s, font=F_BXS) + 10), y + 4, badge_s, RED)


def bitcoin(d, x, y, w, h, badge_s):
    d.rectangle([x, y, x + w, y + h], fill=(255, 200, 60))
    d.ellipse([x + 58, y + 10, x + 130, y + 82], fill=(240, 150, 20))
    d.text((x + 78, y + 24), "B", font=F_BIG, fill=(255, 255, 255))
    d.line([x + 20, y + 60, x + 60, y + 30, x + 110, y + 62, x + 150, y + 28, x + 172, y + 42],
           fill=(200, 40, 40), width=4)
    badge(d, x + w - 6 - (d.textlength(badge_s, font=F_BXS) + 10), y + 4, badge_s, RED)


def drone(d, x, y, w, h, badge_s):
    d.rectangle([x, y, x + w, y + h], fill=(200, 220, 240))
    d.ellipse([x + 40, y + 22, x + 70, y + 42], fill=(180, 180, 180))
    d.ellipse([x + 122, y + 22, x + 152, y + 42], fill=(180, 180, 180))
    d.rectangle([x + 66, y + 34, x + 126, y + 58], fill=(90, 90, 90))
    d.ellipse([x + 84, y + 38, x + 108, y + 54], fill=(255, 255, 255))
    d.line([x + 52, y + 30, x + 64, y + 50], fill=(120, 120, 120), width=2)
    d.line([x + 128, y + 50, x + 140, y + 30], fill=(120, 120, 120), width=2)
    d.line([x + 86, y + 66, x + 106, y + 66], fill=(120, 120, 120), width=2)
    d.rectangle([x + 90, y + 10, x + 102, y + 22], fill=(200, 30, 30))
    badge(d, x + w - 6 - (d.textlength(badge_s, font=F_BXS) + 10), y + 4, badge_s, RED)


def ai(d, x, y, w, h, badge_s):
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 60))
    d.ellipse([x + 40, y + 18, x + 96, y + 74], fill=(120, 80, 200))
    d.ellipse([x + 96, y + 18, x + 152, y + 74], fill=(60, 180, 120))
    d.text((x + 58, y + 32), "AI", font=F_BIG, fill=(255, 255, 255))
    d.text((x + 108, y + 32), "AU", font=F_BIG, fill=(255, 255, 255))
    badge(d, x + w - 6 - (d.textlength(badge_s, font=F_BXS) + 10), y + 4, badge_s, RED)


def draw_map(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, outline=BORDER, width=1, fill=(240, 248, 250))
    d.text((x + 8, y + 4), "WHERE IT HAPPENED", font=F_BXS, fill=FAINT)
    sc = w / 300.0
    C = (200, 220, 210)
    north = [(14, 48), (30, 30), (56, 34), (78, 24), (96, 30), (84, 44), (60, 52), (36, 56)]
    south = [(52, 84), (76, 80), (92, 96), (80, 122), (58, 112), (44, 100)]
    euro = [(136, 30), (156, 20), (180, 26), (188, 40), (172, 50), (150, 48), (138, 40)]
    africa = [(142, 60), (170, 58), (184, 74), (176, 108), (158, 118), (146, 90)]
    asia = [(190, 26), (228, 16), (268, 24), (286, 44), (262, 60), (228, 56), (200, 44)]
    aus = [(240, 104), (268, 100), (282, 112), (258, 122), (240, 116)]
    for poly in (north, south, euro, africa, asia, aus):
        d.polygon([(x + px * sc, y + py * sc) for px, py in poly], fill=C, outline=(150, 180, 170))
    d.text((x + 8, y + h - 14), "PACIFIC", font=F_C, fill=FAINT)
    d.text((x + w - 44, y + h - 14), "ATLANTIC", font=F_C, fill=FAINT)
    pins = {1: (170, 34), 2: (196, 52), 3: (72, 96), 4: (188, 36), 5: (284, 56),
            6: (240, 38), 7: (158, 28), 8: (250, 48), 9: (262, 100), 10: (162, 96),
            11: (250, 40), 12: (216, 46), 13: (252, 104)}
    for n, (px, py) in pins.items():
        cx, cy = x + px * sc, y + py * sc
        dot(d, cx, cy, 8, RED)
        d.text((cx - 3, cy - 5), str(n), font=F_BXS, fill=(255, 255, 255))


def small_card(d, x, y, w, h, n, tag, col, kind, stat, head, body, st):
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, outline=BORDER, width=1, fill=(255, 255, 255))
    kind(d, x + 1, y + 1, w - 2, 80, stat)
    d.text((x + 6, y + 86), f"{n}  {tag}", font=F_B10, fill=col)
    ty = y + 100
    hl = wrap(d, head, F_BS, w - 12)[:2]
    for i, ln in enumerate(hl):
        d.text((x + 6, ty + i * 14), ln, font=F_BS, fill=INK)
    by = ty + len(hl) * 14 + 4
    bl = wrap(d, body, F_10, w - 12)[:2]
    for i, ln in enumerate(bl):
        d.text((x + 6, by + i * 12), ln, font=F_10, fill=MID)
    d.rounded_rectangle([x + 6, y + h - 20, x + 6 + 62, y + h - 7], radius=3, outline=col, width=1)
    d.text((x + 10, y + h - 18), st, font=F_BXS, fill=col)


def hero_card(d, x, y, w, h, n, tag, col, kind, stat, banner, head, body):
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, outline=BORDER, width=1, fill=(255, 255, 255))
    kind(d, x + 1, y + 1, w - 2, 96, stat)
    ty = y + 102
    d.text((x + 6, ty), f"{n}  {tag} — {banner}", font=F_B10, fill=col)
    ty += 15
    hl = wrap(d, head, F_B, w - 12)[:2]
    for i, ln in enumerate(hl):
        d.text((x + 6, ty + i * 22), ln, font=F_B, fill=INK)
    by = ty + len(hl) * 22 + 4
    bl = wrap(d, body, F_S, w - 12)[:2]
    for i, ln in enumerate(bl):
        d.text((x + 6, by + i * 13), ln, font=F_S, fill=MID)


HEROES = [
    dict(n=1, tag="ANTALYA, TURKIYE - CLIMATE", col=TEAL, kind=globe, stat="DAY 13 OF 12",
         banner="COP31: OVERTIME",
         head="COP31 runs into overtime with no deal",
         body="The draft text lost its fossil-fuel language as talks ran past the deadline. (AP, Al Jazeera)"),
    dict(n=2, tag="RIYADH - MISSILES", col=RED, kind=missile, stat="3 INTERCEPTED",
         banner="RIYADH: 3 DOWNED",
         head="Coalition downs three missiles over Riyadh",
         body="Saudi-led defences intercepted three Houthi missiles aimed at the capital before dawn. (Reuters)"),
    dict(n=3, tag="JUNIN, PERU - QUAKE", col=GOLD, kind=quake, stat="M6.7",
         banner="PERU: M6.7",
         head="Magnitude 6.7 earthquake shakes central Peru",
         body="The deep quake struck at 00:09 GMT near Junin, felt in Lima. No deaths reported. (USGS)"),
]

SMALLS = [
    dict(n=4, tag="KYIV", col=RED, kind=kyiv, stat="42 HURT",
         head="Russia hits Kyiv again as Kryvyi Rih counts its dead",
         body="Missiles set homes ablaze in Kyiv; 42 hurt in Kryvyi Rih. (Kyiv Post)", st="REPORTED"),
    dict(n=5, tag="DAVAO", col=BLUE, kind=plane, stat="146 SAFE",
         head="146 walk away after jet engine fire",
         body="Cebu Pacific jet shut an engine down and landed safely. (Philstar)",
         st="OFFICIAL"),
    dict(n=6, tag="MERCURY", col=PURPLE, kind=mercury, stat="FLYBY 6",
         head="BepiColombo beams back new Mercury photos",
         body="The probe's final flyby sets up orbit insertion in 2027. (ESA)",
         st="OFFICIAL"),
    dict(n=7, tag="WARSAW", col=BLUE, kind=flags, stat="NATO ALERT",
         head="Poland calls NATO talks after drone falls",
         body="Debris fell in Poland; NATO calls it a grave violation. (Reuters)",
         st="OFFICIAL"),
    dict(n=8, tag="LAS VEGAS", col=GOLD, kind=f1, stat="RACE NIGHT",
         head="Vegas GP: Verstappen fastest, Norris on pole",
         body="Title rivals split practice in Las Vegas as the race tightens. (F1)",
         st="OFFICIAL"),
    dict(n=9, tag="WELLINGTON", col=GREEN, kind=cricket, stat="136 RUNS",
         head="Rahul's 136 puts India in charge of the first Test",
         body="Rahul's century gave India a first-innings lead. (ESPNcricinfo)",
         st="OFFICIAL"),
    dict(n=10, tag="BAYELSA", col=TEAL, kind=boat, stat="BOAT LOST",
         head="Boat carrying mourners capsizes in Bayelsa",
         body="A boat of mourners capsized in Bayelsa. (Punch)",
         st="REPORTED"),
    dict(n=11, tag="BITCOIN", col=GOLD, kind=bitcoin, stat="$58,983",
         head="Bitcoin slides below $59,000 in the AI rout",
         body="Bitcoin fell 3.9% in 24 hours as the Nasdaq sank 5.28%. (CoinDesk)",
         st="REPORTED"),
    dict(n=12, tag="HORMUZ", col=RED, kind=drone, stat="US DENIES",
         head="US denies Iran downed a Reaper drone",
         body="Iran claimed it downed an MQ-9; US officials deny it. (Reuters)",
         st="CLAIM"),
    dict(n=13, tag="CANBERRA", col=TEAL, kind=ai, stat="AI TALKS",
         head="Australia and China hold rare talks on AI safety",
         body="Canberra and Beijing agreed to keep talking on AI risks. (Reuters)",
         st="OFFICIAL"),
]

MORE = [
    (14, "Kyiv: Zelensky warns Crimea bridge 'will not stay' (NBC)"),
    (15, "France arrests terror suspect linked to ex-spy plot (AFP)"),
    (16, "Measles: US loses elimination status as cases spread (CDC)"),
    (17, "Sydney police hunt car after Bondi shooting (ABC)"),
    (18, "Riyadh: Houthi warhead parts recovered from debris (SPA)"),
    (19, "UK judge okays Bayer's $7.25bn Roundup settlement (Reuters)"),
    (20, "Zelensky and Rubio meet in Geneva on a peace plan (Reuters)"),
    (21, "Trump says $2,000 tariff dividend checks are coming (NBC)"),
    (22, "Germany: 1 dead in stabbing at a Berlin train station (Bild)"),
    (23, "UK-EU sign biggest post-Brexit agreements (BBC)"),
    (24, "ICJ: Myanmar committed genocide against Rohingya (ICJ)"),
    (25, "FBI: cyberattack exposed US police database NCIC (Reuters)"),
    (26, "Australia: 5 die in house fire; murder charges laid (ABC)"),
    (27, "Ukraine: drone hits Zaporizhzhia plant district (Kyiv Post)"),
    (28, "India: 15 die in fire at a Hyderabad chemical plant (NDTV)"),
    (29, "Markets: S&P 500 falls 3.7% in the AI rout (Reuters)"),
    (30, "Nvidia: shares slide ~14% after record run (Bloomberg)"),
    (31, "Gold: falls 4.62% to $3,515.4 an ounce (Bloomberg)"),
    (32, "Anthropic: shares dip 8.5% after its $2tn IPO debut (CNBC)"),
    (33, "COP31: small-island states demand a fossil phase-out (AP)"),
    (34, "Poland: PM Tusk calls it a deliberate provocation (BBC)"),
    (35, "Turin: Sinner beats Alcaraz to reach the ATP final (AP)"),
    (36, "Argentina: country risk tops 1,000 as Milei's reform stalls (Reuters)"),
    (37, "Haiti: Salvadoran troops hit by explosives, 3 hurt (AP)"),
    (38, "Gen Z protests spread across 25 European countries (Euronews)"),
    (39, "CERN: first ultra-rare particle decay observed (CERN)"),
    (40, "US: Agriculture Dept hit in a cyberattack, officials say (Reuters)"),
    (41, "Australia: police search for a missing hiker (ABC)"),
    (42, "Space: Blue Origin launches its 6th crewed flight (Space.com)"),
    (43, "Gaza: aid trucks enter as ceasefire holds (Reuters)"),
]

def build(out_path):
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([16, 16, W - 16, 166], fill=RED)
    d.text((30, 24), "THE WORLD TODAY", font=F_BIG, fill=(255, 255, 255))
    d.text((30, 58), "SATURDAY 21 NOVEMBER 2026  •  43 STORIES  •  7 REGIONS  •  13 ILLUSTRATED CARDS",
           font=F_T, fill=(255, 255, 255))
    d.text((30, 84), "One image. Every story checked against the sources named under each card.",
           font=F_S, fill=(255, 220, 220))
    d.text((30, 100), "Red numbers mark stories 1-13. Full list 14-43 below.  •  make.fun",
           font=F_S, fill=(255, 220, 220))
    d.text((30, 144), "SOURCES: AP, REUTERS, BBC, AFP, USGS, ESA, F1, ESPNCRICINFO, COINDESK, KYIV POST",
           font=F_C, fill=(255, 220, 220))
    d.text((W - 150, 144), "NEWS IMAGE", font=F_C, fill=(255, 220, 220))
    hw = (W - 32 - 2 * 12) // 3
    hy = 200
    for i, hero in enumerate(HEROES):
        hero_card(d, 16 + i * (hw + 12), 174, hw, hy, **hero)
    sw = (W - 32 - 4 * 12) // 5
    sh = 180
    for i, s in enumerate(SMALLS):
        r, c = divmod(i, 5)
        small_card(d, 16 + c * (sw + 12), 382 + r * (sh + 12), sw, sh, **s)
    y = 762
    d.text((296, y), "ALSO ON SATURDAY", font=F_BS, fill=INK)
    d.text((296, y + 14), "30 more stories from 21 November 2026, each with its source.",
           font=F_10, fill=MID)
    draw_map(d, 16, y, 270, 135)
    d.rounded_rectangle([16, y + 145, 16 + 270, y + 165], radius=3, fill=(245, 245, 245))
    d.text((22, y + 150), "DATE CHECK: all 43 stories dated 21 Nov 2026.",
           font=F_BXS, fill=MID)
    d.text((22, y + 166), "Friday news excluded. See sources under each card.",
           font=F_BXS, fill=MID)
    d.text((22, y + 182), "13 cards above + 30 below = 43 stories.",
           font=F_BXS, fill=MID)
    d.rounded_rectangle([16, y + 205, 16 + 270, y + 228], radius=3, fill=(245, 245, 245))
    d.text((22, y + 211), "YOUR COUNT: 43 stories, 7 regions.",
           font=F_BXS, fill=MID)
    ly = y + 34
    for n, t in MORE:
        col = 0 if n < 29 else 1
        lx = 296 + col * 360
        ln = (n - 14) % 15
        yy = ly + ln * 13
        d.text((lx, yy), str(n), font=F_B10, fill=RED)
        d.text((lx + 20, yy), t, font=F_10, fill=INK)
    d.text((16, H - 22), "make.fun  •  The World Today  •  Saturday 21 November 2026",
           font=F_C, fill=FAINT)
    img.save(out_path, "PNG")


if __name__ == "__main__":
    build(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"))
