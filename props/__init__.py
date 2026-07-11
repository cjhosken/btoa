from . import light, geom, camera, render


def register():
    light.register()
    geom.register()
    camera.register()
    render.register()


def unregister():
    render.unregister()
    camera.unregister()
    geom.unregister()
    light.unregister()
