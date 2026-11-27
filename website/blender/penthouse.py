"""ESTILO V2: Penthouse, warm minimal. Aufruf: python3 penthouse.py  ->  szene.blend
Grundriss (Meter, Blender z oben), Wohnung x 0..22, y 0..12, Raumhöhe 3,0:
  Flur x0-4 y0-5 | Büro x4-10 y0-5 | Bad x10-16 y0-5 (geschlossen) | Ankleide x16-22 y0-5
  Wohnen x0-10 y5-12 | Küche+Essen x10-16 y5-12 | Schlafen x16-22 y5-12
Nordseite (y=12) und Ostseite des Schlafzimmers ganz verglast, davor Terrasse. Logo-Wand = Westwand im Wohnzimmer.
Objekt-Eigenschaften wie V1: lm=<gruppe>, vc=1, bake=0, export=0. Kamerastationen station_<n>_<name>, Wegpunkte weg_<n>_<i>."""
import bpy, bmesh, math, os, random
from mathutils import Vector, Matrix

HIER = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HIER, 'assets')
H = 3.0
random.seed(7)
bpy.ops.wm.read_factory_settings(use_empty=True)
sz = bpy.context.scene

# ================================================================ Materialien
def eingefaerbt(tex, hexfarbe, name, kontrast=1.0):
    import numpy as np
    from PIL import Image
    ziel = os.path.join(A, 'texturen_web', f'{name}.jpg')
    if not os.path.exists(ziel):
        os.makedirs(os.path.dirname(ziel), exist_ok=True)
        g = np.asarray(Image.open(os.path.join(A, 'texturen', tex, 'diff.jpg')).convert('L')).astype(np.float32)
        g = g / g.mean(); g = 1 + (g - 1) * kontrast
        c = np.array([int(hexfarbe[i:i + 2], 16) for i in (1, 3, 5)], np.float32)
        Image.fromarray(np.clip(g[..., None] * c, 0, 255).astype(np.uint8)).save(ziel, quality=92)
    return ziel

def srgb(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)

_mats = {}
def mat(name, farbe='#CCCCCC', tex=None, tint=None, kontrast=1.0, rough=0.7, metall=0.0, emit=None, emit_st=0.0, glas=False, normal=0.6):
    if name in _mats: return _mats[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    p.inputs['Roughness'].default_value = rough; p.inputs['Metallic'].default_value = metall
    if glas:
        p.inputs['Transmission Weight'].default_value = 1.0; p.inputs['Roughness'].default_value = 0.02
        p.inputs['Base Color'].default_value = (0.96, 0.98, 0.98, 1); p.inputs['IOR'].default_value = 1.45
    elif tex:
        d = os.path.join(A, 'texturen', tex)
        datei = eingefaerbt(tex, tint, name, kontrast) if tint else os.path.join(d, 'diff.jpg')
        img = nt.nodes.new('ShaderNodeTexImage'); img.image = bpy.data.images.load(datei, check_existing=True)
        nt.links.new(img.outputs['Color'], p.inputs['Base Color'])
        if os.path.exists(os.path.join(d, 'rough.jpg')):
            r = nt.nodes.new('ShaderNodeTexImage'); r.image = bpy.data.images.load(os.path.join(d, 'rough.jpg'), check_existing=True)
            r.image.colorspace_settings.name = 'Non-Color'; nt.links.new(r.outputs['Color'], p.inputs['Roughness'])
        if os.path.exists(os.path.join(d, 'nor.jpg')) and normal > 0:
            n = nt.nodes.new('ShaderNodeTexImage'); n.image = bpy.data.images.load(os.path.join(d, 'nor.jpg'), check_existing=True)
            n.image.colorspace_settings.name = 'Non-Color'
            nm = nt.nodes.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = normal
            nt.links.new(n.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], p.inputs['Normal'])
    else:
        p.inputs['Base Color'].default_value = (*srgb(farbe), 1)
    if emit:
        p.inputs['Emission Color'].default_value = (*emit, 1); p.inputs['Emission Strength'].default_value = emit_st
    m['web'] = {'tex': (name if tint else tex) or '', 'farbe': list(srgb(farbe)), 'rough': rough, 'metall': metall,
                'emit': list(emit) if emit else None, 'glas': glas}
    _mats[name] = m; return m

M = {
    'boden':   mat('boden', tex='wood_floor', tint='#C2A47F', kontrast=1.15, rough=0.45, normal=0.4),
    'deck':    mat('terrasse', tex='wood_floor', tint='#8E8478', kontrast=1.2, rough=0.8),
    'putz':    mat('putz', tex='white_stucco', tint='#F2EEE7', kontrast=0.22, rough=0.92, normal=0.25),
    'putz_a':  mat('putz_aussen', tex='white_stucco', tint='#DDD6CB', kontrast=0.8, rough=0.95),
    'decke':   mat('decke', farbe='#F7F4EF', rough=0.95),
    'stein':   mat('travertin', tex='travertin', rough=0.42),
    'eiche':   mat('eiche', tex='white_oak_veneer', rough=0.5, normal=0.3),
    'nuss':    mat('nuss', tex='black_walnut_veneer_01', tint='#5B4130', kontrast=1.4, rough=0.45),
    'sofa':    mat('sofa_gruen', tex='rough_linen', tint='#687851', kontrast=0.8, rough=0.95),
    'keder':   mat('sofa_keder', tex='rough_linen', tint='#4C5837', kontrast=0.6, rough=0.95),
    'kis_d':   mat('kissen_oliv', tex='velour_velvet', tint='#50533F', kontrast=0.6, rough=0.85),
    'kis_h':   mat('kissen_leinen', tex='rough_linen', tint='#DCD3C4', kontrast=0.8, rough=0.95),
    'bett':    mat('bett_stoff', tex='rough_linen', tint='#CBBDA7', kontrast=0.8, rough=0.95),
    'waesche': mat('bettwaesche', tex='rough_linen', tint='#F3EFE8', kontrast=0.6, rough=0.95),
    'plaid':   mat('plaid', tex='rough_linen', tint='#8E7656', kontrast=0.9, rough=1.0),
    'leder':   mat('leder_cognac', tex='brown_leather', rough=0.5, normal=0.5),
    'teppich': mat('teppich', tex='poly_wool_herringbone', tint='#E2D9CB', kontrast=0.8, rough=1.0),
    'schwarz': mat('metall_schwarz', farbe='#1E1F1B', rough=0.4, metall=0.7),
    'messing': mat('messing', farbe='#B48F5A', rough=0.3, metall=1.0),
    'keramik': mat('keramik', farbe='#ECE7DF', rough=0.45),
    'rahmen':  mat('fensterrahmen', farbe='#2B2C28', rough=0.45, metall=0.4),
    'glas':    mat('glas', glas=True),
    'glut':    mat('leuchte_glut', farbe='#FFF0DA', emit=(1, 0.86, 0.66), emit_st=10),
    'led':     mat('led_streifen', farbe='#FFF0DA', emit=(1, 0.84, 0.6), emit_st=5),
    'schirm':  mat('lampenschirm', farbe='#EFE6D6', rough=0.9, emit=(1, 0.85, 0.62), emit_st=1.5),
    'spiegel': mat('spiegel', farbe='#D9DCDC', rough=0.05, metall=1.0),
}
BUCH = [mat(f'buch_{i}', farbe=c, rough=0.8) for i, c in enumerate(['#D9CFBF', '#8A7A63', '#3F4A3A', '#B9A888', '#5C4636', '#E8E2D6'])]

