import bpy, os
from bpy.props import *


class ArnoldPreferences(bpy.types.AddonPreferences):
    bl_idname = "btoa"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        arnold = scene.arnold

        blender_version = bpy.app.version_string.rsplit('.', 1)[0]  # e.g., "5.0"

        layout.prop(arnold, "version")
    
        if not os.path.exists(os.path.join(os.path.expanduser("~"), ".btoa", f"btoa-{blender_version}-{arnold.version}")):
            layout.operator("arnold.install", text="Install Arnold")
    
def register():
    bpy.utils.register_class(ArnoldPreferences)

def unregister():
    bpy.utils.unregister_class(ArnoldPreferences)