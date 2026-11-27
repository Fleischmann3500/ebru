"""ESTILO-Szene: vier Räume nebeneinander, das Wohnzimmer zeigt die Logo-Komposition.
Aufruf: python3 szene.py  -> szene.blend
Einheiten: Meter, Blender z oben. Räume entlang x: Wohnen [-3,3], Schlafen [3,9], Essen [9,15], Büro [15,21].
Vorne (y = -3) ist offen, dort fährt die Kamera. Rückwand bei y = +3.
Objekt-Eigenschaften: lm=<gruppe> (Lichtatlas), vc=1 (Licht in Vertex-Farben), bake=0 (Glas/Leuchtflächen), export=0."""
import bpy, bmesh, math, os
from mathutils import Vector, Euler

HIER = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HIER, 'assets')
H = 3.2            # Raumhöhe
T0, T1 = -3.0, 3.0 # Tiefe (y)

bpy.ops.wm.read_factory_settings(use_empty=True)
sz = bpy.context.scene
sz.unit_settings.scale_length = 1.0

# ---------------------------------------------------------------- Materialien
_mats = {}
def mat(name, farbe=(0.8, 0.8, 0.8), tex=None, rough=0.7, metall=0.0, emit=None, emit_st=0.0, glas=False, tint=None, kontrast=1.0):
    """Principled-Material. tex = Ordnername unter assets/texturen. tint färbt die Textur (Multiplizieren)."""
    if name in _mats: return _mats[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Roughness'].default_value = rough; p.inputs['Metallic'].default_value = metall
    if glas:
        p.inputs['Transmission Weight'].default_value = 1.0; p.inputs['Roughness'].default_value = 0.02
        p.inputs['Base Color'].default_value = (0.95, 0.97, 0.98, 1); p.inputs['IOR'].default_value = 1.45
    elif tex:
        d = os.path.join(A, 'texturen', tex)
        datei = eingefaerbt(tex, tint, name, kontrast) if tint else os.path.join(d, 'diff.jpg')
        img = nt.nodes.new('ShaderNodeTexImage'); img.image = bpy.data.images.load(datei, check_existing=True)
        nt.links.new(img.outputs['Color'], p.inputs['Base Color'])
        if os.path.exists(os.path.join(d, 'rough.jpg')):
            r = nt.nodes.new('ShaderNodeTexImage'); r.image = bpy.data.images.load(os.path.join(d, 'rough.jpg'), check_existing=True); r.image.colorspace_settings.name = 'Non-Color'
            nt.links.new(r.outputs['Color'], p.inputs['Roughness'])
        if os.path.exists(os.path.join(d, 'nor.jpg')):
            n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(os.path.join(d, 'nor.jpg'), check_existing=True); n.image.colorspace_settings.name = 'Non-Color'
            nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = 0.6
            nt.links.new(n.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], p.inputs['Normal'])
    else:
        p.inputs['Base Color'].default_value = (*farbe, 1)
    if emit:
        p.inputs['Emission Color'].default_value = (*emit, 1); p.inputs['Emission Strength'].default_value = emit_st
    # Werte für den Export (three.js baut die Materialien aus dieser Tabelle neu)
    m['web'] = {'tex': (name if tint else tex) or '', 'farbe': list(farbe), 'rough': rough, 'metall': metall,
                'emit': list(emit) if emit else None, 'glas': glas}
    _mats[name] = m; return m

def eingefaerbt(tex, hexfarbe, name, kontrast=1.0):
    """Textur entsättigen und auf Zielfarbe bringen (Mittelwert = Zielfarbe). Ergebnis: assets/texturen_web/<name>.jpg"""
    import numpy as np
    from PIL import Image
    ziel = os.path.join(A, 'texturen_web', name + '.jpg')
    if not os.path.exists(ziel):
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        g = np.asarray(Image.open(os.path.join(A, 'texturen', tex, 'diff.jpg')).convert('L')).astype(np.float32)
        g = g / g.mean(); g = 1 + (g - 1) * kontrast
        c = np.array([int(hexfarbe[i:i+2], 16) for i in (1, 3, 5)], np.float32)
        Image.fromarray(np.clip(g[..., None] * c, 0, 255).astype(np.uint8)).save(ziel, quality=92)
    return ziel

