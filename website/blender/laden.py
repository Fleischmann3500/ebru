"""Poly-Haven-Assets (CC0) für die ESTILO-Szene laden.
Modelle als glTF 1k, Texturen 1k (diff, nor_gl, rough), HDRI 2k. Aufruf: python3 laden.py"""
import json, os, urllib.request
UA = {'User-Agent': 'estilo-site-build/1.0'}
ZIEL = os.path.join(os.path.dirname(__file__), 'assets')
MODELLE = ['mid_century_lounge_chair', 'modern_wooden_cabinet', 'potted_plant_02', 'potted_plant_04',
           'ceramic_vase_01', 'ceramic_vase_03', 'ceramic_vase_04', 'decorative_book_set_01',
           'standing_picture_frame_01', 'wicker_basket_02', 'wooden_bowl_01', 'pachira_aquatica_01']
TEXTUREN = ['wool_boucle', 'velour_velvet', 'rough_linen', 'oak_veneer_01', 'herringbone_parquet',
            'white_plaster_02', 'poly_wool_herringbone', 'black_walnut_veneer_01', 'brown_leather']
HDRI = ['alps_field']
def hole(url, pfad):
    if os.path.exists(pfad): return
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA)) as r, open(pfad, 'wb') as f: f.write(r.read())
def info(i): return json.load(urllib.request.urlopen(urllib.request.Request(f'https://api.polyhaven.com/files/{i}', headers=UA)))
for m in MODELLE:
    f = info(m)
    if 'gltf' not in f: print('kein glTF, übersprungen:', m); continue
    g = f['gltf']['1k']['gltf']; hole(g['url'], f'{ZIEL}/modelle/{m}/{m}.gltf')
    for rel, d in g['include'].items(): hole(d['url'], f'{ZIEL}/modelle/{m}/{rel}')
    print('Modell', m)
for t in TEXTUREN:
    f = info(t)
    for k, n in [('Diffuse', 'diff'), ('nor_gl', 'nor'), ('Rough', 'rough')]:
        if k in f: hole(f[k]['1k']['jpg']['url'], f'{ZIEL}/texturen/{t}/{n}.jpg')
    print('Textur', t)
for h in HDRI:
    hole(info(h)['hdri']['2k']['hdr']['url'], f'{ZIEL}/hdri/{h}.hdr'); print('HDRI', h)
