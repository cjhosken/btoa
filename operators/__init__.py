from . import build, menu


def register():
    build.register()
    menu.register()


def unregister():
    menu.unregister()
    build.unregister()
