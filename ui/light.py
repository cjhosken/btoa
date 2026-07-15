import bpy

from ..engine import ArnoldHydraRenderEngine

class ArnoldLightPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.light
    
    def setup(self, context):
        layout = self.layout
        layout.use_property_split = True
        settings = context.light.arnold
        return layout, settings

class ARNOLD_HYDRA_LIGHT_PT_light(ArnoldLightPanel):
    bl_label = "Light"

    def draw(self, context):
        layout, _ = self.setup(context)
        light = context.light

        layout.use_property_split = True
        layout.prop(light, "type", expand=True)
        layout.prop(light, "color")

        row = layout.row(align=True)
        row.prop(light, "use_temperature", text="")
        sub = row.row()
        sub.active = light.use_temperature
        sub.prop(light, "temperature", text="Temperature")

        layout.prop(light, "energy")
        layout.prop(light, "exposure")
        layout.prop(light, "normalize")

        if light.type == 'POINT':
            layout.prop(light, "shadow_soft_size", text="Radius")
        elif light.type == 'SUN':
            layout.prop(light, "angle")
        elif light.type == 'SPOT':
            layout.prop(light, 'spot_size', text="Angle", slider=True)
            layout.prop(light, 'spot_blend', slider=True)
            layout.prop(light, 'show_cone')
        elif light.type == 'AREA':
            layout.prop(light, "shape", text="Shape")
            if light.shape in {'SQUARE', 'DISK'}:
                layout.prop(light, "size")
            elif light.shape in {'RECTANGLE', 'ELLIPSE'}:
                layout.prop(light, "size", text="Size X")
                layout.prop(light, "size_y", text="Y")


class ARNOLD_HYDRA_LIGHT_PT_arnold(ArnoldLightPanel):
    bl_label = "Arnold"
    bl_parent_id = "ARNOLD_HYDRA_LIGHT_PT_light"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        pass

class ARNOLD_HYDRA_LIGHT_PT_arnold_light(ArnoldLightPanel):
    bl_label = "Light"
    bl_parent_id = "ARNOLD_HYDRA_LIGHT_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "samples")
        layout.prop(settings, "sampling_mode")
        layout.prop(settings, "volume_samples")
        layout.prop(settings, "roundness")
        layout.prop(settings, "angle")
        layout.prop(settings, "spread")
        layout.prop(settings, "soft_edge")
        layout.prop(settings, "portal")
        layout.prop(settings, "portal_mode")
        layout.prop(settings, "resolution")
        layout.prop(settings, "aspect_ratio")
        layout.prop(settings, "lens_radius")
        layout.prop(settings, "aov_indirect")


class ARNOLD_HYDRA_LIGHT_PT_shadows(ArnoldLightPanel):
    bl_label = "Shadows"
    bl_parent_id = "ARNOLD_HYDRA_LIGHT_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "shadow_color")
        layout.prop(settings, "shadow_density")
        layout.prop(settings, "cast_shadows")
        layout.prop(settings, "cast_volumetric_shadows")


class ARNOLD_HYDRA_LIGHT_PT_contribution(ArnoldLightPanel):
    bl_label = "Contribution"
    bl_parent_id = "ARNOLD_HYDRA_LIGHT_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "camera")
        layout.prop(settings, "diffuse")
        layout.prop(settings, "specular")
        layout.prop(settings, "transmission")
        layout.prop(settings, "sss")
        layout.prop(settings, "volume")
        layout.prop(settings, "indirect")
        layout.prop(settings, "max_bounces")
        layout.prop(settings, "aov_light_group")

class ARNOLD_HYDRA_LIGHT_PT_shaders(ArnoldLightPanel):
    bl_label = "Shaders"
    bl_parent_id = "ARNOLD_HYDRA_LIGHT_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "shaders")


register, unregister = bpy.utils.register_classes_factory((
    ARNOLD_HYDRA_LIGHT_PT_light,
    ARNOLD_HYDRA_LIGHT_PT_arnold,
    ARNOLD_HYDRA_LIGHT_PT_arnold_light,
    ARNOLD_HYDRA_LIGHT_PT_shadows,
    ARNOLD_HYDRA_LIGHT_PT_contribution,
    ARNOLD_HYDRA_LIGHT_PT_shaders,
))
