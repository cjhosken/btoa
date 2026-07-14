from . import light, shape, camera, render, aov, menu


def register():
    light.register()
    shape.register()
    camera.register()
    render.register()
    aov.register()
    menu.register()


def unregister():
    menu.unregister()
    aov.unregister()
    render.unregister()
    camera.unregister()
    shape.unregister()
    light.unregister()
