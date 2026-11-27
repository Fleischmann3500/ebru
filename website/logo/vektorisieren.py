"""Logo-PNG (4465x1961) Farbe für Farbe mit potrace in SVG umwandeln.
Ebenen: sofa, lehne, kissen, pflanze-hell, pflanze-dunkel, linie (Schrift, Lampen, Lamellen, Beine)."""
import sys, numpy as np, potrace
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
im = np.array(Image.open(src).convert('RGBA')).astype(int)
rgb, a = im[..., :3], im[..., 3]
def near(c, tol=6): return (np.abs(rgb - np.array(c)).max(-1) <= tol) & (a > 128)
ebenen = {  # Name: (Farbe im PNG, Füllung im SVG)
  'lehne':  ((104,114,81), '#687251'),
  'sofa':   ((111,127,80), '#6F7F50'),
  'kissen': ((91,91,73),  '#5B5B49'),
  'blatt':  ((154,166,133),'#9AA685'),
}
masks = {k: near(c) for k,(c,_) in ebenen.items()}
masks['kissen'] |= near((93,96,75))
farbig = np.zeros_like(a, bool)
for m in masks.values(): farbig |= m
masks['linie'] = (a > 128) & ~farbig            # alles Übrige = Strichfarbe (weiß bzw. schwarz)
fills = {k: f for k,(_,f) in ebenen.items()}; fills['linie'] = 'currentColor'
def path(mask):
    bm = potrace.Bitmap(~mask)  # potracer zeichnet die dunklen (False) Pixel
    pl = bm.trace(turdsize=8, alphamax=1.0, opticurve=True, opttolerance=0.2)
    d = []
    for c in pl:
        s = c.start_point; d.append(f'M{s.x:.1f},{s.y:.1f}')
        for seg in c.segments:
            if seg.is_corner: d.append(f'L{seg.c.x:.1f},{seg.c.y:.1f}L{seg.end_point.x:.1f},{seg.end_point.y:.1f}')
            else: d.append(f'C{seg.c1.x:.1f},{seg.c1.y:.1f} {seg.c2.x:.1f},{seg.c2.y:.1f} {seg.end_point.x:.1f},{seg.end_point.y:.1f}')
        d.append('Z')
    return ''.join(d)
h, w = a.shape
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="ESTILO Einrichtungsstudio">']
for k in ['lehne','sofa','kissen','blatt','linie']:
    parts.append(f'<path id="{k}" fill="{fills[k]}" fill-rule="evenodd" d="{path(masks[k])}"/>')
parts.append('</svg>')
open(out,'w').write('\n'.join(parts)); print(out, sum(len(p) for p in parts)//1024, 'KB')