# ================================================================ Helfer
def flagge(o, lm=None, vc=False, bake=True, export=True):
    if lm: o['lm'] = lm
    if vc: o['vc'] = 1
    if not bake: o['bake'] = 0
    if not export: o['export'] = 0
    return o

def aktiv(o):
    bpy.ops.object.select_all(action='DESELECT'); bpy.context.view_layer.objects.active = o; o.select_set(True)

def wuerfel_uv(o, groesse=1.0):
    aktiv(o); bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.cube_project(cube_size=groesse, scale_to_bounds=False, correct_aspect=True)
    bpy.ops.object.mode_set(mode='OBJECT'); o.select_set(False)

def glaetten(o, gewichtet=True):
    aktiv(o); bpy.ops.object.shade_smooth()
    if gewichtet:
        w = o.modifiers.new('wn', 'WEIGHTED_NORMAL'); w.keep_sharp = True; w.weight = 100
        bpy.ops.object.modifier_apply(modifier='wn')
    o.select_set(False)

def mod_anwenden(o, typ, **kw):
    aktiv(o); m = o.modifiers.new(typ.lower(), typ)
    for k, v in kw.items(): setattr(m, k, v)
    bpy.ops.object.modifier_apply(modifier=m.name); o.select_set(False)

def kiste(name, gr, pos, m, rot=(0, 0, 0), fase=0.0, seg=3, lm=None, uv=1.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=pos, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = gr
    bpy.ops.object.transform_apply(scale=True)
    if fase > 0: mod_anwenden(o, 'BEVEL', width=fase, segments=seg, limit_method='ANGLE')
    o.data.materials.append(m); wuerfel_uv(o, uv); glaetten(o, fase > 0)
    if fase == 0: aktiv(o); bpy.ops.object.shade_flat(); o.select_set(False)
    return flagge(o, lm=lm)

def zyl(name, r, h, pos, m, r2=None, rot=(0, 0, 0), n=32, lm=None, fase=0.0):
    bpy.ops.mesh.primitive_cone_add(vertices=n, radius1=r, radius2=r if r2 is None else r2, depth=h, location=pos, rotation=rot)
    o = bpy.context.object; o.name = name
    if fase > 0: mod_anwenden(o, 'BEVEL', width=fase, segments=3, limit_method='ANGLE')
    o.data.materials.append(m); wuerfel_uv(o, 0.5)
    aktiv(o); bpy.ops.object.shade_auto_smooth(angle=math.radians(40)); o.select_set(False)
    return flagge(o, lm=lm)

def drehkoerper(name, profil, pos, m, n=48, lm=None):
    """Rotationskörper aus Profil [(radius, höhe), ...] um die z-Achse."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    ringe = []
    for i in range(n):
        a = 2 * math.pi * i / n
        ringe.append([bm.verts.new((r * math.cos(a), r * math.sin(a), z)) for r, z in profil])
    for i in range(n):
        r0, r1 = ringe[i], ringe[(i + 1) % n]
        for j in range(len(profil) - 1):
            bm.faces.new((r0[j], r1[j], r1[j + 1], r0[j + 1]))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sz.collection.objects.link(o); o.location = pos
    me.materials.append(m); wuerfel_uv(o, 0.4)
    aktiv(o); bpy.ops.object.shade_smooth(); o.select_set(False)
    return flagge(o, lm=lm)

def rohr(name, punkte, r, m, lm=None):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = r; cu.bevel_resolution = 3
    sp = cu.splines.new('POLY'); sp.points.add(len(punkte) - 1)
    for i, p in enumerate(punkte): sp.points[i].co = (*p, 1)
    o = bpy.data.objects.new(name, cu); sz.collection.objects.link(o)
    aktiv(o); bpy.ops.object.convert(target='MESH'); o = bpy.context.object
    o.data.materials.append(m); wuerfel_uv(o, 0.3); glaetten(o, False)
    return flagge(o, lm=lm)

def polster(name, gr, pos, m, rad=0.05, puff=0.02, rot=(0, 0, 0), falten=0.004, schnitte=9, keder=None, lm=None):
    """Weiches Polster: abgerundeter Quader, oben und unten leicht gewölbt, feine Falten, optional Keder an beiden Kanten."""
    hx, hy, hz = gr[0] / 2, gr[1] / 2, gr[2] / 2
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=schnitte, use_grid_fill=True)
    cl = lambda v, a: max(-a, min(a, v))
    for v in bm.verts:
        p = Vector((v.co.x * 2 * hx, v.co.y * 2 * hy, v.co.z * 2 * hz))
        innen = Vector((cl(p.x, hx - rad), cl(p.y, hy - rad), cl(p.z, hz - rad)))
        d = p - innen
        if d.length > 1e-7: p = innen + d.normalized() * rad
        ux, uy = p.x / hx, p.y / hy
        f = max(0.0, 1 - ux * ux) * max(0.0, 1 - uy * uy)
        if abs(p.z) > 1e-6: p.z += math.copysign(puff * f, p.z)
        v.co = p
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); sz.collection.objects.link(o)
    me.materials.append(m)
    mod_anwenden(o, 'SUBSURF', levels=2, render_levels=2)
    if falten > 0:
        tex = bpy.data.textures.get('falten') or bpy.data.textures.new('falten', 'CLOUDS'); tex.noise_scale = 0.12
        mod_anwenden(o, 'DISPLACE', texture=tex, strength=falten, mid_level=0.5)
    wuerfel_uv(o, 0.5); aktiv(o); bpy.ops.object.shade_smooth(); o.select_set(False)
    teile = [o]
    if keder:
        for s in (-1, 1):  # Keder auf 45° der Rundung, oben und unten
            k = rad * (1 - math.cos(math.radians(45)))
            ax, ay, z = hx - k, hy - k, s * (hz - k + (puff * 0.15 if s > 0 else -puff * 0.15))
            pts = []
            for cx, cy, a0 in ((ax - rad, ay - rad, 0), (-(ax - rad), ay - rad, 90), (-(ax - rad), -(ay - rad), 180), (ax - rad, -(ay - rad), 270)):
                for i in range(7):
                    a = math.radians(a0 + 90 * i / 6); pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a), z))
            pts.append(pts[0])
            teile.append(rohr(name + f'_keder{s}', pts, 0.0055, keder))
    o = verbinden(teile, name) if len(teile) > 1 else o
    o.location = pos; o.rotation_euler = rot
    return flagge(o, lm=lm)

def verbinden(teile, name):
    bpy.ops.object.select_all(action='DESELECT')
    for t in teile: t.select_set(True)
    bpy.context.view_layer.objects.active = teile[0]; bpy.ops.object.join()
    o = bpy.context.object; o.name = name; return o

def gruppe(teile, name, pos=(0, 0, 0), rz=0.0, lm='moebel'):
    """Teile (lokal um 0 gebaut) zu einem Objekt verbinden, dann setzen und drehen. Transform wird übernommen, Ursprung bleibt Mitte unten."""
    o = verbinden(teile, name)
    aktiv(o); bpy.ops.object.transform_apply(location=True, rotation=True, scale=True); o.select_set(False)
    o.location = pos; o.rotation_euler = (0, 0, rz)
    return flagge(o, lm=lm)

def importiere(name, pos, rot_z=0.0, skala=1.0, ziel_dreiecke=20000):
    vorher = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(A, 'modelle', name, name + '.gltf'))
    neu = [o for o in bpy.data.objects if o not in vorher]
    bm = bmesh.new(); mats = []
    for mo in [o for o in neu if o.type == 'MESH']:
        d = mo.data.copy(); d.transform(mo.matrix_world); abb = []
        for sl in mo.data.materials:
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
    dr = sum(len(p.vertices) - 2 for p in me.polygons)
    if dr > ziel_dreiecke: mod_anwenden(o, 'DECIMATE', ratio=ziel_dreiecke / dr, use_collapse_triangulate=True)
    return flagge(o, vc=True)

# ================================================================ Architektur
D = 0.25  # Wandstärke
kiste('boden', (22.0, 12.0, 0.1), (11.0, 6.0, -0.05), M['boden'], lm='arch', uv=2.4)
kiste('decke', (22.6, 12.6, 0.12), (11.0, 6.0, H + 0.06), M['decke'], lm='arch', uv=4.0)
kiste('terrasse', (17.0, 3.4, 0.1), (8.5, 13.7, -0.08), M['deck'], lm='arch', uv=2.4)
kiste('dachrand', (22.6, 3.6, 0.3), (11.0, 13.6, H + 0.2), M['putz_a'], lm='arch', uv=3.0)   # Vordach über der Terrasse

def wand(name, x0, y0, x1, y1, m=M['putz'], z0=0.0, z1=H):
    """Wand von (x0,y0) nach (x1,y1), Stärke D, mittig auf der Linie."""
    dx, dy = x1 - x0, y1 - y0; l = math.hypot(dx, dy)
    gr = (l, D, z1 - z0) if abs(dx) > abs(dy) else (D, l, z1 - z0)
    return kiste(name, gr, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), m, lm='arch', uv=2.0)

def wand_mit_oeffnung(name, achse, fest, a0, a1, o0, o1, sturz=2.4, m=M['putz']):
    """Wand entlang 'x' oder 'y' von a0 bis a1 mit Öffnung o0..o1 (Durchgang bis Sturzhöhe)."""
    teile = [(a0, o0), (o1, a1)]
    for i, (p, q) in enumerate(teile):
        if q - p > 0.02:
            (wand(f'{name}_{i}', p, fest, q, fest, m) if achse == 'x' else wand(f'{name}_{i}', fest, p, fest, q, m))
    if sturz >= H - 0.01: return
    if achse == 'x': wand(f'{name}_sturz', o0, fest, o1, fest, m, z0=sturz)
    else: wand(f'{name}_sturz', fest, o0, fest, o1, m, z0=sturz)

def glasfront(name, achse, fest, a0, a1, felder, z0=0.0, z1=H):
    """Raumhohe Verglasung mit schmalen schwarzen Rahmen."""
    l = a1 - a0; mitte = (a0 + a1) / 2; zm = (z0 + z1) / 2
    def k(n, gr, pos): return kiste(n, gr, pos, M['rahmen'])
    if achse == 'x':
        k(f'{name}_oben', (l, 0.1, 0.08), (mitte, fest, z1 - 0.04)); k(f'{name}_unten', (l, 0.1, 0.05), (mitte, fest, z0 + 0.025))
        for i in range(felder + 1): k(f'{name}_pfosten{i}', (0.05, 0.1, z1 - z0), (a0 + l * i / felder, fest, zm))
        g = kiste(f'{name}_glas', (l, 0.012, z1 - z0), (mitte, fest, zm), M['glas'])
    else:
        k(f'{name}_oben', (0.1, l, 0.08), (fest, mitte, z1 - 0.04)); k(f'{name}_unten', (0.1, l, 0.05), (fest, mitte, z0 + 0.025))
        for i in range(felder + 1): k(f'{name}_pfosten{i}', (0.1, 0.05, z1 - z0), (fest, a0 + l * i / felder, zm))
        g = kiste(f'{name}_glas', (0.012, l, z1 - z0), (fest, mitte, zm), M['glas'])
    flagge(g, bake=False); g.visible_shadow = False   # Sonne fällt durchs Glas

# Außenwände
wand('aussen_west', -D / 2, -D / 2, -D / 2, 12.0)                     # Logo-Wand innen bei x = 0 (Wohnen) und Flur
wand_mit_oeffnung('aussen_sued', 'x', -D / 2, -D / 2, 22 + D / 2, 1.0, 2.1, sturz=2.25)   # Eingangstür
wand('aussen_ost_ankleide', 22 + D / 2, 0, 22 + D / 2, 5.0)
# Bürofenster in der Südwand (Brüstung + Sturz statt Wand)
glasfront('fenster_buero', 'x', -D / 2, 5.2, 9.3, 3, z0=0.75, z1=2.6)
for o in list(bpy.data.objects):
    if o.name.startswith('aussen_sued_1'):  # Südwand-Teil hinter dem Bürofenster aufschneiden
        bpy.data.objects.remove(o, do_unlink=True)
wand('aussen_sued_a', 2.1, -D / 2, 5.2, -D / 2); wand('aussen_sued_b', 9.3, -D / 2, 22 + D / 2, -D / 2)
wand('aussen_sued_bruestung', 5.2, -D / 2, 9.3, -D / 2, z1=0.75); wand('aussen_sued_sturz', 5.2, -D / 2, 9.3, -D / 2, z0=2.6)
glasfront('front_nord', 'x', 12.0, 0.0, 22.0, 11)
glasfront('front_ost', 'y', 22.0, 5.0, 12.0, 3)
# Glasgeländer der Terrasse
g = kiste('gelaender_glas', (17.0, 0.02, 1.0), (8.5, 15.35, 0.5), M['glas']); flagge(g, bake=False); g.visible_shadow = False
kiste('gelaender_handlauf', (17.0, 0.05, 0.04), (8.5, 15.35, 1.02), M['rahmen'])

# Innenwände
wand_mit_oeffnung('flur_nord', 'x', 5.0, 0.0, 4.0, 0.7, 3.3, sturz=H)       # Flur offen zum Wohnen
wand('flur_ost', 4.0, 0.0, 4.0, 5.0)
wand_mit_oeffnung('buero_nord', 'x', 5.0, 4.0, 10.0, 5.4, 8.2, sturz=H)     # Büro offen zum Wohnen
wand('bad_west', 10.0, 0.0, 10.0, 5.0)
wand('kueche_sued', 10.0, 5.0, 16.0, 5.0)
wand('bad_ost', 16.0, 0.0, 16.0, 5.0)
wand_mit_oeffnung('schlafen_west', 'y', 16.0, 5.0, 12.0, 9.3, 11.3, sturz=2.4)
wand_mit_oeffnung('ankleide_nord', 'x', 5.0, 16.0, 22.0, 20.4, 21.6, sturz=2.4)

# Lichtvoute an der Glasfront (indirektes Licht) und Sockelleisten
g = kiste('voute_led', (21.6, 0.04, 0.02), (11.0, 11.55, H - 0.06), M['led']); flagge(g, bake=False)
kiste('voute', (21.8, 0.5, 0.12), (11.0, 11.7, H - 0.06), M['decke'], lm='arch', uv=3.0)

# ================================================================ Wohnzimmer (Logo-Komposition an der Westwand)
def logo_sofa():
    """Modernes Sofa nach dem Logo: tiefes Polster, zwei Sitzkissen, zwei Rückenkissen, nach außen geneigte Arme, konische Nussbeine.
    Lokal gebaut: Breite entlang x, Front zeigt nach -y."""
    B, T = 2.5, 1.0
    t = []
    t.append(polster('sofa_sockel', (B, T, 0.24), (0, 0, 0.28), M['sofa'], rad=0.05, puff=0.0, falten=0.002))
    for i, x in enumerate((-0.53, 0.53)):
        t.append(polster(f'sofa_sitz{i}', (1.04, 0.78, 0.17), (x, -0.07, 0.49), M['sofa'], rad=0.06, puff=0.022, keder=M['keder']))
        t.append(polster(f'sofa_ruecken{i}', (1.04, 0.24, 0.5), (x, 0.31, 0.78), M['sofa'], rad=0.09, puff=0.03, rot=(math.radians(-12), 0, 0), keder=M['keder']))
    t.append(polster('sofa_lehne', (B, 0.18, 0.44), (0, 0.42, 0.62), M['sofa'], rad=0.06, puff=0.0, falten=0.002))
    for s in (-1, 1):  # Arme: leicht nach außen geneigt wie im Logo
        t.append(polster(f'sofa_arm{s}', (0.2, T, 0.5), (s * 1.17, 0.0, 0.55), M['sofa'], rad=0.08, puff=0.0, rot=(0, math.radians(-10 * s), 0), falten=0.002))
    for i, (bx, by) in enumerate(((-1.1, -0.38), (1.1, -0.38), (-1.1, 0.38), (1.1, 0.38))):
        t.append(zyl(f'sofa_bein{i}', 0.022, 0.19, (bx, by, 0.085), M['nuss'], r2=0.013, rot=(math.radians(12 * (1 if by > 0 else -1)), math.radians(-12 * (1 if bx > 0 else -1)), 0), n=16))
    # Zierkissen: dunkles Oliv-Samt und Leinen, schräg gestellt
    t.append(polster('sofa_kissen_oliv', (0.5, 0.15, 0.46), (-0.75, 0.13, 0.78), M['kis_d'], rad=0.07, puff=0.06, rot=(math.radians(-18), 0, math.radians(8)), falten=0.005))
    t.append(polster('sofa_kissen_leinen', (0.44, 0.14, 0.4), (-0.3, 0.16, 0.74), M['kis_h'], rad=0.07, puff=0.05, rot=(math.radians(-16), 0, math.radians(-6)), falten=0.005))
    return t

sofa = gruppe(logo_sofa(), 'sofa', pos=(0.62, 8.0, 0), rz=math.radians(90))   # Rücken an der Westwand, Front nach +x

# drei Pendelleuchten über der linken Sofahälfte (von der Kamera aus links = Richtung -y)
for i, (ly, lz) in enumerate(((7.05, 1.95), (7.4, 1.72), (7.75, 2.0))):
    lx = 1.05 + 0.08 * i
    rohr(f'pendel_kabel_{i}', [(lx, ly, lz + 0.17), (lx, ly, H)], 0.0035, M['schwarz'])
    p = drehkoerper(f'pendel_{i}', [(0.0, 0.17), (0.07, 0.17), (0.085, 0.15), (0.085, -0.14), (0.08, -0.15), (0.072, -0.13)], (lx, ly, lz), M['schwarz'], lm='moebel')
    drehkoerper(f'pendel_ring_{i}', [(0.072, -0.13), (0.08, -0.15), (0.06, -0.15)], (lx, ly, lz), M['messing'])
    g = zyl(f'pendel_glut_{i}', 0.06, 0.004, (lx, ly, lz - 0.135), M['glut'], n=32); flagge(g, bake=False)
# sechs Nussholz-Lamellen rechts vom Sofa, die letzten zwei kürzer (wie im Logo)
for i, laenge in enumerate((H, H, H, H, H - 0.5, H - 0.85)):
    kiste(f'lamelle_{i}', (0.045, 0.06, laenge), (0.03, 9.55 + i * 0.16, H - laenge / 2), M['nuss'], fase=0.006, seg=1, lm='moebel', uv=0.5)
# Teppich mit runden Ecken
polster('teppich_wohnen', (3.6, 2.7, 0.018), (2.55, 8.0, 0.009), M['teppich'], rad=0.009, puff=0.0, falten=0.0, schnitte=6, lm='arch')
# Couchtisch: zwei Travertin-Trommeln
t = [drehkoerper('tisch_a', [(0.0, 0.0), (0.46, 0.0), (0.48, 0.02), (0.48, 0.33), (0.46, 0.35), (0.0, 0.35)], (0, 0, 0), M['stein']),
     drehkoerper('tisch_b', [(0.0, 0.0), (0.3, 0.0), (0.32, 0.02), (0.32, 0.25), (0.3, 0.27), (0.0, 0.27)], (0.55, 0.62, 0), M['stein'])]
gruppe(t, 'couchtisch', pos=(2.55, 7.8, 0))
# Bücherstapel und Schale auf dem Couchtisch
for i in range(3):
    kiste(f'buch_couch_{i}', (0.3 - i * 0.03, 0.22 - i * 0.015, 0.035), (2.4, 7.65, 0.368 + i * 0.036), BUCH[i * 2], rot=(0, 0, math.radians(8 * i - 6)), fase=0.003, seg=1, lm='moebel', uv=0.3)
importiere('ceramic_vase_02', (2.75, 7.95, 0.35), skala=0.8)
importiere('mid_century_lounge_chair', (3.7, 10.15, 0), rot_z=math.radians(150))
importiere('potted_plant_02', (0.6, 11.25, 0), skala=1.7)
# Vorhänge (Leinen) an der Glasfront, seitlich gerafft
def vorhang(name, x0, x1, y):
    n = int((x1 - x0) / 0.035)
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    spalten = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n; dy = 0.05 * math.sin(i * 0.9)
        spalten.append([bm.verts.new((x, y + dy, z)) for z in (0.01, H - 0.1)])
    for i in range(n): bm.faces.new((spalten[i][0], spalten[i + 1][0], spalten[i + 1][1], spalten[i][1]))
    bm.to_mesh(me); bm.free(); o = bpy.data.objects.new(name, me); sz.collection.objects.link(o)
    me.materials.append(M['kis_h']); mod_anwenden(o, 'SOLIDIFY', thickness=0.01)
    wuerfel_uv(o, 0.6); aktiv(o); bpy.ops.object.shade_smooth(); o.select_set(False)
    rohr(name + '_schiene', [(x0 - 0.05, y, H - 0.06), (x1 + 0.05, y, H - 0.06)], 0.01, M['schwarz'])
    return flagge(o, lm='moebel')
vorhang('vorhang_west', 0.15, 0.95, 11.72)
vorhang('vorhang_ost', 20.9, 21.75, 11.72)

# ================================================================ Büro (Süd, Fenster)
t = [kiste('schreibtisch_platte', (1.8, 0.78, 0.035), (0, 0, 0.74), M['eiche'], fase=0.004, seg=2, uv=1.0)]
for s in (-1, 1):
    t.append(kiste(f'schreibtisch_wange{s}', (0.035, 0.7, 0.72), (s * 0.84, 0, 0.36), M['eiche'], fase=0.003, seg=1, uv=1.0))
t.append(kiste('schreibtisch_lade', (0.5, 0.5, 0.11), (0.55, -0.08, 0.66), M['eiche'], fase=0.003, seg=1, uv=1.0))
gruppe(t, 'schreibtisch', pos=(7.25, 0.75, 0), rz=math.radians(180))
# Regalwand Nussbaum an der Flurwand (x = 4), mit beleuchteten Fächern und Büchern
t = [kiste('regal_rueckwand', (0.02, 4.2, 2.5), (-0.18, 0, 1.25), M['nuss'], uv=1.0)]
for r in range(5): t.append(kiste(f'regal_boden{r}', (0.36, 4.2, 0.03), (0, 0, 0.08 + r * 0.6), M['nuss'], fase=0.003, seg=1, uv=1.0))
for c in range(5): t.append(kiste(f'regal_seite{c}', (0.36, 0.03, 2.43), (0, -2.085 + c * 1.0425, 1.295), M['nuss'], fase=0.003, seg=1, uv=1.0))
regal = gruppe(t, 'regal', pos=(4.32, 2.5, 0))
for r in range(4):
    boden = 0.095 + r * 0.6
    g = kiste(f'regal_led_{r}', (0.01, 4.1, 0.008), (4.45, 2.5, boden + 0.57), M['led']); flagge(g, bake=False)
    for c in range(4):
        if (r + c) % 3 == 1: continue
        yy = 2.5 - 2.07 + c * 1.0425 + 0.05
        for b in range(random.randint(5, 10)):
            dicke = random.uniform(0.025, 0.045); hoch = random.uniform(0.22, 0.32)
            kiste(f'buch_{r}{c}{b}', (random.uniform(0.18, 0.24), dicke, hoch), (4.32, yy + dicke / 2, boden + hoch / 2), random.choice(BUCH), fase=0.003, seg=1, lm='moebel', uv=0.3)
            yy += dicke + 0.004
importiere('pachira_aquatica_01', (9.3, 4.3, 0), skala=1.05)
drehkoerper('schreibtischleuchte', [(0.0, 0.775), (0.08, 0.775), (0.08, 0.785), (0.012, 0.79), (0.012, 1.15), (0.0, 1.15)], (6.55, 0.6, 0), M['messing'], lm='moebel')
g = drehkoerper('schreibtischleuchte_schirm', [(0.13, 1.08), (0.09, 1.24)], (6.55, 0.6, 0), M['schirm']); flagge(g, bake=False)
punktlicht_spaeter = [((6.55, 0.6, 1.1), 15)]

# ================================================================ Küche und Essen
# hohe Eichenfront an der Südwand mit Nische (Travertin-Rückwand und Arbeitsfläche)
t = []
for i, (x0, x1) in enumerate(((10.15, 12.0), (14.6, 15.85))):
    t.append(kiste(f'kueche_hoch{i}', (x1 - x0, 0.62, 2.7), ((x0 + x1) / 2, 5.43, 1.35), M['eiche'], uv=1.2))
    n = round((x1 - x0) / 0.6)
    for j in range(1, n): t.append(kiste(f'kueche_fuge{i}{j}', (0.004, 0.005, 2.6), (x0 + (x1 - x0) * j / n, 5.742, 1.35), M['schwarz']))
t.append(kiste('kueche_unter', (2.6, 0.62, 0.86), (13.3, 5.43, 0.43), M['eiche'], uv=1.2))
t.append(kiste('kueche_platte', (2.6, 0.64, 0.04), (13.3, 5.44, 0.88), M['stein'], uv=1.0))
t.append(kiste('kueche_rueckwand', (2.6, 0.02, 0.62), (13.3, 5.13, 1.21), M['stein'], uv=1.0))
t.append(kiste('kueche_ober', (2.6, 0.4, 0.48), (13.3, 5.33, 2.46), M['eiche'], uv=1.2))
gruppe(t, 'kuechenzeile')
g = kiste('kueche_led', (2.5, 0.02, 0.01), (13.3, 5.5, 2.21), M['led']); flagge(g, bake=False)
rohr('armatur', [(13.3, 5.2, 0.9), (13.3, 5.2, 1.22), (13.3, 5.42, 1.24), (13.3, 5.47, 1.16)], 0.012, M['messing'])
# Kochinsel aus Travertin, Wasserfallkanten
t = [kiste('insel_platte', (3.0, 1.05, 0.06), (0, 0, 0.9), M['stein'], fase=0.004, seg=2, uv=1.0)]
for s in (-1, 1): t.append(kiste(f'insel_wange{s}', (0.06, 1.05, 0.87), (s * 1.47, 0, 0.435), M['stein'], uv=1.0))
t.append(kiste('insel_korpus', (2.8, 0.9, 0.82), (0, 0.02, 0.43), M['eiche'], uv=1.2))
gruppe(t, 'kochinsel', pos=(13.1, 6.95, 0))
importiere('wooden_bowl_01', (12.6, 7.0, 0.93), skala=1.1)
importiere('ceramic_vase_04', (13.9, 6.85, 0.93), skala=0.9)

# Esstisch Eiche, massiv, zwei Wangen
t = [kiste('esstisch_platte', (2.6, 1.05, 0.055), (0, 0, 0.74), M['eiche'], fase=0.006, seg=3, uv=1.2)]
for s in (-1, 1): t.append(kiste(f'esstisch_wange{s}', (0.08, 0.8, 0.71), (s * 0.95, 0, 0.355), M['eiche'], fase=0.004, seg=2, uv=1.2))
t.append(kiste('esstisch_traverse', (1.9, 0.06, 0.08), (0, 0, 0.62), M['eiche'], uv=1.2))
gruppe(t, 'esstisch', pos=(12.5, 10.0, 0))

def schalenstuhl(name, pos, rz, polster_m=M['leder']):
    """Stuhl mit gebogener Schale (Eiche), gepolstertem Sitz, schlanken schwarzen Beinen."""
    t = []
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.27, depth=0.34, location=(0, 0.02, 0.82))
    s = bpy.context.object; s.name = name + '_schale'
    bm = bmesh.new(); bm.from_mesh(s.data)
    weg = [v for v in bm.verts if math.degrees(math.atan2(v.co.x, v.co.y)) > 70 or math.degrees(math.atan2(v.co.x, v.co.y)) < -70]
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if len(f.verts) > 4], context='FACES')
    bmesh.ops.delete(bm, geom=weg, context='VERTS'); bm.to_mesh(s.data); bm.free()
    mod_anwenden(s, 'SOLIDIFY', thickness=0.022, offset=0)
    mod_anwenden(s, 'BEVEL', width=0.006, segments=2)
    s.data.materials.append(M['eiche']); wuerfel_uv(s, 0.4); glaetten(s); t.append(s)
    t.append(polster(name + '_rueckenpolster', (0.42, 0.04, 0.26), (0, 0.255, 0.82), polster_m, rad=0.018, puff=0.008, falten=0.002))
    t.append(polster(name + '_sitz', (0.47, 0.46, 0.07), (0, -0.02, 0.47), polster_m, rad=0.03, puff=0.012, falten=0.003, keder=M['schwarz']))
    t.append(kiste(name + '_sitzplatte', (0.44, 0.42, 0.02), (0, -0.02, 0.425), M['eiche'], fase=0.004, seg=2))
    for i, (bx, by) in enumerate(((-0.19, -0.18), (0.19, -0.18), (-0.19, 0.16), (0.19, 0.16))):
        t.append(rohr(name + f'_bein{i}', [(bx * 0.9, by * 0.9, 0.42), (bx * 1.12, by * 1.12, 0.0)], 0.011, M['schwarz']))
    return gruppe(t, name, pos=pos, rz=rz)

for i, x in enumerate((11.65, 12.5, 13.35)):
    schalenstuhl(f'stuhl_n{i}', (x, 10.78, 0), math.radians(180))
    schalenstuhl(f'stuhl_s{i}', (x, 9.22, 0), 0.0)
schalenstuhl('buerostuhl', (7.15, 1.55, 0), math.radians(10))
# zwei Kuppelleuchten über dem Esstisch
for i, lx in enumerate((11.85, 13.15)):
    rohr(f'ess_kabel_{i}', [(lx, 10.0, 1.95), (lx, 10.0, H)], 0.0035, M['schwarz'])
    drehkoerper(f'ess_kuppel_{i}', [(0.02, 1.95), (0.05, 1.95), (0.16, 1.9), (0.25, 1.8), (0.3, 1.67), (0.31, 1.62), (0.295, 1.62), (0.285, 1.66), (0.24, 1.77), (0.15, 1.87), (0.04, 1.92)], (lx, 10.0, 0), M['schwarz'], lm='moebel')
    g = drehkoerper(f'ess_glut_{i}', [(0.0, 1.7), (0.2, 1.7), (0.27, 1.64)], (lx, 10.0, 0), M['glut']); flagge(g, bake=False)
importiere('ceramic_vase_01', (12.2, 10.05, 0.77), skala=0.9)
importiere('brass_vase_01', (12.9, 9.9, 0.77), skala=0.8)

# ================================================================ Schlafzimmer
def bett():
    """Polsterbett: Rahmen, hohes Kopfteil mit Pfeifensteppung, Matratze, Bettdecke (Stoffsimulation), Kissen, Plaid. Lokal: Kopf bei +y."""
    t = []
    t.append(polster('bett_rahmen', (2.0, 2.2, 0.3), (0, 0, 0.2), M['bett'], rad=0.05, puff=0.0, falten=0.002))
    for i in range(7):  # Pfeifensteppung: senkrechte gepolsterte Bahnen
        t.append(polster(f'bett_kopf{i}', (0.36, 1.2, 0.13), (-1.08 + i * 0.36, 1.1, 0.75), M['bett'], rad=0.06, puff=0.025, rot=(math.pi / 2, 0, 0), falten=0.003))
    t.append(polster('bett_matratze', (1.84, 2.02, 0.22), (0, -0.05, 0.46), M['waesche'], rad=0.06, puff=0.01, falten=0.002))
    for i, x in enumerate((-0.45, 0.45)):
        t.append(polster(f'bett_kissen{i}', (0.78, 0.5, 0.17), (x, 0.72, 0.68), M['waesche'], rad=0.08, puff=0.07, rot=(math.radians(-28), 0, 0), falten=0.006))
    t.append(polster('bett_zierkissen', (0.5, 0.42, 0.13), (-0.1, 0.48, 0.66), M['kis_d'], rad=0.07, puff=0.05, rot=(math.radians(-24), 0, math.radians(6)), falten=0.005))
    return t

def stoff(name, gr, n, pos, ueber, m, dicke=0.045, frames=40, masse=0.4, biegung=1.5):
    """Tuch fällt per Stoffsimulation auf die Objekte 'ueber'."""
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=n[0], y_subdivisions=n[1], size=1, location=pos)
    d = bpy.context.object; d.name = name; d.scale = (gr[0], gr[1], 1); bpy.ops.object.transform_apply(scale=True)
    for o in ueber:
        c = o.modifiers.new('kollision', 'COLLISION'); c.settings.thickness_outer = 0.012
    cl = d.modifiers.new('stoff', 'CLOTH'); cs = cl.settings
    cs.quality = 6; cs.mass = masse; cs.tension_stiffness = 8; cs.compression_stiffness = 8; cs.bending_stiffness = biegung
    cl.collision_settings.distance_min = 0.008; cl.collision_settings.use_self_collision = False
    sz.frame_start = 1; sz.frame_end = frames
    for f in range(1, frames + 1): sz.frame_set(f)
    aktiv(d); bpy.ops.object.modifier_apply(modifier='stoff')
    for o in ueber:
        if 'kollision' in o.modifiers: o.modifiers.remove(o.modifiers['kollision'])
    sz.frame_set(1)
    mod_anwenden(d, 'SOLIDIFY', thickness=dicke, offset=1)
    mod_anwenden(d, 'SUBSURF', levels=1, render_levels=1)
    d.data.materials.append(m); wuerfel_uv(d, 0.5); aktiv(d); bpy.ops.object.shade_smooth(); d.select_set(False)
    return d

bt = bett()
koll = [o for o in bt if o.name in ('bett_matratze', 'bett_rahmen')]
decke = stoff('bett_decke', (2.24, 1.6), (56, 44), (0, -0.32, 0.72), koll, M['waesche'])
plaid = stoff('bett_plaid', (2.3, 0.6), (60, 18), (0.0, -0.78, 0.95), koll + [decke], M['plaid'], dicke=0.012, masse=0.25, biegung=0.6)
gruppe(bt + [decke, plaid], 'bett', pos=(18.6, 6.2, 0), rz=math.radians(180))   # Kopf an der Südwand (y = 5)
for i, x in enumerate((17.15, 20.05)):
    kiste(f'nachttisch_{i}', (0.5, 0.42, 0.34), (x, 5.36, 0.42), M['eiche'], fase=0.004, seg=2, lm='moebel', uv=0.6)
    kiste(f'nachttisch_fuge_{i}', (0.46, 0.004, 0.004), (x, 5.15, 0.42), M['schwarz'])
    drehkoerper(f'nachtlampe_fuss_{i}', [(0.0, 0.59), (0.07, 0.59), (0.085, 0.65), (0.06, 0.78), (0.015, 0.8), (0.015, 0.86), (0.0, 0.86)], (x, 5.36, 0), M['keramik'], lm='moebel')
    g = drehkoerper(f'nachtlampe_schirm_{i}', [(0.15, 0.82), (0.11, 1.02)], (x, 5.36, 0), M['schirm']); flagge(g, bake=False)
polster('bett_bank', (1.5, 0.45, 0.14), (18.6, 8.0, 0.4), M['bett'], rad=0.05, puff=0.02, keder=M['keder'], lm='moebel')
for i, (bx, by) in enumerate(((-0.65, -0.17), (0.65, -0.17), (-0.65, 0.17), (0.65, 0.17))):
    zyl(f'bank_bein{i}', 0.018, 0.33, (18.6 + bx, 8.0 + by, 0.165), M['nuss'], r2=0.012, n=12)
polster('teppich_schlafen', (3.0, 2.4, 0.016), (18.6, 7.0, 0.008), M['teppich'], rad=0.008, puff=0.0, falten=0.0, schnitte=6, lm='arch')
importiere('potted_plant_04', (21.4, 11.2, 0), skala=1.6)
importiere('mid_century_lounge_chair', (21.0, 9.9, 0), rot_z=math.radians(240))

# Ankleide: offene Schranksysteme mit Licht (durch die Öffnung sichtbar)
for i, (x0, x1) in enumerate(((16.2, 21.8),)):
    t = [kiste('ankleide_korpus', (x1 - x0, 0.6, 2.6), ((x0 + x1) / 2, 0.42, 1.3), M['eiche'], uv=1.2)]
    for j in range(1, 6): t.append(kiste(f'ankleide_wand{j}', (0.025, 0.56, 2.5), (x0 + (x1 - x0) * j / 6, 0.45, 1.3), M['eiche']))
    t.append(kiste('ankleide_boden', (x1 - x0, 0.56, 0.025), ((x0 + x1) / 2, 0.45, 1.7), M['eiche']))
    gruppe(t, 'ankleide')
    rohr('ankleide_stange', [(x0 + 0.1, 0.5, 1.6), (x1 - 0.1, 0.5, 1.6)], 0.012, M['messing'])
    g = kiste('ankleide_led', (x1 - x0 - 0.1, 0.01, 0.01), ((x0 + x1) / 2, 0.73, 2.55), M['led']); flagge(g, bake=False)
for i in range(14):  # Kleidung als schlichte Hängeteile
    x = 16.4 + i * 0.38 + random.uniform(-0.05, 0.05)
    polster(f'kleid_{i}', (0.08, 0.5, random.uniform(0.7, 1.0)), (x, 0.5, 1.15), random.choice([M['kis_h'], M['bett'], M['plaid'], M['kis_d']]), rad=0.03, puff=0.0, falten=0.004, schnitte=5, lm='moebel')

# ================================================================ Flur
kiste('flur_konsole', (1.4, 0.35, 0.05), (2.0, 4.62, 0.85), M['stein'], fase=0.004, seg=2, lm='moebel')
drehkoerper('flur_spiegel', [(0.0, 0.0), (0.42, 0.0), (0.42, 0.02), (0.0, 0.02)], (2.0, 4.86, 1.55), M['spiegel']).rotation_euler = (math.pi / 2, 0, 0)
kiste('tuer', (1.06, 0.05, 2.22), (1.55, 0.02, 1.11), M['eiche'], fase=0.003, seg=1, lm='moebel')

# ================================================================ Licht
def flaechenlicht(name, pos, rot, gr, staerke, farbe=(1, 0.97, 0.93), portal=False):
    l = bpy.data.lights.new(name, 'AREA'); l.shape = 'RECTANGLE'; l.size, l.size_y = gr; l.energy = staerke; l.color = farbe
    if portal: l.cycles.is_portal = True
    o = bpy.data.objects.new(name, l); o.location = pos; o.rotation_euler = rot
    o.visible_camera = False; o.visible_glossy = False; o.visible_transmission = False
    sz.collection.objects.link(o); return o
def punktlicht(name, pos, staerke, farbe=(1, 0.8, 0.58), r=0.05):
    l = bpy.data.lights.new(name, 'POINT'); l.energy = staerke; l.color = farbe; l.shadow_soft_size = r
    o = bpy.data.objects.new(name, l); o.location = pos; sz.collection.objects.link(o); return o

w = bpy.data.worlds.new('welt'); sz.world = w; w.use_nodes = True
env = w.node_tree.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(os.path.join(A, 'hdri', 'alps_field.hdr'))
mp = w.node_tree.nodes.new('ShaderNodeMapping'); tc = w.node_tree.nodes.new('ShaderNodeTexCoord')
mp.inputs['Rotation'].default_value = (0, 0, math.radians(-108))
w.node_tree.links.new(tc.outputs['Generated'], mp.inputs['Vector']); w.node_tree.links.new(mp.outputs['Vector'], env.inputs['Vector'])
w.node_tree.links.new(env.outputs['Color'], w.node_tree.nodes['Background'].inputs['Color'])
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.4
# Sonne: später Nachmittag, tief, warm, fällt durch die Nordfront schräg in den Raum
sonne = bpy.data.lights.new('sonne', 'SUN'); sonne.energy = 5.0; sonne.angle = math.radians(1.2); sonne.color = (1.0, 0.88, 0.72)
so = bpy.data.objects.new('sonne', sonne); sz.collection.objects.link(so)
so.rotation_euler = Vector((0.55, -0.8, -0.32)).to_track_quat('-Z', 'Y').to_euler()
# Portale an den Fenstern (weniger Rauschen beim Backen)
flaechenlicht('portal_nord', (11.0, 12.05, H / 2), (math.radians(-90), 0, 0), (22.0, H), 1, portal=True)
flaechenlicht('portal_ost', (22.05, 8.5, H / 2), (0, math.radians(90), 0), (H, 7.0), 1, portal=True)
flaechenlicht('portal_buero', (7.25, -0.2, 1.7), (math.radians(90), 0, 0), (4.1, 1.85), 1, portal=True)
for i, (ly, lz) in enumerate(((7.05, 1.95), (7.4, 1.72), (7.75, 2.0))):
    punktlicht(f'licht_pendel_{i}', (1.05 + 0.08 * i, ly, lz - 0.2), 12)
for i, lx in enumerate((11.85, 13.15)):
    punktlicht(f'licht_kuppel_{i}', (lx, 10.0, 1.6), 30, r=0.15)
for i, (pos, e) in enumerate(punktlicht_spaeter): punktlicht(f'licht_tisch_{i}', pos, e, r=0.1)
for i, x in enumerate((17.15, 20.05)): punktlicht(f'licht_nacht_{i}', (x, 5.36, 0.95), 10, r=0.1)

# ================================================================ Kamerastationen und Wegpunkte
def kamera(name, pos, ziel, fov=50):
    c = bpy.data.cameras.new(name); c.lens_unit = 'FOV'; c.angle = math.radians(fov); c.sensor_fit = 'VERTICAL'
    o = bpy.data.objects.new(name, c); o.location = pos; sz.collection.objects.link(o)
    o.rotation_euler = (Vector(ziel) - Vector(pos)).to_track_quat('-Z', 'Y').to_euler(); return o
def weg(name, pos):
    e = bpy.data.objects.new(name, None); e.location = pos; sz.collection.objects.link(e); return e

kamera('station_0_logo',    (6.4, 8.0, 1.45),  (0.0, 8.0, 1.4), fov=40)
kamera('station_1_wohnen',  (6.6, 5.7, 1.55),  (1.4, 8.9, 0.85), fov=52)
kamera('station_2_sofa',    (3.55, 6.65, 1.2), (1.0, 8.15, 0.6), fov=46)
weg('weg_2_0', (5.6, 6.1, 1.45))
kamera('station_3_buero',   (6.9, 6.3, 1.55),  (6.9, 1.0, 0.9), fov=56)
kamera('station_4_essen',   (9.4, 6.4, 1.6),   (12.9, 10.1, 0.75), fov=54)
weg('weg_4_0', (11.4, 8.2, 1.55)); weg('weg_4_1', (14.6, 8.25, 1.55)); weg('weg_4_2', (15.4, 10.2, 1.55))
kamera('station_5_schlafen', (16.7, 10.6, 1.55), (18.9, 6.0, 0.6), fov=56)
sz.camera = bpy.data.objects['station_0_logo']

n_dr = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in sz.objects if o.type == 'MESH')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HIER, 'szene.blend'))
print('fertig', len(bpy.data.objects), 'Objekte,', n_dr, 'Dreiecke')
