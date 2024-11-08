import bpy, os
from bpy.props import *

class ArnoldSceneProperties(bpy.types.PropertyGroup):

    arnoldUSDPath: StringProperty(
        name="Arnold Renderer Plugin Path",
        description="Path to the ArnoldUSD Hydra Delegate Plugin",
        subtype="FILE_PATH",
        default=os.path.join(os.path.expanduser("~"), ".btoa", "arnoldusd")
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