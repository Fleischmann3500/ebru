"""Licht backen (Cycles): Architektur und eigene Möbel in Lichtatlanten, importierte Modelle in Vertex-Farben.
Aufruf: python3 backen.py [samples] [atlas_px]   ->  szene_gebacken.blend + licht/<gruppe>.exr
Gebacken wird nur Licht (direkt + indirekt, ohne Eigenfarbe). Die Website multipliziert es mit der Materialfarbe."""
import bpy, os, sys, time
HIER = os.path.dirname(os.path.abspath(__file__))
SAMPLES = int(sys.argv[1]) if len(sys.argv) > 1 else 64
PX = int(sys.argv[2]) if len(sys.argv) > 2 else 2048
NUR_VERTEX = 'vertex' in sys.argv   # nur Vertex-Durchgang auf der schon gebackenen Szene wiederholen
bpy.ops.wm.open_mainfile(filepath=os.path.join(HIER, 'szene_gebacken.blend' if NUR_VERTEX else 'szene.blend'))
sz = bpy.context.scene
sz.render.engine = 'CYCLES'; sz.cycles.device = 'CPU'; sz.cycles.samples = SAMPLES
sz.cycles.sample_clamp_indirect = 1.0; sz.cycles.max_bounces = 6
sz.render.bake.margin = 8; sz.render.bake.use_pass_direct = True; sz.render.bake.use_pass_indirect = True; sz.render.bake.use_pass_color = False
os.makedirs(os.path.join(HIER, 'licht'), exist_ok=True)

meshes = [o for o in sz.objects if o.type == 'MESH']
# Glas beim Backen ausblenden (sonst Schatten hinter Fenstern), Leuchtflächen bleiben als Lichtquelle sichtbar
for o in meshes:
    if o.get('bake', 1) == 0 and any(s.material and s.material.name == 'glas' for s in o.material_slots): o.hide_render = True
# Kleinteile ohne Gruppe (Rahmen, Kabel, Fugen) bekommen Vertex-Licht
for o in meshes:
    if 'lm' not in o and 'vc' not in o and o.get('bake', 1) != 0: o['vc'] = 1

def auswahl(objs):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]

def lightmap_uv(objs):
    for o in objs:
        uv = o.data.uv_layers
        if 'Lightmap' not in uv: uv.new(name='Lightmap')
        for l in uv: l.active_render = (l.name != 'Lightmap') and l == uv[0]
        uv.active = uv['Lightmap']
    auswahl(objs)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.002, scale_to_bounds=False)
    bpy.ops.uv.pack_islands(udim_source='CLOSEST_UDIM', rotate=True, margin=0.004, margin_method='FRACTION')
    bpy.ops.object.mode_set(mode='OBJECT')

def backe_atlas(gruppe):
    objs = [o for o in meshes if o.get('lm') == gruppe]
    t = time.time(); lightmap_uv(objs)
    px = PX * 2   # beide Atlanten 2048 (V2: große Wohnung, viele Möbel)
    img = bpy.data.images.new(f'licht_{gruppe}', px, px, float_buffer=True, alpha=False)
    mats = {s.material for o in objs for s in o.material_slots if s.material}
    for m in mats:
        nt = m.node_tree
        n = nt.nodes.get('bake_ziel') or nt.nodes.new('ShaderNodeTexImage'); n.name = 'bake_ziel'
        n.image = img; nt.nodes.active = n
    auswahl(objs)
    bpy.ops.object.bake(type='DIFFUSE', pass_filter={'DIRECT', 'INDIRECT'}, target='IMAGE_TEXTURES', margin=8, use_clear=True)
    img.filepath_raw = os.path.join(HIER, 'licht', f'{gruppe}.exr'); img.file_format = 'OPEN_EXR'; img.save()
    print(f'Atlas {gruppe}: {len(objs)} Objekte, {time.time() - t:.0f} s', flush=True)

def backe_vertex():
    objs = [o for o in meshes if o.get('vc') and not o.hide_render]
    t = time.time()
    for o in objs:
        ca = o.data.color_attributes
        a = ca.get('Licht') or ca.new(name='Licht', type='FLOAT_COLOR', domain='CORNER')
        ca.active_color = a
    auswahl(objs)
    # Vertex-Objekte: Farbe UND Licht (die Website braucht dann keine Texturen für importierte Modelle)
    bpy.ops.object.bake(type='DIFFUSE', pass_filter={'DIRECT', 'INDIRECT', 'COLOR'}, target='VERTEX_COLORS', use_clear=True)
    print(f'Vertex-Licht: {len(objs)} Objekte, {time.time() - t:.0f} s', flush=True)

if not NUR_VERTEX:
    for g in ('arch', 'moebel'): backe_atlas(g)
backe_vertex()
for o in meshes: o.hide_render = False
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HIER, 'szene_gebacken.blend'))
print('fertig')
