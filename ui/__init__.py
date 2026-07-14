from . import light, shape, camera, render, aov


def register():
    light.register()
    shape.register()
    camera.register()
    render.register()
    aov.register()


def unregister():
    aov.unregister()
    render.unregister()
    camera.unregister()
    shape.unregister()
    light.unregister()
