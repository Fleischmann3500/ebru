"""Gebackene Szene für das Web exportieren.
Aufruf: python3 export.py [handy]  ->  ../web/public/welt/estilo(.handy).glb, licht_*.webp, material.json
- Materialien ohne Bilder (die Website lädt Texturen selbst nach Material-Tabelle).
- UV 0 = Material, UV 1 = Lichtatlas. Vertex-Licht (Attribut 'Licht') x0.25, damit nichts abgeschnitten wird.
- Lichtatlas als WebP, kodiert sqrt(L/(1+L)) (dunkle Töne behalten Auflösung), heiße Einzelpixel per Median ersetzt."""
import bpy, os, sys, json
import numpy as np
HIER = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(HIER, '..', 'web', 'public', 'welt')
HANDY = 'handy' in sys.argv
os.makedirs(WEB, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=os.path.join(HIER, 'szene_gebacken.blend'))
sz = bpy.context.scene

# 1) Lichtatlanten kodieren
from PIL import Image, ImageFilter
for g in ('arch', 'moebel'):
    img = bpy.data.images.load(os.path.join(HIER, 'licht', f'{g}.exr'))
    w, h = img.size
    a = np.array(img.pixels[:], dtype=np.float32).reshape(h, w, 4)[::-1, :, :3]
    a = np.clip(a, 0, None)
    # Entrauschen: kantenerhaltend (bilateral) im kodierten Raum, zweimal; Hintergrund (ungenutzte Fläche) bleibt außen vor
    import cv2
    enc = np.sqrt(a / (1 + a)).astype(np.float32)
    for _ in range(2):
        enc = cv2.bilateralFilter(enc, d=9, sigmaColor=0.08, sigmaSpace=4)
    pil = Image.fromarray((enc * 255 + 0.5).astype(np.uint8))
    med = np.asarray(pil.filter(ImageFilter.MedianFilter(3))).astype(np.int16)
    roh = np.asarray(pil).astype(np.int16)
    heiss = (roh - med).max(-1) > 40           # Glühwürmchen
    roh[heiss] = med[heiss]
    # Inseln nach außen erweitern (Dilatation), damit Mipmaps und Filter kein Schwarz aus den Lücken ziehen
    belegt = (a.max(-1) > 1e-6)
    bild = roh.astype(np.float32)
    for _ in range(24):
        if belegt.all(): break
        summe = np.zeros_like(bild); anz = np.zeros(belegt.shape, np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            m = np.roll(belegt, (dy, dx), (0, 1)); summe += np.roll(bild * belegt[..., None], (dy, dx), (0, 1)); anz += m
        neu = (~belegt) & (anz > 0)
        bild[neu] = summe[neu] / anz[neu][:, None]; belegt = belegt | neu
    out = Image.fromarray(np.clip(bild, 0, 255).astype(np.uint8))
    if HANDY: out = out.resize((w // 2, h // 2), Image.LANCZOS)
    out.save(os.path.join(WEB, f'licht_{g}{".handy" if HANDY else ""}.webp'), quality=90, method=6)
    print('Lichtatlas', g, w, h, 'heiße Pixel', int(heiss.sum()))

# 2) Szene aufräumen
for o in list(sz.objects):
    if o.get('export', 1) == 0 or o.type == 'LIGHT': bpy.data.objects.remove(o, do_unlink=True)
if HANDY:  # Handy: kleine Deko weglassen
    for o in list(sz.objects):
        if o.name.startswith(('wooden_bowl', 'brass_vase', 'ceramic_vase_04', 'kleid_', 'buch_')):
            bpy.data.objects.remove(o, do_unlink=True)

tabelle = {}
for m in bpy.data.materials:
    web = dict(m.get('web', {})) if m.get('web') else {}
    if 'farbe' in web: web['farbe'] = list(web['farbe'])
    if 'emit' in web and web['emit'] is not None: web['emit'] = list(web['emit'])
    tabelle[m.name] = web
    if not m.node_tree: continue
    for n in list(m.node_tree.nodes):  # Bilder raus, nur Faktoren bleiben
        if n.type == 'TEX_IMAGE': m.node_tree.nodes.remove(n)

for o in sz.objects:
    if o.type != 'MESH': continue
    me = o.data
    o['gruppe'] = o.get('lm', 'vc' if o.get('vc') else 'ohne')
    uv = me.uv_layers
    if 'lm' in o:
        # Reihenfolge sicherstellen: Material-UV zuerst, dann Lightmap
        if uv[0].name == 'Lightmap' and len(uv) > 1:
            pass
        for l in uv: l.active_render = (l.name != 'Lightmap')
        if 'Licht' in me.color_attributes: me.color_attributes.remove(me.color_attributes['Licht'])
    else:
        if 'Lightmap' in uv: uv.remove(uv['Lightmap'])
        if 'Licht' in me.color_attributes:
            ca = me.color_attributes['Licht']
            d = np.empty(len(ca.data) * 4, dtype=np.float32); ca.data.foreach_get('color', d)
            d = d.reshape(-1, 4); d[:, :3] *= 0.25; d[:, 3] = 1; ca.data.foreach_set('color', d.ravel())
        for c in list(me.color_attributes):
            if c.name != 'Licht': me.color_attributes.remove(c)
    # eigene Eigenschaften nicht als Ballast exportieren
    for k in ('lm', 'vc', 'bake', 'export'):
        if k in o: del o[k]

with open(os.path.join(WEB, 'material.json'), 'w') as f: json.dump(tabelle, f, ensure_ascii=False, indent=1)

ziel = os.path.join(WEB, f'estilo{".handy" if HANDY else ""}.roh.glb')
bpy.ops.export_scene.gltf(filepath=ziel, export_format='GLB', export_image_format='NONE', export_cameras=True,
                          export_extras=True, export_apply=True, export_texcoords=True, export_normals=True,
                          export_vertex_color='NAME', export_vertex_color_name='Licht', export_all_vertex_colors=False,
                          export_yup=True, export_lights=False)
print('exportiert', ziel, os.path.getsize(ziel) // 1024, 'KB')
