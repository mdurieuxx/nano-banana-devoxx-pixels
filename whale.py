import math
from PIL import Image, ImageDraw
from led_kit import *
from marc_lot import sky, COLS, save
from friend_g_nightsky import text1x
DB, DL, DD = (4, 164, 244), (180, 244, 252), (4, 92, 164)
K8S, ORG = (50, 108, 229), (252, 120, 4)
WHALE = ["..........bbbbbbb.....",
         ".b.......bbbbbbbbbb...",
         ".bb.....bbbbbbbbbbbb..",
         "..bb...bbbbbbbbbbbbbb.",
         "..bbb.bbbbbbbbbbbbbbb.",
         "...bbbbbbbbbbbbbbbwkbb",
         "....bbbbbbbbbbbbbbbbb.",
         "....blllllllllllllllb.",
         ".....blllllllllllllb..",
         "......bblllllllllbb...",
         "........bbbbbbbbb....."]
WP = {"b": DB, "l": DL, "w": WHITE, "k": BLK}
def sprite(d, rows, x0, y0, pal):
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != ".": d.point((x0 + c, y0 + r), pal[ch])
CLOUD = [".....bb......", "...bbbbbb.bb.", "..bbbbbbbbbbb", ".bbbbbbbbbbbb", "bbbbbbbbbbbbb", ".bbbbbbbbbbb."]
def cloud(d, x0, y0):
    for r, row in enumerate(CLOUD):
        for c, ch in enumerate(row):
            if ch != ".": d.point((x0 + c, y0 + r), COLS[min(3, c // 4)])
def helm(d, cx, cy, rot):
    for dy in range(-4, 5):
        for dx in range(-4, 5):
            if dx * dx + dy * dy <= 17: d.point((cx + dx, cy + dy), K8S)
    for k in range(7):
        a = rot + k * 2 * math.pi / 7
        d.line([(cx, cy), (round(cx + 3 * math.cos(a)), round(cy + 3 * math.sin(a)))], WHITE)
CUP = ["..r.r..", "...r.r.", "wwwwww.", "wwwwwww", "wwwwww.", ".wwww..", "wwwwwww"]
def frame(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N
    sky(d, f, 32, 22, 29, 12)
    gemini_star(d, 8, 12 + round(2 * math.sin(ph)), 4, 2 * ph)
    cloud(d, 17, 8 + round(2 * math.sin(ph + 1.5)))
    helm(d, 41, 12 + round(2 * math.sin(ph + 3)), ph)
    sprite(d, CUP, 51, 9 + round(2 * math.sin(ph + 4.5)), {"r": RED, "w": WHITE})
    by = 25 + round(1.5 * math.sin(2 * ph))
    sprite(d, WHALE, 18, by, WP)
    for i, (cx, col) in enumerate([(24, RED), (28, YEL), (32, GRN)]):
        d.rectangle([cx, by - 3, cx + 3, by - 1], col)
    d.rectangle([27, by - 6, 30, by - 4], BLUE); d.rectangle([31, by - 6, 34, by - 4], ORG)
    sx = 38 + 3 * math.cos(2 * ph)
    for k in range(3):
        d.point((round(sx) + k, by - 8 + (k % 2)), DL)
    for x in range(S):
        y = 37 + round(1.2 * math.sin(x * 0.45 - 2 * ph))
        d.point((x, y), DB if x % 3 else DD)
        d.point((x, y + 2), DD if (x + f) % 4 else DB)
    text1x(d, "GOOGLE", 20, 2, YEL)
    text1x(d, "GEMINI", 20, 43, WHITE)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img
if __name__ == "__main__":
    save([frame(i) for i in range(N)], "WHALE_partners")
    frame(12).resize((256, 256), Image.NEAREST).save("/tmp/whale_prev.png")

def frame_anti(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N
    sky(d, f, 32, 22, 29, 12)
    gemini_star(d, 8, 14 + round(2 * math.sin(ph)), 4, 2 * ph)
    cloud(d, 17, 10 + round(2 * math.sin(ph + 1.5)))
    helm(d, 41, 14 + round(2 * math.sin(ph + 3)), ph)
    sprite(d, CUP, 51, 11 + round(2 * math.sin(ph + 4.5)), {"r": RED, "w": WHITE})
    by = 26 + round(2 * math.sin(2 * ph))
    sprite(d, WHALE, 18, by, WP)
    for i, (cx, col) in enumerate([(22, RED), (27, YEL), (32, GRN), (37, BLUE)]):
        yy = by - 6 - round(2 + 2 * math.sin(2 * ph + i * 1.3))
        d.rectangle([cx, yy, cx + 3, yy + 2], col)
    for i in range(4):
        d.point((29 + 3 * i, by + 12 + (f // 2 + i) % 3), DL)
    for x in range(S):
        y = 38 + round(1.0 * math.sin(x * 0.45 - 2 * ph))
        d.point((x, y), DB if x % 3 else DD)
    text1x(d, "GOOGLE GEMINI", 6, 1, YEL)
    text1x(d, "ANTIGRAVITY", 10, 43, WHITE)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

if __name__ == "__main__":
    save([frame_anti(i) for i in range(N)], "WHALE_antigravity")
    frame_anti(12).resize((256, 256), Image.NEAREST).save("/tmp/whale_anti_prev.png")
