import bpy

from . import io, install

def register():
    install.register()
    io.register()

def unregister():
    io.unregister()
    install.unregister()