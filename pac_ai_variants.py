# Three "Pac-G eats the AI logos" recipes on the black layout of the leaderboard #1.
#   A  BUFFET  - the G stays put and chomps a conveyor of logos, one every 15 frames
#   B  MODELS  - four logos chase the G, the G powers up, turns around and eats them (ghost-style)
#   C  NOM NOM - the G sweeps across one giant logo and erases it, the logo then re-forms
# Logos are tiny hand-drawn pixel glyphs (simplified interpretations, not official assets).
# 60 frames @ 100 ms, pure-black background, every animated element periodic over N -> seamless loop.
import math, os
from PIL import Image, ImageDraw
from led_kit import *
from recipe_top1_google_chomps_devoxx import g_logo

SPARK_C, RING_C, LOOP_C, BLOCK_C = (217, 119, 87), (16, 163, 127), (0, 100, 224), (250, 100, 15)
SCARED_C = (30, 60, 255)
LOGOS = [  # (rows, color)
    (["....c....", ".c..c..c.", "..c.c.c..", "...ccc...", "ccccccccc", "...ccc...", "..c.c.c..", ".c..c..c.", "....c...."], SPARK_C),
    (["..ccccc..", ".c.....c.", "c.......c", "c..ccc..c", "c..ccc..c", "c..ccc..c", "c.......c", ".c.....c.", "..ccccc.."], RING_C),
    ([".cc...cc.", "c..c.c..c", "c...c...c", "c..c.c..c", ".cc...cc."], LOOP_C),
    (["cc.....cc", "ccc...ccc", "cc.c.c.cc", "cc..c..cc", "cc.....cc"], BLOCK_C),
]
CY = 33

def sprite(d, rows, x, y, col, clip_lo=None, clip_hi=None, scale=1):
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == ".":
                continue
            for sy in range(scale):
                for sx in range(scale):
                    px, py = x + c * scale + sx, y + r * scale + sy
                    if (clip_lo is None or px >= clip_lo) and (clip_hi is None or px < clip_hi) and 0 <= px < S:
                        d.point((px, py), col)

def pac(img, cx, cy, rad, mouth, left=False, tint=None):
    """Google-G pac-man; draw on a scratch tile so it can be mirrored and tinted."""
    t = Image.new("RGB", (2 * rad + 5, 2 * rad + 5), BLK)
    td = ImageDraw.Draw(t)
    g_logo(td, rad + 2, rad + 2, rad, mouth)
    if left:
        t = t.transpose(Image.FLIP_LEFT_RIGHT)
    if tint:
        px = t.load()
        for y in range(t.height):
            for x in range(t.width):
                if px[x, y] != BLK:
                    px[x, y] = tint
    mask = t.convert("L").point(lambda v: 255 if v else 0)
    img.paste(t, (cx - rad - 2, cy - rad - 2), mask)

def burst(d, x, y, col, age):
    if 0 <= age < 6:
        for a in range(8):
            r = 2 + age * 2
            d.rectangle([x + round(r * math.cos(a * math.pi / 4)), y + round(r * math.sin(a * math.pi / 4)),
                         x + round(r * math.cos(a * math.pi / 4)) + 1, y + round(r * math.sin(a * math.pi / 4)) + 1], col)

def pellets(d, f, speed=3, mod=90):
    for k in range(mod // 6):
        x = (k * 6 - f * speed) % mod - 6
        d.rectangle([x, 33, x + 1, 34], (255, 235, 170))

# ---------------------------------------------------------------- A
def frame_a(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    frame_shell(d, f, "BUFFET", "DEVOXX")
    pellets(d, f, 2, 120)
    for k, (rows, col) in enumerate(LOGOS):
        x = 11 + ((k * 30 - 2 * f) % 120)
        if x < S:
            sprite(d, rows, x, CY - len(rows) // 2, col, clip_lo=19)
        burst(d, 19, CY, col, (f - 15 * k) % 60)
    pac(img, 11, CY, 8, 60 if (f // 2) % 2 else 20)
    return img

# ---------------------------------------------------------------- B
EAT = {}
def _eat_frames():
    for i in range(4):
        for f in range(18, 54):
            if 12 + i * 11 - (f - 18) // 2 + 8 >= 56 - 2 * (f - 18) - 8:
                EAT[i] = f; break
_eat_frames()

def chase(img, d, f, off=0):
    for i, (rows, col) in enumerate(LOGOS):
        sprite(d, rows, 12 + i * 11 + off + (f % 2), CY - len(rows) // 2, col)
    pac(img, 62 + off, CY, 6, 60 if (f // 2) % 2 else 20, tint=WHITE if f in (16, 17) else None)

def frame_b(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    frame_shell(d, f, "MODELS", "DEVOXX")
    pellets(d, f)
    if f < 18:
        chase(img, d, f)
    elif f < 54:
        gx = 56 - 2 * (f - 18)
        for i, (rows, col) in enumerate(LOGOS):
            lx = 12 + i * 11 - (f - 18) // 2
            age = f - EAT[i]
            y = CY - len(rows) // 2
            if age < 0:
                sprite(d, rows, lx, y, SCARED_C)
            elif age < 2:
                sprite(d, rows, lx, y, WHITE)
            else:
                burst(d, lx + 4, CY, col, age - 2)
        pac(img, gx, CY, 10, 70 if (f // 2) % 2 else 20, left=True)
    if f >= 54:
        chase(img, d, f, (N - f) * 10)
    return img

# ---------------------------------------------------------------- C
def frame_c(f):
    img = Image.new("RGB", (S, S), BLK); d = ImageDraw.Draw(img)
    frame_shell(d, f, "NOM NOM", "DEVOXX")
    pellets(d, f)
    rows, col = LOGOS[0]
    lx, ly = 23, 24
    gx = round(-10 + 2.1 * f)
    if f < 41:
        sprite(d, rows, lx, ly, col, clip_lo=gx + 6, scale=2)
        if 10 <= f <= 28:
            burst(d, gx + 9, CY, col, (f - 10) % 6)
        pac(img, gx, CY, 9, 60 if (f // 2) % 2 else 20)
    elif f >= 50:
        radius = (f - 49) * 2
        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                if ch != "." and math.hypot(lx + c * 2 + 1 - 32, ly + r * 2 + 1 - CY) <= radius:
                    d.rectangle([lx + c * 2, ly + r * 2, lx + c * 2 + 1, ly + r * 2 + 1], col)
    return img

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    for name, fn in [("PAC_A_buffet", frame_a), ("PAC_B_models", frame_b), ("PAC_C_nomnom", frame_c)]:
        out = [fn(i) for i in range(N)]
        out[0].save(f"output/{name}.gif", save_all=True, append_images=out[1:], duration=100, loop=0, disposal=1)
