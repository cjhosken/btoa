import bpy, os

bl_info = {
    "name" : "Blender to Arnold",
    "author" : "Christopher Hosken",
    "version" : (7, 3, 4, 1),
    "blender" : (4, 1, 1),
    "description" : "Autodesk's Arnold Renderer integration into Blender",
    "warning" : "This Addon is currently under development",
    "support": "COMMUNITY",
    "category" : "Render"
}

from . import properties, engine, preferences, operators, ui

def register():
    os.environ["LD_LIBRARY_PATH"] = os.environ.get("LD_LIBRARY_PATH", "") + ":" + os.path.join(os.path.expanduser("~"), ".btoa", "deps", "lib")

    properties.register()
    preferences.register()
    engine.register()
    operators.register()
    ui.register()

def unregister():
    ui.unregister()
    operators.unregister()
    engine.unregister()
    preferences.unregister()
    properties.unregister()