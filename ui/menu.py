import bpy


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