def srgb(h):  # '#RRGGBB' -> linear
    c = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)

M = {
    'putz':    mat('putz', tex='white_plaster_02', tint='#F3EEE7', rough=0.9),
    'putz_w':  mat('putz_warm', tex='white_plaster_02', tint='#E9E1D4', rough=0.9),
    'decke':   mat('decke', farbe=srgb('#FBF8F3'), rough=0.95),
    'parkett': mat('parkett', tex='herringbone_parquet', rough=0.68),
    'eiche':   mat('eiche', tex='oak_veneer_01', rough=0.55),
    'nuss':    mat('nuss', tex='black_walnut_veneer_01', tint='#5B4130', rough=0.5, kontrast=1.4),
    'sofa':    mat('sofa_gruen', tex='rough_linen', tint='#5F6E45', rough=0.95, kontrast=0.8),
    'lehne':   mat('sofa_lehne', tex='rough_linen', tint='#57643F', rough=0.95, kontrast=0.8),
    'kissen':  mat('kissen', tex='velour_velvet', tint='#55574A', rough=0.9),
    'samt':    mat('bett_samt', tex='velour_velvet', tint='#B9AC98', rough=0.85),
    'leinen':  mat('bettwaesche', tex='rough_linen', tint='#F4F0E8', rough=0.95),
    'oliv':    mat('stuhl_oliv', tex='velour_velvet', tint='#5C5E3C', rough=0.85),
    'teppich': mat('teppich', tex='poly_wool_herringbone', tint='#E8E1D5', rough=1.0),
    'salbei':  mat('lack_salbei', farbe=srgb('#7D8A6A'), rough=0.35),
    'kasch':   mat('lack_kaschmir', farbe=srgb('#D8D0C3'), rough=0.35),
    'schwarz': mat('metall_schwarz', farbe=srgb('#1E1F1B'), rough=0.35, metall=0.6),
    'rahmen':  mat('fensterrahmen', farbe=srgb('#2A2B27'), rough=0.4, metall=0.3),
    'glas':    mat('glas', glas=True),
    'glut':    mat('leuchte_glut', farbe=(1, 0.9, 0.75), emit=(1, 0.82, 0.6), emit_st=12),
    'led':     mat('led_streifen', farbe=(1, 0.9, 0.75), emit=(1, 0.8, 0.55), emit_st=6),
    'stein':   mat('stein_platte', farbe=srgb('#CFC8BC'), rough=0.3),
}

# ---------------------------------------------------------------- Helfer
def flagge(o, lm=None, vc=False, bake=True, export=True):
    if lm: o['lm'] = lm
    if vc: o['vc'] = 1
    if not bake: o['bake'] = 0
    if not export: o['export'] = 0
    return o

