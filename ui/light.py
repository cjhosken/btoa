import bpy

from ..engine import ArnoldHydraRenderEngine

class Panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.light

class ARNOLD_HYDRA_LIGHT_PT_light(Panel):
    bl_label = "Light"

    def draw(self, context):
        layout = self.layout
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


class ARNOLD_HYDRA_LIGHT_PT_arnold(bpy.types.Panel):
    bl_label = "Arnold"
    bl_parent_id = "ARNOLD_HYDRA_LIGHT_PT_light"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return (context.engine in cls.COMPAT_ENGINES and
                context.light and
                hasattr(context.light, 'arnold'))

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

class ARNOLD_HYDRA_LIGHT_PT_arnold_light(bpy.types.Panel):
    bl_label = "Light"
    bl_parent_id = "ARNOLD_HYDRA_LIGHT_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return (context.engine in cls.COMPAT_ENGINES and
                context.light and
                hasattr(context.light, 'arnold'))

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.light.arnold

        layout.prop(arnold, "samples")
        layout.prop(arnold, "sampling_mode")
        layout.prop(arnold, "volume_samples")
        layout.prop(arnold, "roundness")
        layout.prop(arnold, "angle")
        layout.prop(arnold, "spread")
        layout.prop(arnold, "soft_edge")
        layout.prop(arnold, "portal")
        layout.prop(arnold, "portal_mode")
        layout.prop(arnold, "resolution")
        layout.prop(arnold, "aspect_ratio")
        layout.prop(arnold, "lens_radius")
        #layout.prop(arnold, "aov_indirect")

class ARNOLD_HYDRA_LIGHT_PT_shadows(bpy.types.Panel):
    bl_label = "Shadows"
    bl_parent_id = "ARNOLD_HYDRA_LIGHT_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return (context.engine in cls.COMPAT_ENGINES and
                context.light and
                hasattr(context.light, 'arnold'))

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.light.arnold

        layout.prop(arnold, "shadow_color")
        layout.prop(arnold, "shadow_density")
        layout.prop(arnold, "cast_shadows")
        layout.prop(arnold, "cast_volumetric_shadows")


class ARNOLD_HYDRA_LIGHT_PT_contribution(bpy.types.Panel):
    bl_label = "Contribution"
    bl_parent_id = "ARNOLD_HYDRA_LIGHT_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return (context.engine in cls.COMPAT_ENGINES and
                context.light and
                hasattr(context.light, 'arnold'))

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.light.arnold

        layout.prop(arnold, "camera")
        layout.prop(arnold, "diffuse")
        layout.prop(arnold, "specular")
        layout.prop(arnold, "transmission")
        layout.prop(arnold, "sss")
        layout.prop(arnold, "volume")
        layout.prop(arnold, "indirect")
        layout.prop(arnold, "max_bounces")
        #layout.prop(arnold, "aov_light_group")
        #layout.prop(arnold, "shaders")

register_classes, unregister_classes = bpy.utils.register_classes_factory((
    ARNOLD_HYDRA_LIGHT_PT_light,
    ARNOLD_HYDRA_LIGHT_PT_arnold,
    ARNOLD_HYDRA_LIGHT_PT_arnold_light,
    ARNOLD_HYDRA_LIGHT_PT_shadows,
    ARNOLD_HYDRA_LIGHT_PT_contribution,
))

def register():
    register_classes()

def unregister():
    unregister_classes()