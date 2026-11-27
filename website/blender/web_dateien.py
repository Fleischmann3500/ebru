"""Zusatzdateien fürs Web: himmel.webp (aus dem HDRI), Stationsbilder (Rückfall ohne WebGL), Favicon, og.jpg.
Aufruf: python3 web_dateien.py"""
import bpy, os, numpy as np
from PIL import Image
HIER = os.path.dirname(os.path.abspath(__file__)); WEB = os.path.join(HIER, '..', 'web', 'public')
img = bpy.data.images.load(os.path.join(HIER, 'assets', 'hdri', 'alps_field.hdr'))
w, h = img.size
a = np.array(img.pixels[:], dtype=np.float32).reshape(h, w, 4)[::-1, :, :3]
x = 1 - np.exp(-a * 1.1)                                   # weiche Schulter für die Sonne
s = np.where(x <= 0.0031308, x * 12.92, 1.055 * np.power(np.clip(x, 0, 1), 1 / 2.4) - 0.055)
Image.fromarray((s * 255).astype(np.uint8)).resize((2048, 1024), Image.LANCZOS).save(os.path.join(WEB, 'welt', 'himmel.webp'), quality=80)
print('himmel.webp')
# Stationsbilder aus den Blender-Renders
os.makedirs(os.path.join(WEB, 'welt', 'stationen'), exist_ok=True)
v = os.path.join(HIER, 'vorschau')
for n in ['station_0_logo', 'station_1_wohnen', 'station_2_sofa', 'station_3_buero', 'station_4_essen', 'station_5_schlafen']:
    q = n
    Image.open(os.path.join(v, q + '.jpg')).convert('RGB').save(os.path.join(WEB, 'welt', 'stationen', n + '.webp'), quality=78)
og = Image.open(os.path.join(v, 'station_1_wohnen.jpg')).convert('RGB'); og = og.resize((1200, int(1200 * og.height / og.width))).crop((0, 0, 1200, 630)); og.save(os.path.join(WEB, 'og.jpg'), quality=85)
print('stationen, og.jpg')
