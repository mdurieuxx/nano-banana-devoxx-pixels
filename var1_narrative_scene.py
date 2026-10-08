# VAR1 - "Build & Deploy": blocks stack into a rocket on a pad, ignition, launch, fireworks.
# Every animated element is periodic over N frames, so frame N-1 -> frame 0 is a seamless loop.
import math, os
from PIL import Image, ImageDraw
from common import S, G, text, lerp

N = 60
PINK, ORANGE, INDIGO = (233, 30, 99), (255, 152, 0), (63, 81, 181)
WHITE, CLOUD = (255, 255, 255), (235, 240, 255)
BLACK = (0, 0, 0)
GC = [G["blue"], G["red"], G["yellow"], G["green"]]

SKY_H = 46
STOPS = [INDIGO, G["blue"], PINK, ORANGE]
def sky_color(y):
    t = (y // 4) / (SKY_H // 4 - 1) * (len(STOPS) - 1)
    i = min(int(t), len(STOPS) - 2)
    return lerp(STOPS[i], STOPS[i + 1], t - i)

BUILDINGS = [(0, 8, 48), (8, 6, 45), (14, 8, 50), (42, 7, 47), (49, 6, 44), (55, 9, 49)]
PAD_Y = 58
BASE_Y = PAD_Y - 1                      # rocket sits on the pad
# (height, body color, accent color) from bottom to top
BLOCKS = [(5, G["red"], ORANGE), (6, WHITE, G["blue"]), (6, WHITE, G["yellow"]),
          (6, G["blue"], WHITE), (7, G["red"], G["yellow"])]

def block_slots():
    y, slots = BASE_Y, []
    for h, *_ in BLOCKS:
        y -= h
        slots.append(y)
    return slots
SLOTS = block_slots()

def draw_block(d, k, cx, y):
    h, body, accent = BLOCKS[k]
    x0, x1 = cx - 4, cx + 3
    if k == 4:                                     # nose cone
        for r in range(h):
            inset = min(3, (h - 1 - r) // 2)
            d.line([(x0 + inset, y + r), (x1 - inset, y + r)], body)
        d.line([(cx - 1, y + 3), (cx, y + 3)], accent)
        return
    d.rectangle([x0, y, x1, y + h - 1], body)
    if k == 0:                                     # fins
        d.rectangle([x0 - 2, y + 1, x0 - 1, y + h - 1], accent)
        d.rectangle([x1 + 1, y + 1, x1 + 2, y + h - 1], accent)
        d.rectangle([cx - 1, y + 1, cx, y + h - 1], BLACK)
    elif k == 2:                                   # porthole
        d.rectangle([cx - 1, y + 2, cx, y + 3], accent)
    else:
        d.line([(x0, y + h - 1), (x1, y + h - 1)], accent)

def frame(f):
    img = Image.new("RGB", (S, S), BLACK)
    d = ImageDraw.Draw(img)
    for y in range(SKY_H):
        d.line([(0, y), (S, y)], sky_color(y))
    # twinkling stars (2x2 so no isolated pixel)
    for i, (x, y) in enumerate([(3, 16), (58, 17), (12, 22), (51, 24), (60, 30), (6, 31)]):
        if (f // 3 + i) % 2:
            d.rectangle([x, y, x + 1, y + 1], WHITE)
    # drifting clouds, wrap at 64 px per loop
    for x0, y, w in [(8, 19, 12), (40, 29, 14)]:
        x = x0 + round(f * S / N)
        for xx in (x % S, x % S - S):
            d.rounded_rectangle([xx, y + 2, xx + w, y + 5], 2, CLOUD)
            d.ellipse([xx + 2, y, xx + 6, y + 4], CLOUD)
            d.ellipse([xx + 6, y - 1, xx + w - 2, y + 4], CLOUD)
    # skyline silhouettes (pure black) with blinking colored windows
    for bi, (x, w, top) in enumerate(BUILDINGS):
        d.rectangle([x, top, x + w - 1, S], BLACK)
        for wy in range(top + 2, 56, 3):
            for wx in range(x + 1, x + w - 1, 2):
                if (wx * 7 + wy * 3 + f // 5 + bi) % 3:
                    d.rectangle([wx, wy, wx, wy + 1], GC[(wx + wy) % 4])
    d.rectangle([22, PAD_Y, 41, S], BLACK)
    d.line([(24, PAD_Y), (39, PAD_Y)], ORANGE)
    d.line([(24, PAD_Y + 1), (39, PAD_Y + 1)], PINK)

    cx = 32
    launch = 30
    lift = 0 if f < launch else int((f - launch) ** 2 * 0.12)
    shake = (1 if f % 2 else -1) if 26 <= f < launch else 0
    # flame (under the rocket once ignited)
    if 26 <= f < 56:
        grow = min(6, (f - 26) + 2) + (f % 2)
        fy = BASE_Y + 1 - lift
        for r in range(grow):
            half = max(0, 3 - r // 2)
            col = G["yellow"] if r < 2 else ORANGE if r < 4 else G["red"]
            d.line([(cx + shake - half, fy + r), (cx + shake + half - 1, fy + r)], col)
    # stacking blocks, then the rocket flies off
    for k in range(len(BLOCKS)):
        s = f - (2 + 4 * k)
        if s < 0:
            continue
        drop = -(3 - s) * 5 if s < 4 else 0
        y = SLOTS[k] + drop - lift
        if y < S:
            draw_block(d, k, cx + shake, y)
    if 22 <= f < 26 and (f // 2) % 2:                # ready blink on the nose
        d.point((cx - 1, SLOTS[4] + 1), G["yellow"])
        d.point((cx, SLOTS[4] + 1), G["yellow"])
    # smoke at the pad
    for i in range(6):
        age = f - (launch + 2 * i)
        if 0 <= age <= 14:
            side = -1 if i % 2 else 1
            px = cx + side * (2 + age // 2 + i)
            r = 1 + age // 6
            d.ellipse([px - r, BASE_Y - r - 1 - age // 5, px + r, BASE_Y + r - age // 5], (240, 240, 245))
    # fireworks once the rocket is gone
    for bx, by, t0 in [(14, 26, 46), (50, 22, 49)]:
        age = f - t0
        if 0 <= age <= 8:
            rr = 1 + age
            for a in range(8):
                px = bx + round(rr * math.cos(a * math.pi / 4))
                py = by + round(rr * math.sin(a * math.pi / 4))
                d.rectangle([px, py, px + 1, py + 1], GC[(a + age // 2) % 4])
    text(img, "DEVOXX", 3, 2, GC[:2] + GC[2:] + GC[:2])
    text(img, "GOOGLE CLOUD", 8, 9, WHITE)
    return img

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    out = [frame(i) for i in range(N)]
    out[0].save("output/VAR1_narrative_scene.gif", save_all=True, append_images=out[1:],
                duration=90, loop=0, disposal=1)
