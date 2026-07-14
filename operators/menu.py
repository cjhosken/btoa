import bpy
import os
import subprocess


class ARNOLD_OT_open_license_manager(bpy.types.Operator):
    bl_idname = "arnold.open_license_manager"
    bl_label = "Open License Manager"
    bl_description = "Open the Autodesk Arnold License Manager executable"

    def execute(self, context):
        bin_path = os.path.expanduser("~/.btoa/btoa-5.2-7.4.5.1/bin/ArnoldLicenseManager")
        if os.path.exists(bin_path):
            try:
                subprocess.Popen([bin_path])
                self.report({'INFO'}, "Arnold License Manager opened successfully.")
            except Exception as e:
                self.report({'ERROR'}, f"Failed to start Arnold License Manager: {e}")
        else:
            self.report({'ERROR'}, f"Arnold License Manager executable not found at {bin_path}")
        return {'FINISHED'}


class ARNOLD_OT_about(bpy.types.Operator):
    bl_idname = "arnold.about"
    bl_label = "About BtoA"
    bl_description = "Show information about the Blender to Arnold integration"

    def draw(self, context):
        layout = self.layout
        layout.label(text="BtoA: Blender to Arnold Bridge", icon='INFO')
        layout.label(text="Addon Version: 5.2")
        layout.label(text="Arnold SDK Version: 7.4.5.1")
        layout.label(text="Integration utilizing Autodesk Hydra Render Delegate (HdArnold)")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class ARNOLD_OT_diagnostics_dialog(bpy.types.Operator):
    bl_idname = "arnold.diagnostics_dialog"
    bl_label = "Arnold Diagnostics Info"
    bl_description = "Show current diagnostic files configuration"

    def draw(self, context):
        layout = self.layout
        r = getattr(context.scene.arnold, "global", None)
        if r:
            layout.label(text=f"Log File: {r.log_file if r.log_file else 'None (Stdout Only)'}")
            layout.label(text=f"Stats File: {r.stats_file}")
            layout.label(text=f"Profile File: {r.profile_file}")
        else:
            layout.label(text="Scene render settings not initialized.")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


register, unregister = bpy.utils.register_classes_factory((
    ARNOLD_OT_open_license_manager,
    ARNOLD_OT_about,
    ARNOLD_OT_diagnostics_dialog,
))
