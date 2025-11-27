import bpy, os
from bpy.props import *

class ArnoldSceneProperties(bpy.types.PropertyGroup):
    version: EnumProperty(
        name="Arnold Version",
        description="Select Arnold version",
        items=[
            ('7.4.3.0', "7.4.3.0", "Arnold 7.4.3.0"),
            ('7.4.2.0', "7.4.2.0", "Arnold 7.4.2.0"),
        ]
    )

classes = [ArnoldSceneProperties]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.arnold = PointerProperty(type=ArnoldSceneProperties)

def unregister():
    del bpy.types.Scene.arnold

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)