import os
from pathlib import Path
import sys

BLENDER_VERSION = "__BLENDER_VERSION__"
ARNOLD_VERSION = "__ARNOLD_VERSION__"

if BLENDER_VERSION.startswith("__"):
    import bpy
    BLENDER_VERSION = f"{bpy.app.version[0]}.{bpy.app.version[1]}"
if ARNOLD_VERSION.startswith("__"):
    ARNOLD_VERSION = "7.4.4.0"

def register():
    delegate_root = os.path.join(
        os.path.expanduser("~"),
        ".btoa",
        f"btoa-{BLENDER_VERSION}-{ARNOLD_VERSION}"
    )

    os.environ["BTOA_ROOT"] = delegate_root
    os.environ["OCIO"] = os.path.join(delegate_root, "ocio", "configs", "arnold", "config.ocio")

    plugin_dir = os.path.join(delegate_root, "plugin")

    os.environ["ARNOLD_PLUGIN_PATH"] = (
        os.path.join(delegate_root, "plugin") + os.pathsep +
        os.path.join(delegate_root, "plugins") + os.pathsep +
        os.path.join(delegate_root, "procedural") + os.pathsep +
        os.environ.get("ARNOLD_PLUGIN_PATH", "")
    )

    os.environ["PYTHONPATH"] = (
        os.path.join(delegate_root, "lib", "python") + os.pathsep +
        os.environ.get("PYTHONPATH", "")
    )

    if sys.platform == "win32":
        os.environ["PATH"] = os.path.join(delegate_root, "lib") + os.pathsep + os.environ.get("PATH", "")
        lib_dir = os.path.join(delegate_root, "lib")
        if os.path.exists(lib_dir):
            try:
                os.add_dll_directory(lib_dir)
                print(f"[BtoA] Added DLL directory: {lib_dir}")
            except Exception as e:
                print(f"[BtoA] Failed to add DLL directory: {e}")
    elif sys.platform == "darwin":
        os.environ["DYLD_LIBRARY_PATH"] = os.path.join(delegate_root, "lib") + os.pathsep + os.environ.get("DYLD_LIBRARY_PATH", "")
        import ctypes
        libai_path = os.path.join(delegate_root, "bin", "libai.dylib")
        if os.path.exists(libai_path):
            try:
                ctypes.CDLL(libai_path, ctypes.RTLD_GLOBAL)
                print(f"[BtoA] Successfully pre-loaded: {libai_path}")
            except Exception as e:
                print(f"[BtoA] Failed to pre-load {libai_path}: {e}")
    else:
        os.environ["PATH"] = os.path.join(delegate_root, "bin") + os.pathsep + os.environ.get("PATH", "")
        os.environ["LD_LIBRARY_PATH"] = os.path.join(delegate_root, "bin") + os.pathsep + os.environ.get("LD_LIBRARY_PATH", "")
        import ctypes
        libai_path = os.path.join(delegate_root, "bin", "libai.so")
        if os.path.exists(libai_path):
            try:
                ctypes.CDLL(libai_path, ctypes.RTLD_GLOBAL)
                print(f"[BtoA] Successfully pre-loaded: {libai_path}")
            except Exception as e:
                print(f"[BtoA] Failed to pre-load {libai_path}: {e}")

    print("Arnold environment initialized before Blender startup.")

if __name__ == "__main__":
    register()
