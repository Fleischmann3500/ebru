"""Vorschau aller Kamerastationen rendern: python3 vorschau.py [samples] [breite]"""
import bpy, os, sys
HIER = os.path.dirname(os.path.abspath(__file__))
samples = int(sys.argv[1]) if len(sys.argv) > 1 else 16
breite = int(sys.argv[2]) if len(sys.argv) > 2 else 960
bpy.ops.wm.open_mainfile(filepath=os.path.join(HIER, 'szene.blend'))
sz = bpy.context.scene
sz.render.engine = 'CYCLES'; sz.cycles.device = 'CPU'; sz.cycles.samples = samples
sz.cycles.use_denoising = True
try: sz.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
sz.cycles.sample_clamp_indirect = 1.0
sz.render.resolution_x, sz.render.resolution_y = breite, int(breite * 9 / 16)
sz.view_settings.view_transform = 'AgX'; sz.view_settings.look = 'AgX - Medium High Contrast'; sz.view_settings.exposure = 0.15
ziel = os.path.join(HIER, 'vorschau'); os.makedirs(ziel, exist_ok=True)
for o in sorted([o for o in sz.objects if o.type == 'CAMERA'], key=lambda o: o.name):
    sz.camera = o; sz.render.filepath = os.path.join(ziel, o.name + '.jpg'); sz.render.image_settings.file_format = 'JPEG'
    bpy.ops.render.render(write_still=True); print('gerendert', o.name, flush=True)
