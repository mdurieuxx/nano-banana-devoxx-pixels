# Two black-background "single subject" animations (no rules/title band): MARC_A_orbit_cloud, MARC_B_antigravity.
import math, os, random
from PIL import Image, ImageDraw
from led_kit import *
from friend_g_nightsky import text1x
LETTER["C"] = FONT["C"]
COLS = [BLUE, RED, YEL, GRN]

def sky(d, f, cx, cy, seed, avoid=17):
    rng = random.Random(seed)
    for _ in range(26):
        x, y, k, off, col = rng.randrange(1, 63), rng.randrange(1, 40), rng.randrange(1, 4), rng.randrange(0, 60), rng.choice(COLS)
        if math.hypot(x - cx, y - cy) > avoid and ((f + off) // (6 * k)) % 2 == 0 and (f + off) % 3 != 0:
            d.point((x, y), col)

def ring(d, cx, cy, r, th, rot):
    for dy in range(-r - 1, r + 2):
        for dx in range(-r - 1, r + 2):
            dist = math.hypot(dx, dy)
            if r - th < dist <= r:
                ang = (math.degrees(math.atan2(dy, dx)) - math.degrees(rot)) % 360
                d.point((cx + dx, cy + dy), COLS[int(ang // 90) % 4])

def frame_a(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N; cx, cy = 32, 22
    sky(d, f, cx, cy, 11)
    ring(d, cx, cy, 17, 4, ph)
    gemini_star(d, cx, cy, 7 + round(2 * math.sin(2 * ph)), -2 * ph)
    d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], YEL)
    for k in range(6):
        a = -ph + k * math.pi / 3
        x, y = round(cx + 24 * math.cos(a)), round(cy + 5 * math.sin(a) + 10 * math.sin(a / 1.0) * 0)
        if 1 <= y <= 40:
            d.rectangle([x - 1, y - 1, x, y], COLS[k % 4])
    text1x(d, "GOOGLE CLOUD", 8, 43, YEL)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

def frame_b(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N; cx = 32; cy = 22 + round(3 * math.sin(ph))
    sky(d, f, 32, 22, 23, 15)
    for k in range(7):                                   # debris floating around the levitating planet
        a = ph + k * 2 * math.pi / 7
        x, y = round(cx + 22 * math.cos(a)), round(cy + 7 * math.sin(a) - 4)
        if 1 <= y <= 40 and not (abs(x - cx) < 10 and abs(y - cy) < 10):
            d.rectangle([x - 1, y - 1, x + 1, y], COLS[k % 4])
    for dy in range(-10, 11):                            # planet: flat-shaded bands
        for dx in range(-10, 11):
            if dx * dx + dy * dy <= 100:
                col = BLUE if dy < -3 else YEL if dy < 0 else GRN if dy < 4 else RED
                d.point((cx + dx, cy + dy), col)
    gemini_star(d, cx + round(17 * math.cos(-ph)), cy - 3 + round(6 * math.sin(-ph)), 4, 2 * ph)
    for k in range(7):                                   # ring in front of the planet
        a = ph + k * 2 * math.pi / 7
        x, y = round(cx + 22 * math.cos(a)), round(cy + 7 * math.sin(a) - 4)
        if 1 <= y <= 40 and math.sin(a) > 0 and abs(x - cx) < 10 and abs(y - cy) < 10:
            d.rectangle([x - 1, y - 1, x + 1, y], COLS[k % 4])
    text1x(d, "ANTIGRAVITY", 10, 43, YEL)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

def save(fr, name):
    fr[0].save(f"output/{name}.gif", save_all=True, append_images=fr[1:], duration=100, loop=0, disposal=1)

if __name__ == "__main__":
    save([frame_a(i) for i in range(N)], "MARC_A_orbit_cloud")
    save([frame_b(i) for i in range(N)], "MARC_B_antigravity")

# ---- lot 02 test: coloured (non-black) background, horizontal marquee + equalizer bars, different layout from the rest
BG = (45, 25, 120)
def frame_c(f):
    img = Image.new("RGB", (S, S), BG); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N
    for k in range(2):
        text2x(d, "DEVOXX GEMINI", -(2 * f) % 120 - 120 + k * 120 + 2, 8, BRAND)
    gemini_star(d, 32, 25, 7 + round(2 * math.sin(2 * ph)), ph)
    for i in range(14):
        h = 4 + round(14 * abs(math.sin(ph * (1 + i % 3) + i * 0.7)))
        d.rectangle([2 + i * 4, 62 - h, 4 + i * 4, 62], COLS[i % 4])
    return img

if __name__ == "__main__":
    save([frame_c(i) for i in range(N)], "MARC_C_colour_bg")

# ---- lot 03: A variant with the readable word GEMINI (theme), ring/star counter-rotated so it is not a near-duplicate of A
def frame_a2(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N; cx, cy = 32, 22
    sky(d, f, cx, cy, 31)
    ring(d, cx, cy, 17, 4, -ph + math.pi / 4)
    gemini_star(d, cx, cy, 8 + round(2 * math.sin(3 * ph)), 3 * ph)
    d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], YEL)
    for k in range(8):
        a = ph + k * math.pi / 4
        x, y = round(cx + 24 * math.cos(a)), round(cy + 7 * math.sin(a))
        if 1 <= y <= 40:
            d.rectangle([x - 1, y - 1, x, y], COLS[(k + 1) % 4])
    text1x(d, "GEMINI", 20, 43, YEL)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

if __name__ == "__main__":
    save([frame_a2(i) for i in range(N)], "MARC_A2_gemini")

# ---- lot 03 probe: A2 with a small robot mascot (character animation) in the ring, to test the AES bar
ROBOT = [".bbbbbbbbb.", "bbbbbbbbbbb", "bbyybbbyybb", "bbyybbbyybb", "bbbbrrrbbbb", ".bbbbbbbbb.",
         "..ggggggg..", ".gggggggggg", "gggyggggygg", ".gg.....gg."]
def sprite_rows(d, rows, x0, y0, pal):
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != ".":
                d.point((x0 + c, y0 + r), pal[ch])

def frame_a3(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    ph = 2 * math.pi * f / N; cx, cy = 32, 22
    sky(d, f, cx, cy, 31)
    ring(d, cx, cy, 17, 4, -ph + math.pi / 4)
    rows = list(ROBOT)
    if (f // 3) % 10 == 0:                                   # blink
        rows[2] = rows[3] = "bbbbbbbbbbb"
    if (f // 5) % 2:                                         # waving arm
        rows[7] = "gggggggggg."; rows[8] = "gggyggggygg"
    sprite_rows(d, rows, cx - 5, cy - 4, {"b": BLUE, "y": YEL, "r": RED, "g": GRN})
    bob = round(1.5 * math.sin(2 * ph))
    gemini_star(d, cx, cy - 10 + bob, 3, 3 * ph)
    for k in range(8):
        a = ph + k * math.pi / 4
        x, y = round(cx + 24 * math.cos(a)), round(cy + 7 * math.sin(a))
        if 1 <= y <= 40:
            d.rectangle([x - 1, y - 1, x, y], COLS[(k + 1) % 4])
    text1x(d, "GEMINI", 20, 43, YEL)
    text2x(d, "DEVOXX", 9, 53, BRAND)
    return img

if __name__ == "__main__":
    save([frame_a3(i) for i in range(N)], "MARC_A3_robot")
