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
    from ..props.aov import FILTERS_WITH_WIDTH

    split = layout.split(factor=0.4, align=True)
    split.prop(r, f"aov_{name}_enabled", text=label)
    
    row = split.row(align=True)
    enabled = getattr(r, f"aov_{name}_enabled", False)
    row.enabled = enabled
    
    ftype_prop = f"aov_{name}_filter_type"
    row.prop(r, ftype_prop, text="")
    row.prop(r, f"aov_{name}_format", text="")
    
    # Check if selected filter supports extra controls
    ftype = getattr(r, ftype_prop, "box_filter")
    has_extras = (ftype in FILTERS_WITH_WIDTH or
                  ftype in {"diff_filter", "variance_filter", "cryptomatte_filter"})
    
    if enabled and has_extras:
        box = layout.box()
        box.use_property_split = True
        box.use_property_decorate = False
        
        p = f"aov_{name}_filter"
        if ftype in FILTERS_WITH_WIDTH:
            box.prop(r, f"{p}_width", text="Width")
        if ftype == "diff_filter":
            box.prop(r, f"{p}_weights", text="Weights")
        elif ftype == "variance_filter":
            box.prop(r, f"{p}_weights", text="Weights")
            box.prop(r, f"{p}_scalar_mode")
        elif ftype == "cryptomatte_filter":
            box.prop(r, f"{p}_sub_filter", text="Sub-Filter")
            box.prop(r, f"{p}_noop")
            box.prop(r, f"{p}_source_filter")


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


class ARNOLD_HYDRA_RENDER_PT_aovs_builtin(bpy.types.Panel):
    bl_label = "Built-in Passes"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'view_layer'
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_aovs"
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        from ..props.aov import BUILTIN_AOVS, FILTERS_WITH_WIDTH

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        r = getattr(context.scene.arnold, "global")
        if not r:
            return

        for cat, aovs in BUILTIN_AOVS.items():
            box = layout.box()
            box.label(text=cat)
            for name, label, def_filt, def_fmt in aovs:
                p           = f"aov_{name}"
                enabled_prop = f"{p}_enabled"
                ftype_prop   = f"{p}_filter_type"
                format_prop  = f"{p}_format"

                row = box.row(align=True)
                row.prop(r, enabled_prop, text=label)

                enabled = getattr(r, enabled_prop, False)
                sub = row.row(align=True)
                sub.enabled = enabled
                sub.prop(r, ftype_prop, text="")
                sub.prop(r, format_prop, text="")

                # Show filter width only when enabled and filter has width
                ftype = getattr(r, ftype_prop, "box_filter")
                if enabled and ftype in FILTERS_WITH_WIDTH:
                    sub_box = box.box()
                    p_filt = f"aov_{name}_filter"
                    sub_box.prop(r, f"{p_filt}_width", text="Width")


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
            col_settings.use_property_split = True
            col_settings.use_property_decorate = False
            col_settings.prop(item, "name")
            col_settings.prop(item, "format")
            col_settings.prop(item, "data_type")
            col_settings.prop(item, "source_name")
            col_settings.prop(item, "source_type")
            
            if item.filter:
                filt = item.filter
                col_settings.prop(filt, "type", text="Filter")
                
                from ..props.aov import FILTERS_WITH_WIDTH
                if filt.type in FILTERS_WITH_WIDTH:
                    col_settings.prop(filt, "width")


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
    ARNOLD_HYDRA_RENDER_PT_aovs_builtin,
    ARNOLD_HYDRA_RENDER_PT_aovs_extra,
    ARNOLD_VIEW3D_PT_shading_render_pass
))


def register():
    register_classes()


def unregister():
    unregister_classes()