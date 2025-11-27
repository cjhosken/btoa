import bpy
import subprocess
import os

class ARNOLD_OT_install(bpy.types.Operator):
    bl_idname = "arnold.install"
    bl_label = "Install Arnold"
    bl_description = "Runs the Arnold build script"

    def execute(self, context):
        arnold = context.scene.arnold
        blender_version = bpy.app.version_string.rsplit('.', 1)[0]  # e.g., "5.0"

        # Path to the folder where your addon lives
        addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Path to your build.sh inside the addon
        script_path = os.path.join(addon_dir, "build.sh")

        if not os.path.exists(script_path):
            self.report({'ERROR'}, f"build.sh not found: {script_path}")
            return {'CANCELLED'}

        try:
            # Run the script
            subprocess.run(
                ["bash", script_path, blender_version, arnold.version],
                check=True
            )
            self.report({'INFO'}, "Arnold installation started…")
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