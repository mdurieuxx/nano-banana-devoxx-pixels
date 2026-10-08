# VAR2 - "Gemini Bloom": a four-colour Gemini star pulses and spins at the centre while four Google-colour
# comets orbit it. Black background (~80% pure #000000), one clear subject, 60 frames @ 100 ms.
# Everything is periodic over N frames (the star spins exactly 360 degrees per loop) -> seamless loop.
import math, os
from PIL import Image, ImageDraw
from led_kit import *

CX, CY = 32, 32

def frame(f):
    img = Image.new("RGB", (S, S), BLK)
    d = ImageDraw.Draw(img)
    frame_shell(d, f, "GEMINI", "DEVOXX")
    phase = 2 * math.pi * f / N
    # orbiting comets: head 3x3 + two trailing squares, on a slightly flattened orbit
    for k, col in enumerate([BLUE, RED, YEL, GRN]):
        for j, size in enumerate([3, 2, 2]):
            a = phase + k * math.pi / 2 - j * 0.16
            x = round(CX + 25 * math.cos(a)) - size // 2
            y = round(CY + 14 * math.sin(a)) - size // 2
            d.rectangle([x, y, x + size - 1, y + size - 1], col)
    # pulsing, spinning star (3 pulses per loop)
    r = 9 + round(4 * math.sin(3 * phase))
    gemini_star(d, CX, CY, r, phase)
    d.rectangle([CX - 1, CY - 1, CX + 1, CY + 1], WHITE)                 # white core
    return img

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    out = [frame(i) for i in range(N)]
    out[0].save("output/VAR2_gemini_bloom.gif", save_all=True, append_images=out[1:], duration=100, loop=0, disposal=1)
