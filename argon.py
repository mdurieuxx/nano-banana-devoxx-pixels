import math
from PIL import Image, ImageDraw
from led_kit import *
from marc_lot import sky, COLS, save
from friend_g_nightsky import text1x
LETTER.update({"1": ["010", "110", "010", "010", "111"], "8": ["111", "101", "111", "101", "111"],
               "r": ["000", "110", "101", "100", "100"]})
TX, TY, TW, TH = 19, 8, 26, 30

def big(d, s, x, y, col):
    for ch in s:
        for r, row in enumerate(LETTER[ch]):
            for c, v in enumerate(row):
                if v == "1":
                    d.rectangle([x + c * 3, y + r * 3, x + c * 3 + 2, y + r * 3 + 2], col)
        x += 13 if ch == "A" else 10

def frame_argon(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N; cx, cy = 32, 22
    sky(d, f, cx, cy, 61, 19)
    per = [(x, TY) for x in range(TX, TX + TW)] + [(TX + TW - 1, y) for y in range(TY + 1, TY + TH)] + \
          [(x, TY + TH - 1) for x in range(TX + TW - 2, TX - 1, -1)] + [(TX, y) for y in range(TY + TH - 2, TY, -1)]
    for i, p in enumerate(per):
        d.point(p, COLS[((i + 2 * f) // 7) % 4])
    text1x(d, "18", TX + 3, TY + 3, WHITE)
    big(d, "Ar", TX + 3, TY + 9, YEL)
    text1x(d, "ARGON", TX + 3, TY + 24, BLUE)
    for k, sx in enumerate((8, 56)):
        gemini_star(d, sx, 22 + round(3 * math.sin(ph + k * math.pi)), 4 + round(math.sin(2 * ph)), (1 if k else -1) * 2 * ph)
    for k in range(2):
        a = ph * 2 + k * math.pi
        x, y = round(cx + 22 * math.cos(a)), round(cy + 15 * math.sin(a))
        if 8 <= y <= 36 and not (TX - 1 <= x <= TX + TW and TY - 1 <= y <= TY + TH):
            d.rectangle([x - 1, y - 1, x, y], [RED, GRN][k])
    text1x(d, "GOOGLE", 20, 2, YEL)
    text1x(d, "GEMINI", 20, 43, WHITE)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

if __name__ == "__main__":
    save([frame_argon(i) for i in range(N)], "ARGON_tile")
    frame_argon(10).resize((256, 256), Image.NEAREST).save("/tmp/argon_prev.png")

from marc_lot import ROBOT
def frame_argon_robot(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N; cx, cy = 34, 21
    tx, ty, tw, th = 25, 8, 24, 30
    sky(d, f, cx, cy, 67, 17)
    per = [(x, ty) for x in range(tx, tx + tw)] + [(tx + tw - 1, y) for y in range(ty + 1, ty + th)] + \
          [(x, ty + th - 1) for x in range(tx + tw - 2, tx - 1, -1)] + [(tx, y) for y in range(ty + th - 2, ty, -1)]
    for i, p in enumerate(per):
        d.point(p, COLS[((i + 2 * f) // 7) % 4])
    text1x(d, "18", tx + 3, ty + 2, WHITE)
    big(d, "Ar", tx + 2, ty + 7, YEL)
    text1x(d, "ARGON", tx + 3, ty + 23, BLUE)
    rows = list(ROBOT)
    if (f // 3) % 10 == 0:
        rows[2] = rows[3] = "bbbbbbbbbbb"
    if (f // 5) % 2:
        rows[7] = "gggggggggg."; rows[8] = "gggyggggygg"
    bob = round(1.2 * math.sin(2 * ph))
    pal = {"b": BLUE, "y": YEL, "r": RED, "g": GRN}
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != ".":
                d.point((6 + c, 26 + bob + r), pal[ch])
    gemini_star(d, 6 + 5, 14 + bob, 3, 3 * ph)
    gemini_star(d, 57, 20 + round(3 * math.sin(ph)), 4 + round(math.sin(2 * ph)), -2 * ph)
    for k in range(2):
        a = ph * 2 + k * math.pi
        x, y = round(cx + 22 * math.cos(a)), round(cy + 16 * math.sin(a))
        if 8 <= y <= 38 and not (tx - 1 <= x <= tx + tw and ty - 1 <= y <= ty + th) and x > 17:
            d.rectangle([x - 1, y - 1, x, y], [RED, GRN][k])
    text1x(d, "GOOGLE", 20, 2, YEL)
    text1x(d, "GEMINI", 20, 43, WHITE)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

if __name__ == "__main__":
    save([frame_argon_robot(i) for i in range(N)], "ARGON_robot")
    frame_argon_robot(10).resize((256, 256), Image.NEAREST).save("/tmp/argon_robot_prev.png")
