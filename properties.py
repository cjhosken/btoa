import bpy
from bpy.props import *

class ArnoldSceneProperties(bpy.types.PropertyGroup):
    pass



classes = [ArnoldSceneProperties]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.arnold = PointerProperty(type=ArnoldSceneProperties)

def unregister():
    del bpy.types.Scene.arnold

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)