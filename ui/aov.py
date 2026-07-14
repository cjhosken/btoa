import bpy
from ..engine import ArnoldHydraRenderEngine
from ..props.aov import BUILTIN_AOVS


class ARNOLD_HYDRA_RENDER_PT_aovs(bpy.types.Panel):
    bl_label = "Render Vars"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "view_layer"
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        settings = getattr(context.scene.arnold, "global")

        for aovs in BUILTIN_AOVS.values():
            for name, label, *_ in aovs:
                prefix = f"aov_{name}"

                enabled_prop = f"{prefix}_enabled"
                filter_prop = f"{prefix}_filter_type"
                format_prop = f"{prefix}_format"

                row = layout.row(align=True)
                row.prop(settings, enabled_prop, text=label)

                sub = row.row(align=True)
                sub.enabled = getattr(settings, enabled_prop)
                sub.prop(settings, filter_prop, text="")
                sub.prop(settings, format_prop, text="")


class ARNOLD_VIEW3D_PT_shading_render_pass(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "HEADER"
    bl_label = "Render Pass"
    bl_parent_id = "VIEW3D_PT_shading"
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        shading = context.space_data.shading
        return (
            context.engine in cls.COMPAT_ENGINES
            and shading.type == "RENDERED"
            and hasattr(shading, "arnold")
        )

    def draw(self, context):
        shading = context.space_data.shading
        layout = self.layout
        layout.prop(shading.arnold, "viewport_aov", text="")


register, unregister = bpy.utils.register_classes_factory((
    ARNOLD_HYDRA_RENDER_PT_aovs,
    ARNOLD_VIEW3D_PT_shading_render_pass
))
