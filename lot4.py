import math
from PIL import Image, ImageDraw
from led_kit import *
from marc_lot import sky, ring, COLS, sprite_rows, ROBOT, save
from friend_g_nightsky import text1x

WORDS = [("GEMINI", 20), ("GOOGLE CLOUD", 8), ("ANTIGRAVITY", 10)]

def base():
    return Image.new("RGB", (S, S), BLK)

def frame_m4a(f):
    img = base(); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N; cx, cy = 32, 22
    sky(d, f, cx, cy, 41, 16)
    ring(d, cx, cy, 15, 3, ph + math.pi / 3)
    gemini_star(d, cx, cy, 9 + round(2 * math.sin(2 * ph)), -ph)
    d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], WHITE)
    for k in range(6):
        a = -ph + k * math.pi / 3
        x, y = round(cx + 25 * math.cos(a)), round(cy + 8 * math.sin(a))
        if 1 <= y <= 40:
            d.rectangle([x - 1, y - 1, x, y], COLS[k % 4])
    w, x = WORDS[(f // 20) % 3]
    text1x(d, w, x, 43, YEL)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

def frame_m4b(f):
    img = base(); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N; cx = 32; cy = 22 + round(3 * math.sin(ph))
    sky(d, f, 32, 22, 23, 15)
    for k in range(7):
        a = ph + k * 2 * math.pi / 7
        x, y = round(cx + 22 * math.cos(a)), round(cy + 7 * math.sin(a) - 4)
        if 1 <= y <= 40 and not (abs(x - cx) < 10 and abs(y - cy) < 10):
            d.rectangle([x - 1, y - 1, x + 1, y], COLS[k % 4])
    for dy in range(-10, 11):
        for dx in range(-10, 11):
            if dx * dx + dy * dy <= 100:
                d.point((cx + dx, cy + dy), BLUE if dy < -3 else YEL if dy < 0 else GRN if dy < 4 else RED)
    gemini_star(d, cx + round(17 * math.cos(-ph)), cy - 3 + round(6 * math.sin(-ph)), 4, 2 * ph)
    for k in range(7):
        a = ph + k * 2 * math.pi / 7
        x, y = round(cx + 22 * math.cos(a)), round(cy + 7 * math.sin(a) - 4)
        if 1 <= y <= 40 and math.sin(a) > 0 and abs(x - cx) < 10 and abs(y - cy) < 10:
            d.rectangle([x - 1, y - 1, x + 1, y], COLS[k % 4])
    text1x(d, "GEMINI", 20, 43, YEL)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

def frame_m4c(f):
    img = base(); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N; cx, cy = 32, 21
    sky(d, f, cx, cy, 53, 17)
    ring(d, cx, cy, 18, 2, -ph)
    rows = list(ROBOT)
    if (f // 3) % 10 == 0:
        rows[2] = rows[3] = "bbbbbbbbbbb"
    if (f // 5) % 2:
        rows[7] = "gggggggggg."; rows[8] = "gggyggggygg"
    pal = {"b": BLUE, "y": YEL, "r": RED, "g": GRN}
    bob = round(1.5 * math.sin(2 * ph))
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != ".":
                d.rectangle([cx - 11 + 2 * c, cy - 10 + bob + 2 * r, cx - 10 + 2 * c, cy - 9 + bob + 2 * r], pal[ch])
    gemini_star(d, cx + round(14 * math.cos(2 * ph)), cy - 12 + round(3 * math.sin(2 * ph)), 3, 3 * ph)
    text1x(d, "GEMINI", 20, 43, YEL)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

def frame_f1(f):
    img = base(); d = ImageDraw.Draw(img)
    cx, cy = 32, 21
    for k in range(5):
        r = 2 + ((f + 12 * k) % N) * 19 // N
        for a in range(0, 360, 3):
            x, y = round(cx + r * math.cos(math.radians(a))), round(cy + r * math.sin(math.radians(a)))
            if 0 <= y <= 41:
                d.point((x, y), COLS[k % 4])
    ph = 2 * math.pi * f / N
    gemini_star(d, cx, cy, 6 + round(1 * math.sin(2 * ph)), ph)
    text1x(d, "GEMINI", 20, 43, YEL)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

def frame_f2(f):
    img = base(); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N
    for k in range(2):
        text2x(d, "DEVOXX GEMINI", -(2 * f) % 120 - 120 + k * 120 + 2, 3, BRAND)
    gemini_star(d, 32, 27, 8 + round(2 * math.sin(2 * ph)), ph)
    for i in range(16):
        h = 3 + round(12 * abs(math.sin(ph * (1 + i % 3) + i * 0.7)))
        d.rectangle([1 + i * 4, 62 - h, 3 + i * 4, 62], COLS[i % 4])
    return img

def frame_f3(f):
    img = base(); d = ImageDraw.Draw(img)
    cx, cy = 32, 21; ph = 2 * math.pi * f / N
    for r in (7, 13, 19):
        for a in range(0, 360, 2):
            d.point((round(cx + r * math.cos(math.radians(a))), round(cy + r * math.sin(math.radians(a)))), BLUE)
    for t in range(0, 40, 2):
        a = -ph + t * 0.02
        col = GRN
        for rr in range(2, 20):
            d.point((round(cx + rr * math.cos(a)), round(cy + rr * math.sin(a))), col)
    for k, (rr, aa, c) in enumerate([(11, 0.8, RED), (16, 2.4, YEL), (8, 4.0, GRN), (17, 5.3, BLUE)]):
        diff = (((-ph) - aa) % (2 * math.pi))
        if diff < 2.8:
            x, y = round(cx + rr * math.cos(aa)), round(cy + rr * math.sin(aa))
            d.rectangle([x - 1, y - 1, x, y], c)
    gemini_star(d, cx, cy, 3, 2 * ph)
    text1x(d, "GEMINI", 20, 43, YEL)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

if __name__ == "__main__":
    for nm, fn in [("M4_A_cycle", frame_m4a), ("M4_B_planet_gemini", frame_m4b), ("M4_C_robot_big", frame_m4c),
                   ("F4_tunnel", frame_f1), ("F4_marquee_eq", frame_f2), ("F4_radar", frame_f3)]:
        save([fn(i) for i in range(N)], nm)

def frame_f4(f):
    img = base(); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N; cx, cy = 32, 21
    sky(d, f, cx, cy, 77, 20)
    ring(d, cx, cy, 20, 3, ph)
    gemini_star(d, cx, cy, 7 + round(1 * math.sin(2 * ph)), -2 * ph)
    for k in range(4):
        a = -2 * ph + k * math.pi / 2
        d.rectangle([round(cx + 12 * math.cos(a)) - 1, round(cy + 12 * math.sin(a)) - 1, round(cx + 12 * math.cos(a)), round(cy + 12 * math.sin(a))], COLS[(k + 2) % 4])
    text1x(d, "GEMINI", 20, 43, WHITE)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

if __name__ == "__main__":
    save([frame_f4(i) for i in range(N)], "F4_ring")
