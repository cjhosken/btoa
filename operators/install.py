import bpy
import subprocess
import os
import urllib.request
from pathlib import Path
import tarfile

class ARNOLD_OT_install(bpy.types.Operator):
    bl_idname = "arnold.install"
    bl_label = "Install Arnold"
    bl_description = "Runs the Arnold build script"

    def execute(self, context):
        arnold = context.scene.arnold
        blender_version = bpy.app.version_string.rsplit('.', 1)[0]  # e.g., "5.0"

        # Path to the folder where your addon lives
        addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if not os.path.exists(script_path):
            self.report({'ERROR'}, f"build.sh not found: {script_path}")
            return {'CANCELLED'}

        try:
            self.report({'INFO'}, "Arnold installation started…")

            # Download a file from github and extract it into ~/.arnold/install/arnoldusd
            btoa = Path.home() / ".btoa"
            install_path = btoa / f"Arnold-{arnold.version}"
            tgz_path = btoa / f"Arnold-{arnold.version}.tgz"

            url = f"https://github.com/cjhosken/btoa/releases/download/arnoldsdk/Arnold-{arnold.version}-linux.tgz"

            os.mkdir(btoa, exist_ok=True)
            urllib.request.urlretrieve(url, tgz_path)
            with tarfile.open(tgz_path, "r:gz") as tar:
                tar.extractall(path=install_path)
            
            os.remove(tgz_path)

            os.copy(
                os.path.join(addon_dir, "arnold_env.py"),
                os.path.join(bpy.utils.user_resource('SCRIPTS'), "startup", "arnold_env.py")
            )

            with open(os.path.join(addon_dir, "arnold_env.py"), "r") as f:
                content = f.read()
                content = content.replace("__BLENDER_VERSION__", blender_version)
                content = content.replace("__ARNOLD_VERSION__", arnold.version)
            
            with open(os.path.join(bpy.utils.user_resource('SCRIPTS'), "startup", "arnold_env.py"), "w") as f:
                f.write(content)

        except subprocess.CalledProcessError as e:
            self.report({'ERROR'}, f"Build script failed: {e}")
            return {'CANCELLED'}
        
        self.repot({'INFO'}, "Arnold installation completed! Please restart Blender.")

        return {'FINISHED'}

classes = [ARNOLD_OT_install]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)