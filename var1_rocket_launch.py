# VAR1 - "Launch to Gemini": a pixel rocket on a DEVOXX pad counts down, climbs the full height of the
# matrix, bursts into a Gemini star, the star collapses and the rocket is rebuilt on the pad (seamless loop).
# Black background (~80% pure #000000), exact Google palette, 60 frames @ 100 ms.
import os
from PIL import Image, ImageDraw
from led_kit import *

ROCKET = ["....r....", "...rrr...", "...rrr...", "..rrrrr..", "..wwwww..", "..wbbbw..", "..wbbbw..",
          "..wwwww..", "..wyyyw..", "..wwwww..", ".rwwwwwr.", "rrwwwwwrr", "rr.www.rr", "...yyy..."]
PAL = {"r": RED, "w": WHITE, "b": BLUE, "y": YEL, "g": GRN}
PAD_Y = 49                      # nozzle bottom row = 48, pad underneath
CX = 32
LAUNCH, BURST, COLLAPSE, REBUILD = 10, 36, 48, 54

def rocket_top(f):
    lift = 0 if f < LAUNCH or f >= REBUILD else round(20 * (min(f, BURST) - LAUNCH) ** 2 / (BURST - LAUNCH) ** 2)
    return PAD_Y - len(ROCKET) - lift

def frame(f):
    img = Image.new("RGB", (S, S), BLK)
    d = ImageDraw.Draw(img)
    frame_shell(d, f, "GOOGLE", "DEVOXX")
    # stars drifting down the band (35 rows per loop -> periodic), faster feeling while the rocket climbs
    for i, (x, y0) in enumerate([(6, 3), (56, 9), (12, 17), (52, 24), (58, 30), (4, 12), (30, 27), (44, 6)]):
        y = 15 + (y0 + round(f * 35 / N)) % 35
        if 20 <= x <= 44 and PAD_Y - 16 <= y <= PAD_Y:                  # keep the pad area clean
            continue
        d.rectangle([x, y, x + 1, y + 1], [BLUE, YEL, RED, GRN][i % 4])
    d.rectangle([26, PAD_Y, 38, PAD_Y + 1], GRN)                      # pad
    if f < LAUNCH:                                                    # countdown lights
        for k, col in enumerate([RED, YEL, GRN]):
            if f >= 2 + 3 * k:
                d.rectangle([10 + k * 4, 44, 12 + k * 4, 46], col)
    top = rocket_top(f)
    visible_rows = len(ROCKET)
    if f >= REBUILD:
        visible_rows = (f - REBUILD + 1) * len(ROCKET) // (N - REBUILD)
    if f < BURST or f >= REBUILD:
        if f >= LAUNCH and f < BURST:                                  # flame
            for r in range(3 + (f % 2) * 2 + min(4, (f - LAUNCH) // 3)):
                half = max(0, 2 - r // 2)
                d.line([(CX - half, top + len(ROCKET) + r), (CX + half, top + len(ROCKET) + r)], YEL if r < 2 else RED)
        for r in range(len(ROCKET) - visible_rows if f >= REBUILD else 0, len(ROCKET)):
            row = ROCKET[r]
            for c, ch in enumerate(row):
                if ch != ".":
                    d.point((CX - 4 + c, top + r), PAL[ch])
    cy = PAD_Y - len(ROCKET) - 20 + 5
    if BURST <= f < COLLAPSE:                                          # burst into a Gemini star
        t = f - BURST
        gemini_star(d, CX, cy, 2 + t + t // 3, 0.0)
    elif COLLAPSE <= f < REBUILD:                                      # star collapses
        t = f - COLLAPSE
        gemini_star(d, CX, cy, max(0, 15 - 3 * t), 0.0)
    return img

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    out = [frame(i) for i in range(N)]
    out[0].save("output/VAR1_rocket_launch.gif", save_all=True, append_images=out[1:], duration=100, loop=0, disposal=1)
