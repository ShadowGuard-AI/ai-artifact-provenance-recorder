#!/usr/bin/env python3
"""ai-artifact-provenance-recorder intro banner: one dew heavy orb web at close range,
hedge running away to the left with more webs as pale discs, dawn air above. No writing anywhere."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFilter
random.seed(131)
HERE = __file__.rsplit('/', 1)[0]
OUT = sys.argv[1] if len(sys.argv) > 1 else HERE + '/intro-banner.png'
W, H = 1200, 520
img = Image.new('RGB', (W, H), (196, 208, 196))
d = ImageDraw.Draw(img, 'RGBA')
# dawn air: pale, light strengthening toward the top of the frame
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(216 - 66 * t), int(224 - 62 * t), int(208 - 44 * t)))
# distant chimney reduced to a soft brick coloured block
chim = Image.new('RGBA', (W, H), (0, 0, 0, 0))
ImageDraw.Draw(chim).rectangle([88, 92, 148, 226], fill=(172, 100, 80, 150))
img = Image.alpha_composite(img.convert('RGBA'), chim.filter(ImageFilter.GaussianBlur(7))).convert('RGB')
d = ImageDraw.Draw(img, 'RGBA')
# the hedge mass running away to the left: overlapping leaf clusters, no hard outline
hedge = Image.new('RGBA', (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(hedge)
for _ in range(260):
    cx = random.uniform(-10, 730); cy = 305 + random.gauss(0, 54) + (cx / 730) * 18
    r = random.uniform(22, 52)
    hd.ellipse([cx - r, cy - r * 0.66, cx + r, cy + r * 0.66], fill=random.choice([(44, 74, 52, 215), (52, 86, 58, 215), (38, 66, 46, 220)]))
for _ in range(500):
    x = random.uniform(0, 720); y = random.uniform(190, 430)
    hd.ellipse([x, y, x + random.uniform(4, 12), y + random.uniform(3, 8)], fill=random.choice([(56, 94, 62, 190), (36, 64, 44, 190), (70, 110, 74, 165)]))
img = Image.alpha_composite(img.convert('RGBA'), hedge.filter(ImageFilter.GaussianBlur(2.2))).convert('RGB')
d = ImageDraw.Draw(img, 'RGBA')
# more webs in the hedge as pale discs of different sizes, some torn, softened into the hedge
disc_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
dd = ImageDraw.Draw(disc_layer)
def pale_disc(cx, cy, r, torn=False):
    dd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(238, 244, 238, 175), width=2)
    for k in range(6):
        a = k * math.pi / 3 + 0.3
        dd.line([(cx, cy), (cx + math.cos(a) * r, cy + math.sin(a) * r)], fill=(238, 244, 238, 85), width=1)
    dd.ellipse([cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6], outline=(238, 244, 238, 110), width=1)
    if torn:
        dd.polygon([(cx, cy), (cx + r, cy - r * 0.4), (cx + r * 0.9, cy + r * 0.5)], fill=(52, 84, 58, 170))
    for _ in range(7):
        a = random.uniform(0, math.pi * 2); rr = random.uniform(0.3, 0.95)
        bx, by = cx + math.cos(a) * r * rr, cy + math.sin(a) * r * rr
        dd.ellipse([bx - 1.8, by - 1.8, bx + 1.8, by + 1.8], fill=(250, 252, 246, 150))
for (x, y, r, t) in [(150, 268, 44, False), (268, 300, 30, True), (392, 262, 24, False), (500, 306, 19, False), (586, 272, 14, True), (648, 312, 11, False), (84, 348, 26, True)]:
    pale_disc(x, y, r, t)
img = Image.alpha_composite(img.convert('RGBA'), disc_layer.filter(ImageFilter.GaussianBlur(0.8))).convert('RGB')
d = ImageDraw.Draw(img, 'RGBA')
# grass stems crossing in front of the furthest discs, curving, in a loose group at the left
for gx, lean in [(52, -14), (96, 10), (238, -8), (470, 12), (606, -10)]:
    pts = [(gx + math.sin(s * 1.9 + gx) * 9 + lean * s * s, 520 - s * random.uniform(150, 190)) for s in [i / 12 for i in range(13)]]
    d.line(pts, fill=(92, 126, 78), width=2)
    tx, ty = pts[-1]
    for dx in (-4, 0, 4):
        d.ellipse([tx + dx - 2, ty - 10, tx + dx + 2, ty + 3], fill=(110, 144, 94))

# the one complete orb web filling the right half, sharp
hx, hy = 905, 238  # hub, off centre in its own web
RAD = 218
NRAD = 15
radials = []
for k in range(NRAD):
    a = k * math.pi * 2 / NRAD + 0.12
    radials.append(a)
    ex, ey = hx + math.cos(a) * RAD * random.uniform(0.94, 1.03), hy + math.sin(a) * RAD * random.uniform(0.92, 1.0)
    d.line([(hx, hy), (ex, ey)], fill=(226, 234, 240, 235), width=2)
    radials[-1] = (a, ex, ey)
# spiral with a sag between each pair of radials; one lower segment broken
rings = 9
broken_ring, broken_seg = 6, 11  # ring index, segment between radial 11 and 12 (lower left of hub)
web = Image.new('RGBA', (W, H), (0, 0, 0, 0))
wd = ImageDraw.Draw(web)
beads = []
for ri in range(1, rings + 1):
    fr = ri / rings
    pts = []
    for k in range(NRAD + 1):
        a, ex, ey = radials[k % NRAD]
        bx, by = hx + (ex - hx) * fr, hy + (ey - hy) * fr
        pts.append((bx, by))
    # draw segment by segment with sag midpoints
    for k in range(NRAD):
        if ri == broken_ring and k == broken_seg:
            continue
        p0, p1 = pts[k], pts[k + 1]
        mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + RAD * 0.028 * fr + 2
        seg = [(p0[0] + (mx - p0[0]) * s, p0[1] + (my - p0[1]) * s + math.sin(s * math.pi) * 1.2) for s in [i / 6 for i in range(7)]]
        seg += [(mx + (p1[0] - mx) * s, my + (p1[1] - my) * s) for s in [i / 6 for i in range(1, 7)]]
        wd.line(seg, fill=(226, 234, 240, 225), width=2)
        beads.append((mx, my, fr))
    beads += [(p[0], p[1], fr) for p in pts[:-1]]
# dew beads at the junctions, largest along the lower half, each with one point of throat light
for (bx, by, fr) in beads:
    lower = 1 + max(0, (by - hy) / RAD) * 0.9
    r = (1.4 + fr * 2.6) * lower * random.uniform(0.75, 1.3)
    wd.ellipse([bx - r, by - r, bx + r, by + r], fill=(208, 228, 238, 150), outline=(240, 248, 250, 220), width=1)
    wd.ellipse([bx - r * 0.34, by - r * 0.4, bx + r * 0.05, by - r * 0.05], fill=(255, 255, 252, 235))
img = Image.alpha_composite(img.convert('RGBA'), web).convert('RGB')
d = ImageDraw.Draw(img, 'RGBA')
# the broken segment: loose end curled, with a bead hanging from the curl
fr = broken_ring / rings
a0, ex0, ey0 = radials[broken_seg]
px, py = hx + (ex0 - hx) * fr, hy + (ey0 - hy) * fr
d.arc([px - 4, py - 2, px + 22, py + 24], 300, 130, fill=(230, 238, 242), width=2)
d.line([(px + 13, py + 22), (px + 13, py + 30)], fill=(230, 238, 242), width=1)
d.ellipse([px + 8, py + 28, px + 18, py + 40], fill=(208, 228, 238, 170), outline=(240, 248, 250, 230), width=1)
d.ellipse([px + 10.5, py + 30.5, px + 14, py + 34], fill=(255, 255, 252, 240))
# one bead near the hub large enough to hold a reflected strip of hedge and sky
bx, by, br = hx - 30, hy - 20, 11
d.ellipse([bx - br, by - br, bx + br, by + br], fill=(206, 226, 238, 150), outline=(242, 250, 252, 220), width=1)
d.polygon([(bx - br + 3, by + 2), (bx + br - 3, by + 2), (bx + br - 4, by + 6), (bx - br + 4, by + 6)], fill=(84, 116, 86, 120))
d.polygon([(bx - br + 3, by - 5), (bx + br - 3, by - 5), (bx + br - 3, by - 1), (bx - br + 3, by - 1)], fill=(238, 242, 228, 130))
img = img.filter(ImageFilter.GaussianBlur(0.35))
img.save(OUT)
print('saved', OUT)
