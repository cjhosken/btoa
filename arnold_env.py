import os
from pathlib import Path
import sys

BLENDER_VERSION = "__BLENDER_VERSION__"
ARNOLD_VERSION = "__ARNOLD_VERSION__"

delegate_root = os.path.join(
    "opt",
    "blender",
    BLENDER_VERSION,
    "arnold",
    ARNOLD_VERSION
)

plugin_dir = os.path.join(delegate_root, "plugin")

os.environ["ARNOLD_PLUGIN_PATH"] = (
    os.path.join(delegate_root, "procedural") + os.pathsep +
    os.environ.get("ARNOLD_PLUGIN_PATH", "")
)

os.environ["PYTHONPATH"] = (
    os.path.join(delegate_root, "lib", "python") + os.pathsep +
    os.environ.get("PYTHONPATH", "")
)

os.environ["PXR_PLUGINPATH_NAME"] = (
    plugin_dir + os.pathsep +
    os.path.join(delegate_root, "lib", "usd") + os.pathsep +
    os.environ.get("PXR_PLUGINPATH_NAME", "")
)

if sys.platform == "win32":
    os.environ["PATH"] = os.path.join(delegate_root, "lib") + os.pathsep + os.environ.get("PATH", "")
elif sys.platform == "darwin":
    os.environ["DYLD_LIBRARY_PATH"] = os.path.join(delegate_root, "lib") + os.pathsep + os.environ.get("DYLD_LIBRARY_PATH", "")
else:
    os.environ["PATH"] = os.path.join(delegate_root, "bin") + os.pathsep + os.environ.get("PATH", "")
    os.environ["LD_LIBRARY_PATH"] = os.path.join(delegate_root, "bin") + os.pathsep + os.environ.get("LD_LIBRARY_PATH", "")

print("Arnold environment initialized before Blender startup.")
