from . import light, shape, camera, render


def register():
    light.register()
    shape.register()
    camera.register()
    render.register()


def unregister():
    render.unregister()
    camera.unregister()
    shape.unregister()
    light.unregister()
