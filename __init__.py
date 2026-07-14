bl_info = {
    "name": "Hydra Arnold Render Engine",
    "author": "Christopher Hosken",
    "version": (7, 5, 4, 1),
    "blender": (5, 2, 0),
    "description": "Arnold path tracing renderer using the Hydra render delegate",
    "category": "Render",
    "support": "OFFICIAL",
}


from . import engine, ui, operators, props, preferences


def register():
    operators.register()
    engine.register()
    props.register()
    preferences.register()
    ui.register()


def unregister():
    ui.unregister()
    preferences.unregister()
    props.unregister()
    engine.unregister()
    operators.unregister()