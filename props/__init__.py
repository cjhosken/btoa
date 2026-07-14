from . import light, shape, camera, aov, render


def register():
    light.register()
    shape.register()
    camera.register()
    aov.register()
    render.register()


def unregister():
    render.unregister()
    aov.unregister()
    camera.unregister()
    shape.unregister()
    light.unregister()
