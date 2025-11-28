import bpy
import subprocess
import os
import urllib.request
from pathlib import Path
import zipfile

class ARNOLD_OT_install(bpy.types.Operator):
    bl_idname = "arnold.install"
    bl_label = "Install Arnold"
    bl_description = "Runs the Arnold build script"

    def execute(self, context):
        arnold = context.scene.arnold
        blender_version = bpy.app.version_string.rsplit('.', 1)[0]  # e.g., "5.0"

        # Path to the folder where your addon lives
        addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        try:
            self.report({'INFO'}, "Arnold installation started…")

            # Download a file from github and extract it into ~/.arnold/install/arnoldusd
            btoa = Path.home() / ".btoa"
            install_path = btoa / f"btoa-{blender_version}-{arnold.version}"
            zip_path = btoa / f"btoa-{blender_version}-{arnold.version}.zip"

            url = f"https://github.com/cjhosken/btoa/releases/download/btoa/btoa-{blender_version}-{arnold.version}-linux.zip"

            if not os.path.isdir(btoa):
                os.mkdir(btoa)

            urllib.request.urlretrieve(url, zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for member in zip_ref.infolist():
                    # Skip top-level folder
                    parts = Path(member.filename).parts
                    if len(parts) <= 1:
                        # skip the folder itself
                        continue
                    # Rebuild path without the first component
                    target_path = install_path.joinpath(*parts[1:])
                    if member.is_dir():
                        target_path.mkdir(parents=True, exist_ok=True)
                    else:
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        with zip_ref.open(member) as source, open(target_path, "wb") as target:
                            target.write(source.read())
            
            os.remove(zip_path)

            with open(os.path.join(addon_dir, "arnold_env.py"), "r") as f:
                content = f.read()
                content = content.replace("__BLENDER_VERSION__", blender_version)
                content = content.replace("__ARNOLD_VERSION__", arnold.version)
            
            with open(os.path.join(bpy.utils.user_resource('SCRIPTS'), "startup", "arnold_env.py"), "w") as f:
                f.write(content)

        except subprocess.CalledProcessError as e:
            self.report({'ERROR'}, f"Build script failed: {e}")
            return {'CANCELLED'}
        
        self.report({'INFO'}, "Arnold installation completed! Please restart Blender.")

        return {'FINISHED'}

classes = [ARNOLD_OT_install]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)