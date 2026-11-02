#!/usr/bin/env python3
"""ai-artifact-provenance-recorder logo: one dew heavy orb web, spider absent,
name in Asta Sans as a field guide entry, ruled line under the first word only."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont
random.seed(47)
HERE = __file__.rsplit('/', 1)[0]
OUT = sys.argv[1] if len(sys.argv) > 1 else HERE + '/logo.png'
W, H = 900, 600
PALE = (243, 242, 233); SOOT = (38, 36, 34); BLUE = (52, 74, 110)
img = Image.new('RGB', (W, H), PALE)
d = ImageDraw.Draw(img, 'RGBA')
hx, hy, RAD = 438, 232, 172  # hub off centre in its own web
NRAD = 14
ends = []
for k in range(NRAD):
    a = k * math.pi * 2 / NRAD + 0.1
    ex = hx + math.cos(a) * RAD * random.uniform(0.93, 1.03)
    ey = hy + math.sin(a) * RAD * random.uniform(0.91, 1.0)
    ends.append((ex, ey))
    d.line([(hx, hy), (ex, ey)], fill=BLUE + (235,), width=2)
rings = 8
beads = []
for ri in range(1, rings + 1):
    fr = ri / rings
    pts = [(hx + (ex - hx) * fr, hy + (ey - hy) * fr) for (ex, ey) in ends]
    for k in range(NRAD):
        p0, p1 = pts[k], pts[(k + 1) % NRAD]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + RAD * 0.03 * fr + 1.6
        seg = [(p0[0] + (mx - p0[0]) * s, p0[1] + (my - p0[1]) * s) for s in [i / 6 for i in range(7)]]
        seg += [(mx + (p1[0] - mx) * s, my + (p1[1] - my) * s) for s in [i / 6 for i in range(1, 7)]]
        d.line(seg, fill=BLUE + (225,), width=2)
        beads.append((mx, my, fr))
    beads += [(p[0], p[1], fr) for p in pts]
# anchor thread: the spiral ends in a single line running out of the frame at the lower right
ax, ay = ends[1]
d.line([(ax, ay), (ax + 66, ay + 44), (W + 4, ay + 118)], fill=BLUE + (235,), width=2)
bx2, by2 = ax + 40, ay + 27
d.ellipse([bx2 - 4.5, by2 - 4.5, bx2 + 4.5, by2 + 4.5], fill=(206, 226, 240, 170), outline=BLUE + (190,), width=1)
d.ellipse([bx2 - 1.8, by2 - 2, bx2 + 0.4, by2 + 0.2], fill=(255, 255, 252, 240))
# beads at the junctions, largest along the lower half, each with one point of white throat light
for (bx, by, fr) in beads:
    lower = 1 + max(0, (by - hy) / RAD) * 1.0
    r = (1.6 + fr * 3.0) * lower * random.uniform(0.7, 1.35)
    d.ellipse([bx - r, by - r, bx + r, by + r], fill=(206, 226, 240, 165), outline=BLUE + (190,), width=1)
    d.ellipse([bx - r * 0.36, by - r * 0.42, bx, by - r * 0.02], fill=(255, 255, 252, 240))
# name as a field guide entry, with a short ruled line under the first word only
f = ImageFont.truetype(HERE + '/fonts/AstaSans.ttf', 33)
try:
    f.set_variation_by_axes([560])
except Exception:
    pass
t = 'ai-artifact-provenance-recorder'
bb = d.textbbox((0, 0), t, font=f)
tx = (W - (bb[2] - bb[0])) / 2 - bb[0]
ty = 478
d.text((tx, ty), t, font=f, fill=SOOT)
w_ai = d.textlength('ai', font=f)
d.line([(tx + 1, ty + 50), (tx + w_ai + 1, ty + 50)], fill=SOOT, width=2)
img.save(OUT)
img.resize((72, 48)).save(HERE + '/scratch/logo64-ship.png')
print('saved', OUT)
