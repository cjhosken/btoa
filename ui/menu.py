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


class ARNOLD_MT_licensing_menu(bpy.types.Menu):
    bl_label = "Licensing"
    bl_idname = "ARNOLD_MT_licensing_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("arnold.open_license_manager", text="License Manager", icon='PREFERENCES')
        
        op = layout.operator("wm.url_open", text="Licensing Help", icon='HELP')
        op.url = "https://help.autodesk.com/view/ARNOL/ENU/?guid=arnold_user_guide_licensing_html"
        
        op = layout.operator("wm.url_open", text="Purchase Subscription", icon='WORLD')
        op.url = "https://www.autodesk.com/products/arnold/overview"


class ARNOLD_MT_help_menu(bpy.types.Menu):
    bl_label = "Help"
    bl_idname = "ARNOLD_MT_help_menu"

    def draw(self, context):
        layout = self.layout
        op = layout.operator("wm.url_open", text="Autodesk Analytics", icon='WORLD')
        op.url = "https://www.autodesk.com/company/autodesk-analytics"
        
        layout.operator("arnold.diagnostics_dialog", text="Diagnostics", icon='CONSOLE')
        
        op = layout.operator("wm.url_open", text="Legal Notice", icon='FILE_TEXT')
        op.url = "https://www.autodesk.com/company/legal-notices-trademarks"
        
        layout.operator("arnold.about", text="About BtoA", icon='INFO')


class ARNOLD_MT_main_menu(bpy.types.Menu):
    bl_label = "Arnold"
    bl_idname = "ARNOLD_MT_main_menu"

    def draw(self, context):
        layout = self.layout
        
        op = layout.operator("wm.url_open", text="User Guide", icon='HELP')
        op.url = "https://help.autodesk.com/view/ARNOL/ENU/"
        
        op = layout.operator("wm.url_open", text="Tutorials", icon='PLAY')
        op.url = "https://help.autodesk.com/view/ARNOL/ENU/?guid=arnold_for_maya_tutorials_html"
        
        op = layout.operator("wm.url_open", text="Developer Guide", icon='FILE_TEXT')
        op.url = "https://help.autodesk.com/view/ARNOL/ENU/?guid=arnold_dev_guide_html"
        
        op = layout.operator("wm.url_open", text="Arnold Product Page", icon='WORLD')
        op.url = "https://www.autodesk.com/products/arnold"
        
        op = layout.operator("wm.url_open", text="Arnold Community", icon='WORLD')
        op.url = "https://community.autodesk.com/t5/arnold/ct-p/arnold"
        
        op = layout.operator("wm.url_open", text="Support Blog", icon='FILE_TEXT')
        op.url = "https://arnoldsupport.com/"
        
        layout.separator()
        layout.menu("ARNOLD_MT_licensing_menu")
        layout.menu("ARNOLD_MT_help_menu")


def draw_menu(self, context):
    self.layout.menu("ARNOLD_MT_main_menu")


register_classes, unregister_classes = bpy.utils.register_classes_factory((
    ARNOLD_OT_open_license_manager,
    ARNOLD_OT_about,
    ARNOLD_OT_diagnostics_dialog,
    ARNOLD_MT_licensing_menu,
    ARNOLD_MT_help_menu,
    ARNOLD_MT_main_menu
))


def register():
    register_classes()
    bpy.types.TOPBAR_MT_editor_menus.append(draw_menu)


def unregister():
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_menu)
    unregister_classes()
