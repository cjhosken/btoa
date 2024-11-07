import bpy
import os, subprocess
from bpy.props import *

class ARNOLD_OT_Install(bpy.types.Operator):
    bl_idname = "arnold.install"
    bl_description="Install Arnold"
    bl_label = "Install Arnold"

    def execute(self, context):
        print("""This has yet to be implemented! 
            The way I'm thinking this will work is that the delegate binaries will be prebuilt for each OS. 
            The user can then download and extract a compressed .zip which should quickly link everything up.""")
        return {"FINISHED"}


classes = [ARNOLD_OT_Install]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)