import math
from PIL import Image
from led_kit import BLUE, RED, YEL, GRN
BASE = {BLUE, RED, YEL, GRN}

def light(c): return tuple(round(v + (255 - v) * 0.45) // 4 * 4 for v in c)
def dark(c): return tuple(round(v * 0.55) // 4 * 4 for v in c)

def shade(img, y0=2, y1=41, a=14, b=29):
    px = img.load()
    for y in range(y0, y1 + 1):
        for x in range(img.width):
            c = px[x, y]
            if c in BASE:
                px[x, y] = light(c) if y < a else dark(c) if y > b else c
    return img
