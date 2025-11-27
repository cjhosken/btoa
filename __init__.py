import bpy, os, sys

bl_info = {
    "name" : "Blender to Arnold",
    "author" : "Christopher Hosken",
    "version" : (7, 4, 3, 0),
    "blender" : (5, 0, 0),
    "description" : "Autodesk's Arnold Renderer integration into Blender",
    "warning" : "This Addon is currently under development",
    "tracker_url":"",
    "doc_url":"",
    "community":"",
    "downloads":"",
    "main_web":"",
    "support": "COMMUNITY",
    "category" : "Render"
}

from . import properties, engine, preferences, operators, ui


def register():
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