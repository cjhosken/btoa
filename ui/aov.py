import bpy
from ..engine import ArnoldHydraRenderEngine

class ARNOLD_UL_custom_render_vars(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.label(text="", icon='RENDER_STILL')
        row.prop(item, "name", text="", emboss=False)


class ARNOLD_OT_custom_render_var_add(bpy.types.Operator):
    bl_idname = "arnold.custom_render_var_add"
    bl_label = "Add Custom Render Var"

    def execute(self, context):
        r = getattr(context.scene.arnold, "global")
        item = r.custom_render_vars.add()
        item.name = f"custom_pass_{len(r.custom_render_vars)}"
        r.custom_active_index = len(r.custom_render_vars) - 1
        context.scene.update_tag()
        return {'FINISHED'}


class ARNOLD_OT_custom_render_var_remove(bpy.types.Operator):
    bl_idname = "arnold.custom_render_var_remove"
    bl_label = "Remove Custom Render Var"

    def execute(self, context):
        r = getattr(context.scene.arnold, "global")
        if len(r.custom_render_vars) > 0:
            r.custom_render_vars.remove(r.custom_active_index)
            r.custom_active_index = min(r.custom_active_index, len(r.custom_render_vars) - 1)
            context.scene.update_tag()
        return {'FINISHED'}


def draw_aov_row(layout, r, name, label):
    split = layout.split(factor=0.4, align=True)
    split.prop(r, f"aov_{name}_enabled", text=label)
    
    row = split.row(align=True)
    row.enabled = getattr(r, f"aov_{name}_enabled", False)
    
    filter_prop = f"aov_{name}_filter"
    row.prop(r, filter_prop, text="")
    row.prop(r, f"aov_{name}_format", text="")
    
    # Check if selected filter supports width control
    selected_filter = getattr(r, filter_prop, "")
    filters_with_width = {
        "box_filter", "gaussian_filter", "blackman_harris_filter",
        "mitnet_filter", "triangle_filter", "catrom_filter", "disk_filter"
    }
    
    if selected_filter in filters_with_width:
        row.prop(r, f"aov_{name}_filter_width", text="Width")


class ARNOLD_HYDRA_RENDER_PT_aovs(bpy.types.Panel):
    bl_label = "AOVs"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'view_layer'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        r = getattr(context.scene.arnold, "global")
        if not r:
            return

        layout.prop(r, "output_variable_aovs")


class ARNOLD_HYDRA_RENDER_PT_aovs_render_vars(bpy.types.Panel):
    bl_label = "Render Vars"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_aovs"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'view_layer'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        pass


class ARNOLD_HYDRA_RENDER_PT_aovs_standard(bpy.types.Panel):
    bl_label = "Standard"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_aovs_render_vars"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'view_layer'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        r = getattr(context.scene.arnold, "global")
        if not r:
            return

        col = layout.column(align=True)
        draw_aov_row(col, r, "RGBA", "RGBA")
        draw_aov_row(col, r, "A", "A")
        col.separator()
        draw_aov_row(col, r, "P", "P")
        draw_aov_row(col, r, "Pref", "Pref")
        col.separator()
        draw_aov_row(col, r, "N", "N")
        draw_aov_row(col, r, "N_Denoise", "N (Denoise)")
        col.separator()
        draw_aov_row(col, r, "Opacity", "Opacity")
        col.separator()
        draw_aov_row(col, r, "Z", "Z")
        draw_aov_row(col, r, "Z_Back", "Z (Back)")


class ARNOLD_HYDRA_RENDER_PT_aovs_lighting(bpy.types.Panel):
    bl_label = "Lighting"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_aovs_render_vars"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'view_layer'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        r = getattr(context.scene.arnold, "global")
        if not r:
            return

        col = layout.column(align=True)
        draw_aov_row(col, r, "Direct", "Direct")
        draw_aov_row(col, r, "Indirect", "Indirect")
        draw_aov_row(col, r, "Emission", "Emission")
        draw_aov_row(col, r, "Background", "Background")
        draw_aov_row(col, r, "Albedo", "Albedo")
        draw_aov_row(col, r, "Denoise_Albedo", "Denoise Albedo")
        draw_aov_row(col, r, "Shadow_Matte", "Shadow Matte")
        
        # Grouped passes: specular, sss, transmission, diffuse, coat, sheen
        for pass_group in ["Specular", "SSS", "Transmission", "Diffuse", "Coat", "Sheen"]:
            col.separator()
            draw_aov_row(col, r, pass_group, pass_group)
            draw_aov_row(col, r, f"{pass_group}_Direct", f"{pass_group} Direct")
            draw_aov_row(col, r, f"{pass_group}_Indirect", f"{pass_group} Indirect")
            draw_aov_row(col, r, f"{pass_group}_Albedo", f"{pass_group} Albedo")


class ARNOLD_HYDRA_RENDER_PT_aovs_volume(bpy.types.Panel):
    bl_label = "Volume"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_aovs_render_vars"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'view_layer'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        r = getattr(context.scene.arnold, "global")
        if not r:
            return

        col = layout.column(align=True)
        draw_aov_row(col, r, "Volume", "Volume")
        col.separator()
        draw_aov_row(col, r, "Volume_Z", "Volume Z")
        draw_aov_row(col, r, "Volume_Albedo", "Volume Albedo")
        draw_aov_row(col, r, "Volume_Direct", "Volume Direct")
        draw_aov_row(col, r, "Volume_Indirect", "Volume Indirect")
        draw_aov_row(col, r, "Volume_Opacity", "Volume Opacity")


class ARNOLD_HYDRA_RENDER_PT_aovs_utility(bpy.types.Panel):
    bl_label = "Utility"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_aovs_render_vars"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'view_layer'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        r = getattr(context.scene.arnold, "global")
        if not r:
            return

        col = layout.column(align=True)
        draw_aov_row(col, r, "ID", "ID")
        col.separator()
        draw_aov_row(col, r, "Object", "Object")
        col.separator()
        draw_aov_row(col, r, "Shader", "Shader")
        col.separator()
        draw_aov_row(col, r, "Motion_Vector", "Motion Vector")


class ARNOLD_HYDRA_RENDER_PT_aovs_diagnostic(bpy.types.Panel):
    bl_label = "Diagnostic"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_aovs_render_vars"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'view_layer'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        r = getattr(context.scene.arnold, "global")
        if not r:
            return

        col = layout.column(align=True)
        draw_aov_row(col, r, "CPU_Time", "CPU Time")
        draw_aov_row(col, r, "Ray_Count", "Ray Count")
        draw_aov_row(col, r, "AA_Inv_Density", "AA Inv Density")


class ARNOLD_HYDRA_RENDER_PT_aovs_extra(bpy.types.Panel):
    bl_label = "Extra Render Vars"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_aovs"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'view_layer'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        r = getattr(context.scene.arnold, "global")
        if not r:
            return

        row = layout.row()
        col = row.column()
        col.template_list("ARNOLD_UL_custom_render_vars", "", r, "custom_render_vars", r, "custom_active_index")

        col_ops = row.column(align=True)
        col_ops.operator("arnold.custom_render_var_add", icon='ADD', text="")
        col_ops.operator("arnold.custom_render_var_remove", icon='REMOVE', text="")

        if len(r.custom_render_vars) > 0 and r.custom_active_index < len(r.custom_render_vars):
            item = r.custom_render_vars[r.custom_active_index]
            box = layout.box()
            box.label(text="Render Var Settings")
            col_settings = box.column(align=True)
            col_settings.prop(item, "name")
            col_settings.prop(item, "format")
            col_settings.prop(item, "data_type")
            col_settings.prop(item, "source_name")
            col_settings.prop(item, "source_type")
            col_settings.prop(item, "filter")


class ARNOLD_VIEW3D_PT_shading_render_pass(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = "Render Pass"
    bl_parent_id = "VIEW3D_PT_shading"
    COMPAT_ENGINES = {'ARNOLD'}

    @classmethod
    def poll(cls, context):
        return (
            context.space_data.shading.type == 'RENDERED' and
            context.engine == 'ARNOLD' and
            hasattr(context.space_data.shading, 'arnold')
        )

    def draw(self, context):
        shading = context.space_data.shading
        layout = self.layout
        layout.prop(shading.arnold, "viewport_aov", text="")


register_classes, unregister_classes = bpy.utils.register_classes_factory((
    ARNOLD_UL_custom_render_vars,
    ARNOLD_OT_custom_render_var_add,
    ARNOLD_OT_custom_render_var_remove,
    ARNOLD_HYDRA_RENDER_PT_aovs,
    ARNOLD_HYDRA_RENDER_PT_aovs_render_vars,
    ARNOLD_HYDRA_RENDER_PT_aovs_standard,
    ARNOLD_HYDRA_RENDER_PT_aovs_lighting,
    ARNOLD_HYDRA_RENDER_PT_aovs_volume,
    ARNOLD_HYDRA_RENDER_PT_aovs_utility,
    ARNOLD_HYDRA_RENDER_PT_aovs_diagnostic,
    ARNOLD_HYDRA_RENDER_PT_aovs_extra,
    ARNOLD_VIEW3D_PT_shading_render_pass
))


def register():
    register_classes()


def unregister():
    unregister_classes()