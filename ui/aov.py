import bpy
from ..engine import ArnoldHydraRenderEngine
from ..props.aov import BUILTIN_AOVS


class ArnoldAOVPanel(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "view_layer"
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw_aovs(self, context, category):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        settings = getattr(context.scene.arnold, "global")

        for name, label, *_ in BUILTIN_AOVS.get(category, []):
            enabled = f"aov_{name}_enabled"
            filter_type = f"aov_{name}_filter_type"
            format_type = f"aov_{name}_format"

            row = layout.row(align=True)

            row.prop(settings, enabled, text=label)

            sub = row.row(align=True)
            sub.enabled = getattr(settings, enabled)
            sub.prop(settings, filter_type, text="")
            sub.prop(settings, format_type, text="")

    def draw(self, context):
        pass


class ARNOLD_HYDRA_RENDER_PT_aovs(ArnoldAOVPanel):
    bl_label = "Render Vars"


class ARNOLD_HYDRA_RENDER_PT_aovs_standard(ArnoldAOVPanel):
    bl_label = "Standard"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_aovs"

    def draw(self, context):
        self.draw_aovs(context, "Standard")


class ARNOLD_HYDRA_RENDER_PT_aovs_standard_lighting(ArnoldAOVPanel):
    bl_label = "Lighting"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_aovs_standard"

    def draw(self, context):
        self.draw_aovs(context, "Lighting")


class ARNOLD_HYDRA_RENDER_PT_aovs_volume(ArnoldAOVPanel):
    bl_label = "Volume"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_aovs"

    def draw(self, context):
        self.draw_aovs(context, "Volume")


class ARNOLD_HYDRA_RENDER_PT_aovs_utility(ArnoldAOVPanel):
    bl_label = "Utility"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_aovs"

    def draw(self, context):
        self.draw_aovs(context, "Utility")


class ARNOLD_HYDRA_RENDER_PT_aovs_diagnostic(ArnoldAOVPanel):
    bl_label = "Diagnostic"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_aovs"

    def draw(self, context):
        self.draw_aovs(context, "Diagnostic")


register, unregister = bpy.utils.register_classes_factory((
    ARNOLD_HYDRA_RENDER_PT_aovs,
    ARNOLD_HYDRA_RENDER_PT_aovs_standard,
    ARNOLD_HYDRA_RENDER_PT_aovs_standard_lighting,
    ARNOLD_HYDRA_RENDER_PT_aovs_volume,
    ARNOLD_HYDRA_RENDER_PT_aovs_utility,
    ARNOLD_HYDRA_RENDER_PT_aovs_diagnostic,
))