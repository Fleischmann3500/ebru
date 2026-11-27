"""Materialtexturen fürs Web: public/welt/tex/<name>.webp (1024) und <name>.handy.webp (512) + tex.json.
Eingefärbte Materialien (assets/texturen_web/<name>.jpg) werden als Graustruktur (Mittelwert 0.7) gespeichert,
die Farbe steht in tex.json (sRGB-Hex). So lässt sich z. B. der Sofabezug im Browser umfärben."""
import os, json
import numpy as np
from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HIER, 'assets'); WEB = os.path.join(HIER, '..', 'web', 'public', 'welt', 'tex')
os.makedirs(WEB, exist_ok=True)
mats = json.load(open(os.path.join(HIER, '..', 'web', 'public', 'welt', 'material.json')))
info = {}
for name, w in mats.items():
    t = (w or {}).get('tex')
    if not t: continue
    gefaerbt = os.path.join(A, 'texturen_web', t + '.jpg')
    if os.path.exists(gefaerbt):
        im = np.asarray(Image.open(gefaerbt).convert('RGB')).astype(np.float32)
        mittel = im.reshape(-1, 3).mean(0)
        g = im.mean(-1); g = g / g.mean() * 0.7 * 255
        bild = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert('RGB')
        info[name] = {'datei': t, 'grau': True, 'farbe': '#%02X%02X%02X' % tuple(int(x) for x in mittel)}
    else:
        bild = Image.open(os.path.join(A, 'texturen', t, 'diff.jpg')).convert('RGB')
        info[name] = {'datei': t, 'grau': False}
    for suffix, px in (('', 1024), ('.handy', 512)):
        ziel = os.path.join(WEB, f'{t}{suffix}.webp')
        if not os.path.exists(ziel): bild.resize((px, px), Image.LANCZOS).save(ziel, quality=82, method=6)
json.dump(info, open(os.path.join(WEB, '..', 'tex.json'), 'w'), indent=1, ensure_ascii=False)
print(json.dumps(info, indent=1, ensure_ascii=False)); print(sum(os.path.getsize(os.path.join(WEB, f)) for f in os.listdir(WEB)) // 1024, 'KB')
