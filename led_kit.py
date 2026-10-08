# Shared helpers for the black-background variants (frame layout borrowed from the leaderboard #1:
# 2x title on top, rule, scene band, rule, 2x title at the bottom).
import math
from recipe_top1_google_chomps_devoxx import (text2x, LETTER, FONT, BLUE, RED, YEL, GRN, WHITE, BLK, S, N)

for ch in "MNPRTHY":
    LETTER[ch] = FONT[ch]

BRAND = [BLUE, RED, YEL, BLUE, GRN, RED]

def frame_shell(d, f, top, bottom=None):
    """Titles + rules. A 1-px glint runs along each rule so no two consecutive frames are identical."""
    text2x(d, top, 9, 2, BRAND)
    d.line([(0, 13), (S, 13)], BLUE)
    d.line([(0, 51), (S, 51)], BLUE)
    if bottom:
        text2x(d, bottom, 9, 53, BRAND)
    d.point((f * S // N, 13), WHITE)
    d.point((S - 1 - f * S // N, 51), WHITE)

def gemini_star(d, cx, cy, r, rot=0.0):
    """Filled 4-point astroid ('Gemini' sparkle), crisp pixels, one Google color per arm (no anti-aliasing)."""
    if r < 1:
        return
    c, s = math.cos(rot), math.sin(rot)
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            u, v = dx * c + dy * s, -dx * s + dy * c
            if (abs(u) / r) ** 0.7 + (abs(v) / r) ** 0.7 <= 1.0:
                if abs(u) > abs(v):
                    col = RED if u > 0 else GRN
                else:
                    col = BLUE if v < 0 else YEL
                d.point((cx + dx, cy + dy), col)
