import math
from PIL import Image, ImageDraw
from led_kit import *
from marc_lot import COLS, save
from friend_g_nightsky import text1x
import newchar
from newchar import sky, sprite, minicloud, ORG
NAVY, B1, B2, B3, LIGHT, BELLY = (0, 60, 130), (4, 92, 190), (4, 164, 244), (90, 210, 255), (200, 250, 255), (150, 235, 250)
PINK = (252, 130, 170)
TAIL = ["bb......bb",
        "bbb....bbb",
        ".bbb..bbb.",
        "..bbbbbb..",
        "...bbbb...",
        "....bb....",
        "....bb....",
        "....bb...."]
def whale(d, cx, cy, wag):
    for x in range(cx - 22, cx + 24):
        u = (x - cx) / 22.0
        if abs(u) > 1: continue
        k = math.sqrt(1 - u * u)
        top = 11.0 * k * (0.45 + 0.55 * (u + 1) / 2)
        bot = 7.5 * k
        for y in range(int(cy - top) - 1, int(cy + bot) + 2):
            dy = y - cy
            if not (-top <= dy <= bot): continue
            edge = dy < -top + 1 or dy > bot - 1 or x <= cx - 21 or x >= cx + 22
            t = dy / max(top if dy < 0 else bot, 1)
            if edge: c = NAVY
            elif dy > bot - 2.2: c = B1
            elif dy < -top * 0.55: c = B3
            elif dy > 1.0 and u > -0.8 and dy < bot - 2.2: c = BELLY if dy < bot - 4 else LIGHT
            else: c = B2
            d.point((x, y), c)
    for r, row in enumerate(TAIL):
        for c_, ch in enumerate(row):
            if ch != ".":
                d.point((cx - 26 + c_, cy - 10 + r + wag), NAVY if (r == 0 or c_ in (0, 9)) else B2)
    ex, ey = cx + 12, cy - 3
    d.rectangle([ex, ey, ex + 2, ey + 2], WHITE); d.point((ex + 2, ey + 1), BLK); d.point((ex + 2, ey + 2), BLK)
    for k in range(5): d.point((ex - 2 + k, ey + 6 + (0 if 1 <= k <= 3 else -1)), NAVY)
    d.point((ex - 3, ey + 4), PINK); d.point((ex - 4, ey + 4), PINK)
def box(d, x, y, w, h, col, dark):
    d.rectangle([x, y, x + w - 1, y + h - 1], col)
    for k in range(2, w - 1, 2): d.line([(x + k, y + 1), (x + k, y + h - 2)], dark)
    d.line([(x, y + h - 1), (x + w - 1, y + h - 1)], dark)
DK = lambda c: tuple(v // 2 for v in c)
DUCK = [".yy..", "yyyyo", ".yyy.", ".yyy."]
def frame(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N
    sky(d, f, 32, 26, 71, 24)
    by = round(1.5 * math.sin(ph))
    wag = (0, 1, 2, 1)[(f // 5) % 4] - 1
    cx, cy = 33, 32 + by
    whale(d, cx, cy, wag)
    rows = [(24, cy - 14 + 0, [RED, YEL, BLUE]), ]
    for i, col in enumerate((RED, YEL, BLUE)): box(d, 21 + 7 * i + (i > 0), cy - 15 + 6, 7, 6, col, DK(col))
    for i, col in enumerate((GRN, ORG)): box(d, 25 + 8 * i, cy - 15, 7, 6, col, DK(col))
    jump = (0, 1, 0, 0)[(f // 6) % 4] if False else round(1.5 * abs(math.sin(2 * ph)))
    sprite(d, DUCK, 28, cy - 19 - jump, {"y": YEL, "o": ORG})
    d.point((29, cy - 18 - jump), BLK)
    for i in range(4):
        d.point((cx + 18 + i, cy - 12 - (f // 3 + i) % 3), LIGHT if (f // 3 + i) % 2 else B3)
    for x in range(S):
        y = cy + 8 + round(1.0 * math.sin(x * 0.5 - 2 * ph))
        d.point((x, y), B3 if x % 3 else B2); d.point((x, y + 1), B1 if (x + f) % 4 else B2)
    gemini_star(d, 54, 16 + round(2 * math.sin(ph)), 4, 2 * ph)
    minicloud(d, 4, 14 + round(2 * math.sin(ph + 2)))
    text1x(d, "GOOGLE CLOUD", 8, 2, YEL)
    text1x(d, "GEMINI", 20, 44, WHITE)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img
if __name__ == "__main__":
    fr = [frame(i) for i in range(N)]
    save(fr, "WHALE_v3")
    sh = Image.new("RGB", (256 * 3, 256))
    for k, fi in enumerate((0, 15, 40)): sh.paste(fr[fi].resize((256, 256), Image.NEAREST), (256 * k, 0))
    sh.save("/tmp/w3.png")
