import bpy, os
from bpy.props import *


class ArnoldPreferences(bpy.types.AddonPreferences):
    bl_idname = "btoa"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        arnold = scene.arnold
        layout.prop(arnold, "version")
        layout.operator("arnold.install", text="Install Arnold")
    
def register():
    bpy.utils.register_class(ArnoldPreferences)

def unregister():
    bpy.utils.unregister_class(ArnoldPreferences)