def kiste(name, gr, pos, m, rot=(0, 0, 0), fase=0.0, lm=None, uv=1.0, seg=3):
    """Quader mit optionaler Fase (Bevel), Würfel-UVs im Maßstab uv (Meter pro Kachel)."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = gr
    bpy.ops.object.transform_apply(scale=True)
    if fase > 0:
        b = o.modifiers.new('fase', 'BEVEL'); b.width = fase; b.segments = max(seg, 5) if fase >= 0.03 else seg; b.limit_method = 'ANGLE'; b.harden_normals = False
        bpy.ops.object.modifier_apply(modifier='fase')
    o.data.materials.append(m)
    wuerfel_uv(o, uv)
    glaetten(o, fase > 0)
    return flagge(o, lm=lm)

def glaetten(o, gewichtet=True):
    """Weiche Fasen ohne Facetten: glatt schattieren, Normalen nach Flächengröße gewichten."""
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.shade_smooth()
    if gewichtet:
        w = o.modifiers.new('wn', 'WEIGHTED_NORMAL'); w.keep_sharp = True; w.weight = 100
        bpy.ops.object.modifier_apply(modifier='wn')
    else:
        bpy.ops.object.shade_auto_smooth(angle=math.radians(35))
    o.select_set(False)

def wuerfel_uv(o, groesse=1.0):
    bpy.context.view_layer.objects.active = o; o.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(cube_size=groesse, scale_to_bounds=False, correct_aspect=True)
    bpy.ops.object.mode_set(mode='OBJECT'); o.select_set(False)

def zyl(name, r, h, pos, m, r2=None, rot=(0, 0, 0), n=32, lm=None):
    bpy.ops.mesh.primitive_cone_add(vertices=n, radius1=r, radius2=r if r2 is None else r2, depth=h, location=pos, rotation=rot)
    o = bpy.context.object; o.name = name; o.data.materials.append(m)
    bpy.ops.object.shade_auto_smooth(angle=math.radians(40)); wuerfel_uv(o, 0.5)
    return flagge(o, lm=lm)

def importiere(name, pos, rot_z=0.0, skala=1.0, vc=True):
    """Poly-Haven-glTF laden, Teile zu einem Objekt zusammenfassen (über Geometriedaten, nicht über die Auswahl)."""
    from mathutils import Matrix
    vorher = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(A, 'modelle', name, name + '.gltf'))
    neu = [o for o in bpy.data.objects if o not in vorher]
    meshes = [o for o in neu if o.type == 'MESH']
    bm = bmesh.new()
    mats = []
    for m in meshes:
        d = m.data.copy(); d.transform(m.matrix_world)
        # Materialindizes auf gemeinsame Liste umbiegen
        abb = []
        for sl in m.data.materials:
            if sl not in mats: mats.append(sl)
            abb.append(mats.index(sl))
        for p in d.polygons: p.material_index = abb[p.material_index] if abb else 0
        bm.from_mesh(d); bpy.data.meshes.remove(d)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for sl in mats: me.materials.append(sl)
    for o in neu: bpy.data.objects.remove(o, do_unlink=True)
    o = bpy.data.objects.new(name, me); sz.collection.objects.link(o)
    me.transform(Matrix.Rotation(rot_z, 4, 'Z') @ Matrix.Scale(skala, 4))
    xs = [v.co.x for v in me.vertices]; ys = [v.co.y for v in me.vertices]; zs = [v.co.z for v in me.vertices]
    me.transform(Matrix.Translation((-(min(xs) + max(xs)) / 2, -(min(ys) + max(ys)) / 2, -min(zs))))
    o.location = pos
    return flagge(o, vc=vc)

# ---------------------------------------------------------------- Architektur
X0, X1 = -3.0, 21.0
kiste('boden', (X1 - X0, T1 - T0 + 1.0, 0.1), ((X0 + X1) / 2, 0.5, -0.05), M['parkett'], lm='arch', uv=2.0)
kiste('decke', (X1 - X0, T1 - T0 + 1.0, 0.1), ((X0 + X1) / 2, 0.5, H + 0.05), M['decke'], lm='arch', uv=4.0)

def wand_mit_fenster(name, x0, x1, y, fx0, fx1, fz0=0.45, fz1=H - 0.25, m=M['putz'], lm='arch'):
    """Rückwand (parallel zu x) mit einem Fenster von fx0..fx1 und fz0..fz1."""
    d = 0.2
    teile = [(x0, fx0, 0, H), (fx1, x1, 0, H), (fx0, fx1, 0, fz0), (fx0, fx1, fz1, H)]
    for i, (a, b, c, e) in enumerate(teile):
        if b - a > 0.01 and e - c > 0.01:
            kiste(f'{name}_{i}', (b - a, d, e - c), ((a + b) / 2, y + d / 2, (c + e) / 2), m, lm=lm, uv=2.0)
    # Rahmen + Glas
    kiste(f'{name}_rahmen_o', (fx1 - fx0, 0.08, 0.06), ((fx0 + fx1) / 2, y + 0.1, fz1 - 0.03), M['rahmen'])
    kiste(f'{name}_rahmen_u', (fx1 - fx0, 0.08, 0.06), ((fx0 + fx1) / 2, y + 0.1, fz0 + 0.03), M['rahmen'])
    n = max(1, round((fx1 - fx0) / 1.4))
    for i in range(n + 1):
        x = fx0 + (fx1 - fx0) * i / n
        kiste(f'{name}_sprosse_{i}', (0.06, 0.08, fz1 - fz0), (x, y + 0.1, (fz0 + fz1) / 2), M['rahmen'])
    g = kiste(f'{name}_glas', (fx1 - fx0, 0.01, fz1 - fz0), ((fx0 + fx1) / 2, y + 0.1, (fz0 + fz1) / 2), M['glas'])
    flagge(g, bake=False)

def seitenwand(name, x, y0, y1, m=M['putz_w'], fenster=None):
    d = 0.2
    if not fenster:
        kiste(name, (d, y1 - y0, H), (x, (y0 + y1) / 2, H / 2), m, lm='arch', uv=2.0); return
    fy0, fy1, fz0, fz1 = fenster
    for i, (a, b, c, e) in enumerate([(y0, fy0, 0, H), (fy1, y1, 0, H), (fy0, fy1, 0, fz0), (fy0, fy1, fz1, H)]):
        if b - a > 0.01 and e - c > 0.01:
            kiste(f'{name}_{i}', (d, b - a, e - c), (x, (a + b) / 2, (c + e) / 2), m, lm='arch', uv=2.0)
    for i in range(3):
        yy = fy0 + (fy1 - fy0) * i / 2
        kiste(f'{name}_sprosse_{i}', (0.08, 0.06, fz1 - fz0), (x, yy, (fz0 + fz1) / 2), M['rahmen'])
    g = kiste(f'{name}_glas', (0.01, fy1 - fy0, fz1 - fz0), (x, (fy0 + fy1) / 2, (fz0 + fz1) / 2), M['glas']); flagge(g, bake=False)

# Wohnzimmer: geschlossene Leinen-Rückwand (Logo-Wand), Fenster links
kiste('wand_wohnen', (6.0, 0.2, H), (0.0, T1 + 0.1, H / 2), M['putz'], lm='arch', uv=2.0)
seitenwand('seite_links', X0 - 0.1, T0 - 0.5, T1 + 0.2, fenster=(-2.2, 2.2, 0.0, H - 0.2))
# Schlafen, Essen, Büro: große Fenster in der Rückwand
wand_mit_fenster('wand_schlafen', 3.0, 9.0, T1, 6.2, 8.6)
wand_mit_fenster('wand_essen', 9.0, 15.0, T1, 9.6, 14.4, fz0=0.0)
wand_mit_fenster('wand_buero', 15.0, 21.0, T1, 17.6, 20.4)
seitenwand('seite_rechts', X1 + 0.1, T0 - 0.5, T1 + 0.2)
# Raumteiler mit breitem Durchgang vorne (die Kamera geht dort durch)
for x in (3.0, 9.0, 15.0):
    seitenwand(f'teiler_{x:g}', x, 0.2, T1 + 0.0)

# ---------------------------------------------------------------- Wohnzimmer (Logo-Komposition)
def logo_sofa(x, y, rz=0.0, m_sitz=M['sofa'], m_lehne=M['lehne'], name='sofa'):
    teile = []
    teile.append(kiste(f'{name}_sitz', (2.0, 0.86, 0.22), (0, 0.02, 0.36), m_sitz, fase=0.07, seg=4, uv=0.5))
    teile.append(kiste(f'{name}_lehne', (1.86, 0.26, 0.56), (0, 0.33, 0.72), m_lehne, rot=(math.radians(-8), 0, 0), fase=0.1, seg=4, uv=0.5))
    for s in (-1, 1):  # nach außen geneigte Armlehnen wie im Logo
        teile.append(kiste(f'{name}_arm{s}', (0.24, 0.86, 0.44), (s * 1.06, 0.02, 0.5), m_sitz, rot=(0, math.radians(-14 * s), 0), fase=0.1, seg=4, uv=0.5))
    for i, (bx, by) in enumerate([(-0.86, -0.3), (-0.86, 0.3), (0.86, -0.3), (0.86, 0.3)]):
        teile.append(zyl(f'{name}_bein{i}', 0.022, 0.3, (bx, by, 0.12), M['nuss'], r2=0.012, rot=(math.radians(10 * (1 if by > 0 else -1)), math.radians(14 * (1 if bx > 0 else -1)), 0), n=12))
    # Kissen: weich gerundeter Quader
    k = kiste(f'{name}_kissen', (0.46, 0.15, 0.4), (-0.5, 0.12, 0.66), M['kissen'], rot=(math.radians(-14), 0, math.radians(5)), fase=0.06, seg=4, uv=0.5)
    teile.append(k)
    bpy.ops.object.select_all(action='DESELECT')
    for t in teile: t.select_set(True)
    bpy.context.view_layer.objects.active = teile[0]; bpy.ops.object.join()
    o = bpy.context.object; o.name = name; o.location = (x, y, 0); o.rotation_euler = (0, 0, rz)
    return flagge(o, lm='moebel')

logo_sofa(0.15, 2.1)
# drei Pendelleuchten über der linken Sofahälfte (Höhen wie im Logo)
for i, (lx, lz) in enumerate([(-0.75, 1.95), (-0.35, 1.7), (0.05, 2.0)]):
    zyl(f'pendel_kabel_{i}', 0.004, H - lz - 0.17, (lx, 1.75, (H + lz + 0.17) / 2), M['schwarz'], n=6)
    zyl(f'pendel_{i}', 0.085, 0.3, (lx, 1.75, lz), M['schwarz'], n=32, lm='moebel')
    zyl(f'pendel_kappe_{i}', 0.045, 0.04, (lx, 1.75, lz + 0.17), M['schwarz'], n=24)
    g = zyl(f'pendel_glut_{i}', 0.075, 0.004, (lx, 1.75, lz - 0.152), M['glut'], n=32); flagge(g, bake=False)
# sechs Nussholz-Lamellen rechts vom Sofa, die letzten zwei kürzer (wie im Logo)
for i, laenge in enumerate([H, H, H, H, H - 0.55, H - 0.95]):
    kiste(f'lamelle_{i}', (0.05, 0.05, laenge), (1.55 + i * 0.17, T1 - 0.03, H - laenge / 2), M['nuss'], fase=0.006, seg=1, lm='moebel', uv=0.5)
kiste('teppich_wohnen', (3.4, 2.4, 0.012), (0.1, 0.9, 0.006), M['teppich'], lm='arch', uv=1.0)
# runder Couchtisch: Steinplatte auf schwarzem Gestell
zyl('couchtisch_platte', 0.42, 0.03, (0.3, 0.75, 0.38), M['stein'], n=64, lm='moebel')
zyl('couchtisch_fuss', 0.06, 0.36, (0.3, 0.75, 0.18), M['schwarz'], r2=0.04, n=24, lm='moebel')
importiere('mid_century_lounge_chair', (2.15, 1.05, 0), rot_z=math.radians(55))
importiere('modern_wooden_cabinet', (-2.62, 0.6, 0), rot_z=math.radians(-90))
importiere('potted_plant_02', (-2.45, 2.55, 0), skala=1.6)
importiere('ceramic_vase_03', (-2.62, -0.2, 0.52), skala=1.0)
importiere('wooden_bowl_01', (0.35, 0.72, 0.395), skala=0.9)

# ---------------------------------------------------------------- Schlafzimmer
def bett(x, y):
    teile = []
    teile.append(kiste('bett_rahmen', (1.9, 2.15, 0.36), (0, -1.07, 0.22), M['samt'], fase=0.04, seg=3, uv=0.5))
    teile.append(kiste('bett_matratze', (1.78, 2.0, 0.24), (0, -1.07, 0.5), M['leinen'], fase=0.06, seg=4, uv=0.5))
    teile.append(kiste('bett_decke', (1.86, 1.25, 0.08), (0, -1.55, 0.65), M['leinen'], fase=0.035, seg=4, uv=0.5))
    # hohes Paneel-Kopfteil mit integriertem LED-Streifen (aus Ebrus Text zu Maßanfertigungen)
    for i in range(6):
        teile.append(kiste(f'bett_paneel_{i}', (0.5, 0.12, 1.25), (-1.25 + i * 0.5, 0.02, 0.72), M['samt'], fase=0.05, seg=4, uv=0.5))
    for s in (-1, 1):
        teile.append(kiste(f'bett_kissen_{s}', (0.72, 0.18, 0.4), (s * 0.42, -0.24, 0.78), M['leinen'], rot=(math.radians(-18), 0, 0), fase=0.08, seg=4, uv=0.5))
    bpy.ops.object.select_all(action='DESELECT')
    for t in teile: t.select_set(True)
    bpy.context.view_layer.objects.active = teile[0]; bpy.ops.object.join()
    o = bpy.context.object; o.name = 'bett'; o.location = (x, y, 0)
    g = kiste('bett_led', (2.9, 0.02, 0.015), (x, y + 0.09, 1.36), M['led']); flagge(g, bake=False)
    return flagge(o, lm='moebel')
bett(6.0, 2.85)
for s in (-1, 1):
    kiste(f'nachttisch_{s}', (0.5, 0.42, 0.42), (6.0 + s * 1.35, 2.55, 0.32), M['eiche'], fase=0.01, seg=2, lm='moebel', uv=0.6)
importiere('ceramic_vase_01', (7.35, 2.55, 0.53), skala=0.8)
kiste('schrank_schlafen', (0.62, 2.6, 2.6), (3.42, 0.9, 1.3), M['salbei'], fase=0.006, seg=1, lm='moebel', uv=1.0)
for i in range(4):  # Fugen und Griffleisten der Schranktüren
    kiste(f'schrank_fuge_{i}', (0.01, 0.006, 2.5), (3.735, -0.4 + i * 0.65 + 0.65, 1.3), M['schwarz'])
kiste('teppich_schlafen', (2.8, 2.0, 0.012), (6.0, 1.4, 0.006), M['teppich'], lm='arch')
importiere('potted_plant_04', (8.5, 2.6, 0), skala=1.4)

# ---------------------------------------------------------------- Esszimmer
kiste('esstisch_platte', (2.2, 1.0, 0.05), (12.0, 1.2, 0.75), M['eiche'], fase=0.008, seg=2, lm='moebel', uv=1.0)
for s in (-1, 1):  # X-Kufen aus Stahl
    for d in (-1, 1):
        kiste(f'esstisch_kufe_{s}{d}', (0.06, 0.06, 0.86), (12.0 + s * 0.8, 1.2 + d * 0.18, 0.37), M['schwarz'], rot=(math.radians(26 * d), 0, 0), lm='moebel')
def stuhl(name, x, y, rz):
    t = []
    t.append(kiste(name + '_sitz', (0.48, 0.48, 0.1), (0, 0, 0.47), M['oliv'], fase=0.04, seg=3, uv=0.4))
    t.append(kiste(name + '_lehne', (0.48, 0.1, 0.4), (0, 0.22, 0.74), M['oliv'], rot=(math.radians(-8), 0, 0), fase=0.04, seg=3, uv=0.4))
    for i, (bx, by) in enumerate([(-0.18, -0.18), (0.18, -0.18), (-0.18, 0.18), (0.18, 0.18)]):
        t.append(zyl(name + f'_bein{i}', 0.016, 0.44, (bx, by, 0.21), M['schwarz'], n=10))
    bpy.ops.object.select_all(action='DESELECT')
    for k in t: k.select_set(True)
    bpy.context.view_layer.objects.active = t[0]; bpy.ops.object.join()
    o = bpy.context.object; o.name = name; o.location = (x, y, 0); o.rotation_euler = (0, 0, rz)
    return flagge(o, lm='moebel')
for i, x in enumerate((11.35, 12.65)):
    stuhl(f'stuhl_v{i}', x, 0.38, math.radians(180))
# gepolsterte Bank an der Fensterseite
kiste('bank_sitz', (2.1, 0.46, 0.12), (12.0, 2.05, 0.46), M['oliv'], fase=0.04, seg=3, lm='moebel', uv=0.4)
kiste('bank_korpus', (2.1, 0.42, 0.38), (12.0, 2.07, 0.2), M['eiche'], fase=0.005, seg=1, lm='moebel', uv=0.8)
for i, (lx) in enumerate((11.45, 12.55)):  # zwei große schwarze Kuppelleuchten wie in den Herstellerbildern
    zyl(f'ess_kabel_{i}', 0.004, 1.0, (lx, 1.2, H - 0.5), M['schwarz'], n=6)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.28, location=(lx, 1.2, 2.0), segments=48, ring_count=24)
    k = bpy.context.object; k.name = f'ess_kuppel_{i}'
    bm = bmesh.new(); bm.from_mesh(k.data); bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -0.001], context='VERTS'); bm.to_mesh(k.data); bm.free()
    so = k.modifiers.new('dicke', 'SOLIDIFY'); so.thickness = 0.008; bpy.ops.object.modifier_apply(modifier='dicke')
    k.data.materials.append(M['schwarz']); bpy.ops.object.shade_smooth(); wuerfel_uv(k, 0.5); flagge(k, lm='moebel')
    g = zyl(f'ess_glut_{i}', 0.2, 0.004, (lx, 1.2, 2.05), M['glut'], n=32); flagge(g, bake=False)
importiere('ceramic_vase_04', (12.25, 1.15, 0.775), skala=0.7)
importiere('modern_wooden_cabinet', (9.45, 0.5, 0), rot_z=math.radians(-90))
importiere('pachira_aquatica_01', (14.4, 2.5, 0), skala=1.0)

# ---------------------------------------------------------------- Büro
kiste('schreibtisch_platte', (1.8, 0.8, 0.04), (18.6, 1.6, 0.74), M['eiche'], fase=0.006, seg=2, lm='moebel', uv=1.0)
kiste('schreibtisch_korpus', (0.45, 0.76, 0.72), (19.27, 1.6, 0.36), M['kasch'], fase=0.004, seg=1, lm='moebel')
kiste('schreibtisch_wange', (0.04, 0.76, 0.72), (17.73, 1.6, 0.36), M['eiche'], lm='moebel')
stuhl('buerostuhl', 18.4, 0.95, math.radians(180))
# Regalwand mit beleuchteten Fächern (wie RMW in den Herstellerbildern)
kiste('regal_korpus', (0.42, 2.8, 2.4), (15.32, 0.9, 1.2), M['nuss'], fase=0.004, seg=1, lm='moebel', uv=1.0)
for r in range(4):
    for c in range(4):
        fy, fz = -0.15 + c * 0.7, 0.35 + r * 0.55
        kiste(f'regal_fach_{r}{c}', (0.06, 0.62, 0.46), (15.55, fy, fz + 0.04), M['kasch'], lm='moebel')
    g = kiste(f'regal_led_{r}', (0.01, 2.7, 0.01), (15.56, 0.9, 0.35 + r * 0.55 + 0.27), M['led']); flagge(g, bake=False)
importiere('standing_picture_frame_01', (19.0, 1.85, 0.76), skala=0.8)
importiere('potted_plant_02', (20.4, 2.5, 0), skala=1.3)
importiere('wicker_basket_02', (20.3, 0.6, 0), skala=1.0)

# ---------------------------------------------------------------- Licht
def flaechenlicht(name, pos, rot, gr, staerke, farbe=(1, 0.97, 0.92)):
    l = bpy.data.lights.new(name, 'AREA'); l.shape = 'RECTANGLE'; l.size, l.size_y = gr; l.energy = staerke; l.color = farbe
    o = bpy.data.objects.new(name, l); o.location = pos; o.rotation_euler = rot; o.visible_camera = False; o.visible_glossy = False; o.visible_transmission = False; sz.collection.objects.link(o); return o
def punktlicht(name, pos, staerke, farbe=(1, 0.8, 0.58), r=0.05):
    l = bpy.data.lights.new(name, 'POINT'); l.energy = staerke; l.color = farbe; l.shadow_soft_size = r
    o = bpy.data.objects.new(name, l); o.location = pos; sz.collection.objects.link(o); return o
# Himmel (Alpen-HDRI) füllt durch Fenster und offene Front
w = bpy.data.worlds.new('welt'); sz.world = w; w.use_nodes = True
env = w.node_tree.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(os.path.join(A, 'hdri', 'alps_field.hdr'))
mp = w.node_tree.nodes.new('ShaderNodeMapping'); tc = w.node_tree.nodes.new('ShaderNodeTexCoord')
mp.inputs['Rotation'].default_value = (0, 0, math.radians(-108))
w.node_tree.links.new(tc.outputs['Generated'], mp.inputs['Vector']); w.node_tree.links.new(mp.outputs['Vector'], env.inputs['Vector'])
w.node_tree.links.new(env.outputs['Color'], w.node_tree.nodes['Background'].inputs['Color'])
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.9
# Tageslicht durch die Fenster (Flächenlichter knapp außen, nach innen gerichtet)
flaechenlicht('fenster_links', (X0 - 0.4, 0.0, 1.6), (0, math.radians(-90), 0), (4.4, 3.0), 1100)
for nm, (a, b) in {'fenster_schlafen': (6.2, 8.6), 'fenster_essen': (9.6, 14.4), 'fenster_buero': (17.6, 20.4)}.items():
    flaechenlicht(nm, ((a + b) / 2, T1 + 0.5, 1.6), (math.radians(-90), 0, 0), (b - a, 2.6), 280 * (b - a))
# Front (offen, Richtung Kamera): weiche Aufhellung
flaechenlicht('front', ((X0 + X1) / 2, T0 - 1.5, 2.2), (math.radians(90), 0, 0), (X1 - X0, 2.0), 2600, farbe=(1, 0.98, 0.95))
for i, (lx, lz) in enumerate([(-0.75, 1.95), (-0.35, 1.7), (0.05, 2.0)]):
    punktlicht(f'licht_pendel_{i}', (lx, 1.75, lz - 0.22), 18)
for i, lx in enumerate((11.45, 12.55)):
    punktlicht(f'licht_kuppel_{i}', (lx, 1.2, 1.88), 45, r=0.15)

# ---------------------------------------------------------------- Kamerastationen (Website-Brennweite: 50°-Hochformat-tauglich)
def kamera(name, pos, ziel, fov=50):
    c = bpy.data.cameras.new(name); c.lens_unit = 'FOV'; c.angle = math.radians(fov); c.sensor_fit = 'VERTICAL'
    o = bpy.data.objects.new(name, c); o.location = pos; sz.collection.objects.link(o)
    d = Vector(ziel) - Vector(pos); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return o
kamera('station_0_logo',      (0.35, -2.6, 1.25), (0.35, 3.0, 1.25), fov=58)
kamera('station_1_wohnen',    (-1.6, -1.6, 1.45), (1.0, 2.2, 0.9))
kamera('station_2_schlafen',  (4.2, -1.8, 1.5),   (6.6, 2.4, 0.8))
kamera('station_3_essen',     (10.0, -1.6, 1.55), (12.6, 1.6, 0.9))
kamera('station_4_buero',     (17.0, -1.5, 1.5),  (18.9, 2.0, 0.9))
sz.camera = bpy.data.objects['station_0_logo']

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HIER, 'szene.blend'))
print('fertig', len(bpy.data.objects), 'Objekte')
