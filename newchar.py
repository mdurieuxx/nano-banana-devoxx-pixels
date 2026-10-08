import math
from PIL import Image, ImageDraw
from led_kit import *
import random
from marc_lot import COLS, save
from friend_g_nightsky import text1x
ORG = (252, 120, 4)
BY, BO, BG_, BRN = (255, 226, 40), (236, 150, 8), (96, 200, 64), (150, 90, 20)
def _banana():
    W, H = 30, 20
    g = [["."] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            px = x - 14.5
            if (px / 15.0) ** 2 + ((y - 5) / 14.5) ** 2 <= 1 and not (px / 14.0) ** 2 + ((y - 0.5) / 10.0) ** 2 <= 1 and y >= 2:
                g[y][x] = "y"
    for y in range(H):
        for x in range(W):
            if g[y][x] == "y":
                nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
                if any(not (0 <= a < W and 0 <= b < H) or g[b][a] == "." for a, b in nb): g[y][x] = "o"
    g[0][0] = g[0][1] = g[1][0] = g[1][1] = "g"; g[2][0] = g[2][1] = "g"
    g[0][28] = g[0][29] = g[1][28] = g[1][29] = g[2][28] = g[2][29] = "n"
    for y, xs in ((12, range(7, 13)), (12, range(17, 23)), (13, range(7, 13)), (13, range(17, 23))):
        for x in xs: g[y][x] = "k"
    g[12][8] = g[12][18] = "w"
    for x in range(13, 17): g[12][x] = "k"
    for x in (12, 13, 14, 15, 16, 17): g[16][x] = "r"
    g[15][11] = g[15][18] = "r"
    return ["".join(r) for r in g]
BANANA = _banana()
BP = {"n": BRN, "g": BG_, "y": BY, "o": BO, "k": BLK, "w": WHITE, "r": RED}
def sky(d, f, cx, cy, seed, avoid=17):
    rng = random.Random(seed)
    for _ in range(26):
        x, y, k, off, col = rng.randrange(1, 63), rng.randrange(1, 40), rng.choice((1, 5)), rng.randrange(0, 60), rng.choice(COLS)
        if math.hypot(x - cx, y - cy) > avoid and ((f + off) // (6 * k)) % 2 == 0 and (f + off) % 3 != 0:
            d.point((x, y), col)
def sprite(d, rows, x0, y0, pal):
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != ".": d.point((x0 + c, y0 + r), pal[ch])
MINI = [".bb....", "bbbbbb.", "bbbbbbb", ".bbbbb."]
def minicloud(d, x0, y0):
    for r, row in enumerate(MINI):
        for c, ch in enumerate(row):
            if ch != ".": d.point((x0 + c, y0 + r), COLS[(c // 2 + r) % 4])
def kw_bottom(d, f, word="GEMINI"):
    text1x(d, word, 32 - 2 * len(word), 43, WHITE if word == "GEMINI" else YEL)
def frame_banana(f, word="GEMINI", sgn=1):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N
    sky(d, f, 32, 24, 41, 19)
    bx, by = 17, 15 + round(2 * math.sin(ph))
    for i, dx in enumerate((11, 13, 15, 17)):
        ln = 2 + (f + i * 2) % 3
        for k in range(ln):
            d.point((bx + dx, by + 20 + k), (YEL, ORG, RED)[min(2, k * 3 // max(ln, 1))])
    sprite(d, BANANA, bx, by, BP)
    ox, oy = 32 + 24 * math.cos(sgn * ph), 24 + 12 * math.sin(sgn * ph)
    gemini_star(d, round(ox), round(oy), 3, 2 * ph)
    cx2, cy2 = 32 - 24 * math.cos(sgn * ph), 24 - 12 * math.sin(sgn * ph)
    minicloud(d, round(cx2) - 3, round(cy2) - 2)
    text1x(d, "GOOGLE CLOUD", 8, 2, YEL)
    kw_bottom(d, f, word)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img
if __name__ == "__main__":
    save([frame_banana(i) for i in range(N)], "NEW_banana")
    save([frame_banana(i, "ANTIGRAVITY", -1) for i in range(N)], "NEW_banana_b")
    Image.fromarray if False else None
    sheet = Image.new("RGB", (256 * 3, 256))
    for k, fr in enumerate((0, 12, 30)): sheet.paste(frame_banana(fr).resize((256, 256), Image.NEAREST), (256 * k, 0))
    sheet.save("/tmp/banana_prev.png")

RB, RD, RC = (4, 164, 244), (4, 92, 164), (120, 236, 252)
ROBO = ["......r.......",
        "......b.......",
        "..bbbbbbbbbb..",
        ".bbbbbbbbbbbb.",
        ".bwwwbbbbwwwb.",
        ".bwkcbbbbwkcb.",
        ".bwwwbbbbwwwb.",
        ".bbbbbbbbbbbb.",
        ".bbbrrrrrrbbb.",
        "..bbbbbbbbbb..",
        "...dddddddd..."]
RP = {"b": RB, "d": RD, "w": WHITE, "k": BLK, "c": RC, "r": RED}
def _mini():
    return ["g.......n",
            "yy.....yy",
            "yyy...yyy",
            "oyyyyyyyo",
            ".oyyyyyo.",
            "..ooooo.."]
MINIB = _mini()
def frame_coder(f, buddy=False):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N
    sky(d, f, 32, 26, 53, 21)
    hy = 11 + round(1 * math.sin(2 * ph))
    sprite(d, ROBO, 25, hy, RP)
    if (f // 6) % 2 == 0: d.point((31, hy), BLK)
    for dx in (-1, 0): d.rectangle([22 + dx, hy + 9, 23 + dx, hy + 12], RB)
    for dx in (0, 1): d.rectangle([40 + dx, hy + 9, 41 + dx, hy + 12], RB)
    d.rectangle([20, 24, 43, 35], (150, 70, 240)); d.rectangle([21, 25, 42, 34], BLK)
    for k in range(5):
        y = 26 + k * 2
        ln = 3 + ((f // 2 + k * 5) % 10)
        d.line([(23, y), (23 + ln, y)], COLS[(k + f // 15) % 4])
    gemini_star(d, 38, 29, 3, 2 * ph)
    d.rectangle([17, 36, 46, 38], (240, 70, 200)); d.line([(17, 39), (46, 39)], (110, 40, 170))
    for k in range(4):
        if (f // 2 + k) % 3 == 0: d.point((22 + k * 7, 37), WHITE)
    for k in range(0 if buddy else 3):
        d.point((53 + (1 if (f // 5 + k) % 2 else 0), 27 - k * 3 - (f // 5) % 3), RC)
    if buddy:
        mb = MINIB; yy = 29 + round(2 * math.sin(2 * ph))
        sprite(d, mb, 52, yy, BP)
        for i, dx in enumerate((3, 4, 5)): d.point((52 + dx, yy + 6 + (f + i) % 2), (YEL, ORG, RED)[(f + i) % 3])
    else:
        d.rectangle([51, 31, 55, 37], ORG); d.rectangle([56, 32, 57, 35], ORG); d.point((56, 33), BLK); d.point((56, 34), BLK)
        d.rectangle([52, 31, 54, 32], (150, 90, 20))
    cx2, cy2 = 32 + 27 * math.cos(ph), 20 + 9 * math.sin(ph)
    minicloud(d, round(cx2) - 3, round(cy2) - 2)
    gemini_star(d, round(64 - cx2) , round(40 - cy2) if False else round(20 - 9 * math.sin(ph)), 3, 2 * ph)
    text1x(d, "GOOGLE CLOUD", 8, 2, YEL)
    kw_bottom(d, f)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img
if __name__ == "__main__":
    save([frame_coder(i) for i in range(N)], "NEW_coder")
    save([frame_coder(i, True) for i in range(N)], "NEW_coder_b")
    sheet = Image.new("RGB", (256 * 3, 256))
    for k, fr in enumerate((0, 12, 36)): sheet.paste(frame_coder(fr).resize((256, 256), Image.NEAREST), (256 * k, 0))
    sheet.save("/tmp/coder_prev.png")
