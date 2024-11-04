import bpy
import os, subprocess
from bpy.props import *

class ARNOLD_OT_Install(bpy.types.Operator):
    bl_idname = "arnold.install"
    bl_description="Install Arnold"
    bl_label = "Install Arnold"

    def execute(self, context):
        print("TEST")
        return {"FINISHED"}


classes = [ARNOLD_OT_Install]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)