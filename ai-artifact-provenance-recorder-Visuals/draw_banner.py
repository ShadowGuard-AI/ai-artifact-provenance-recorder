#!/usr/bin/env python3
"""ai-artifact-provenance-recorder wordmark banner: a hedge at first light counted web by web,
two swifts over a distant chimney, the name in Asta Sans on a tally board hung on a gate post."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
random.seed(101)
HERE = __file__.rsplit('/', 1)[0]
OUT = sys.argv[1] if len(sys.argv) > 1 else HERE + '/banner.png'
W, H = 1200, 420
BLUE = (52, 74, 110)
img = Image.new('RGB', (W, H), (198, 210, 198))
d = ImageDraw.Draw(img, 'RGBA')
# dawn air, low sun behind the hedge: bright band low, paling upward
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(226 - 58 * t), int(230 - 52 * t), int(210 - 34 * t)))
# distant brick chimney far behind the hedge at the left, softened by haze
chim = Image.new('RGBA', (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(chim)
cd.rectangle([120, 66, 172, 196], fill=(172, 100, 80, 165))
cd.rectangle([112, 52, 180, 68], fill=(160, 92, 72, 165))
img = Image.alpha_composite(img.convert('RGBA'), chim.filter(ImageFilter.GaussianBlur(4))).convert('RGB')
d = ImageDraw.Draw(img, 'RGBA')
# two swifts crossing high above the chimney, dark sickle shapes, for scale and hour:
# each is two long shallow wing arcs swept back from a small body, drawn as smooth curves
for (sx, sy, s) in [(316, 58, 46), (424, 38, 34)]:
    left = [(sx - s * (1 - t) * 1.0, sy + math.sin(t * 2.4) * s * 0.16 - t * s * 0.1) for t in [i / 12 for i in range(13)]]
    right = [(sx + s * t * 1.0, sy + math.sin(t * 2.4) * s * 0.16 - t * s * 0.1) for t in [i / 12 for i in range(13)]]
    d.line(left, fill=(38, 36, 34), width=3)
    d.line(right, fill=(38, 36, 34), width=3)
    d.ellipse([sx - 4, sy - 2, sx + 4, sy + 2], fill=(38, 36, 34))
# the hedge: a deep band across the frame, evening blue shadow in its gaps
hedge = Image.new('RGBA', (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(hedge)
for _ in range(300):
    cx = random.uniform(-16, W + 16); cy = 252 + random.gauss(0, 52)
    r = random.uniform(20, 50)
    hd.ellipse([cx - r, cy - r * 0.64, cx + r, cy + r * 0.64], fill=random.choice([(42, 70, 50, 215), (50, 82, 56, 215), (36, 62, 44, 220)]))
for _ in range(420):
    x = random.uniform(0, W); y = random.uniform(160, 380)
    hd.ellipse([x, y, x + random.uniform(4, 11), y + random.uniform(3, 7)], fill=random.choice([(58, 96, 62, 175), (34, 60, 40, 175), (72, 112, 74, 150)]))
img = Image.alpha_composite(img.convert('RGBA'), hedge.filter(ImageFilter.GaussianBlur(2.0))).convert('RGB')
d = ImageDraw.Draw(img, 'RGBA')
# shadow pools between the webs
for (sx, sy, sr) in [(240, 300, 90), (620, 320, 110), (980, 296, 84)]:
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([sx - sr, sy - sr * 0.5, sx + sr, sy + sr * 0.5], fill=(30, 48, 74, 70))
    img = Image.alpha_composite(img.convert('RGBA'), sh.filter(ImageFilter.GaussianBlur(16))).convert('RGB')
    d = ImageDraw.Draw(img, 'RGBA')

def orb_web(cx, cy, R, broken=False, sheet=False):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    if sheet:  # tiny sheet web down in the grass, catching light at a lower angle
        for k in range(5):
            ld.line([(cx - R, cy + k * 3 - 6), (cx + R, cy + k * 3 - 6 + random.uniform(-2, 2))], fill=(238, 244, 238, 130), width=1)
        for k in range(6):
            ld.line([(cx - R + k * R / 3, cy - 8), (cx - R + k * R / 3 + 4, cy + 10)], fill=(238, 244, 238, 90), width=1)
        img.paste(Image.alpha_composite(img.convert('RGBA'), layer).convert('RGB'), (0, 0))
        return ImageDraw.Draw(img, 'RGBA')
    nrad = 12
    ends = []
    for k in range(nrad):
        a = k * math.pi * 2 / nrad + 0.15
        ex = cx + math.cos(a) * R * random.uniform(0.93, 1.03); ey = cy + math.sin(a) * R * random.uniform(0.91, 1.0)
        ends.append((ex, ey))
        ld.line([(cx, cy), (ex, ey)], fill=(232, 240, 244, 200), width=1)
    for ri in range(1, 7):
        fr = ri / 6
        pts = [(cx + (ex - cx) * fr, cy + (ey - cy) * fr) for (ex, ey) in ends]
        for k in range(nrad):
            if broken and ri == 4 and k in (2, 3):
                continue
            p0, p1 = pts[k], pts[(k + 1) % nrad]
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + R * 0.03 * fr + 1
            ld.line([(p0[0], p0[1]), (mx, my), (p1[0], p1[1])], fill=(232, 240, 244, 185), width=1)
            if random.random() < 0.4:  # beads lit from inside, uneven
                r = random.uniform(0.8, 1.7) * (1 + max(0, (my - cy) / R) * 0.6)
                ld.ellipse([mx - r, my - r, mx + r, my + r], fill=(250, 252, 246, 200))
    img.paste(Image.alpha_composite(img.convert('RGBA'), layer.filter(ImageFilter.GaussianBlur(0.5))).convert('RGB'), (0, 0))
    return ImageDraw.Draw(img, 'RGBA')

# three webs large and complete in the near hedge
for (x, y, r) in [(268, 236, 62), (560, 214, 54), (838, 242, 58)]:
    d = orb_web(x, y, r)
# smaller and partly broken ones deeper in
for (x, y, r, b) in [(130, 286, 30, True), (414, 282, 26, False), (700, 292, 24, True), (1010, 220, 28, False), (1086, 286, 22, True), (356, 196, 18, False), (966, 330, 20, True)]:
    d = orb_web(x, y, r, broken=b)
# tiny sheet webs down in the grass
for (x, y, r) in [(180, 386, 34), (520, 396, 28), (760, 384, 32)]:
    d = orb_web(x, y, r, sheet=True)
# foreground grass heads carrying their own dew, no webs among them
for gx in range(30, 1130, 46):
    hgt = random.uniform(38, 74)
    pts = [(gx + math.sin(s * 2 + gx) * 5, 420 - s * hgt) for s in [i / 10 for i in range(11)]]
    d.line(pts, fill=(86, 120, 72), width=2)
    tx, ty = pts[-1]
    for dx in (-4, 0, 4):
        d.ellipse([tx + dx - 2.2, ty - 9, tx + dx + 2.2, ty + 3], fill=(104, 138, 88))
    d.ellipse([tx - 1.6, ty - 13, tx + 1.6, ty - 9.8], fill=(250, 252, 246, 230))
# gate post at the right edge, tally board hung on it, tilted a little on its nail
px = 1052
d.rectangle([px, 120, px + 20, 388], fill=(88, 74, 58))
d.rectangle([px, 120, px + 7, 388], fill=(104, 88, 68))
board = Image.new('RGBA', (300, 150), (0, 0, 0, 0))
bd = ImageDraw.Draw(board)
bd.rectangle([6, 30, 294, 118], fill=(70, 62, 52), outline=(46, 40, 34), width=3)
bd.ellipse([144, 36, 156, 48], fill=(30, 28, 26))  # the nail
f = ImageFont.truetype(HERE + '/fonts/AstaSans.ttf', 19)
try:
    f.set_variation_by_axes([560])
except Exception:
    pass
for li, line in enumerate(['ai-artifact-', 'provenance-', 'recorder']):
    bd.text((18, 52 + li * 21), line, font=f, fill=(246, 244, 234))
board = board.rotate(3.5, resample=Image.BICUBIC, expand=True)
img.paste(board, (px - 118, 128), board)
img = img.filter(ImageFilter.GaussianBlur(0.35))
img.save(OUT)
print('saved', OUT)
