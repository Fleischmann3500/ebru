import bpy, os, sys, math
from mathutils import Vector
HIER = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(HIER, 'szene.blend'))
sz = bpy.context.scene; sz.render.engine='CYCLES'; sz.cycles.samples=24; sz.cycles.use_denoising=True
sz.render.resolution_x, sz.render.resolution_y = 1200, 700; sz.view_settings.view_transform='AgX'; sz.view_settings.exposure=-0.3
c = bpy.data.cameras.new('nah'); o = bpy.data.objects.new('nah', c); sz.collection.objects.link(o)
o.location = (0.2, -0.4, 1.0); d = Vector((0.0, 2.1, 0.55)) - o.location; o.rotation_euler = d.to_track_quat('-Z','Y').to_euler(); c.lens = 32
sz.camera = o; sz.render.filepath = os.path.join(HIER, 'vorschau', 'nah_sofa.jpg'); sz.render.image_settings.file_format='JPEG'
bpy.ops.render.render(write_still=True)
