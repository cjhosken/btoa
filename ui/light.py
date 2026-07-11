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
        arnold = light.arnold

        layout.use_property_split = True

        if not arnold.dome_light:
            layout.prop(light, "type", expand=True)

        layout.prop(arnold, "dome_light")
        layout.prop(light, "color")

        row = layout.row(align=True)
        row.prop(light, "use_temperature", text="")
        sub = row.row()
        sub.active = light.use_temperature
        sub.prop(light, "temperature", text="Temperature")

        layout.prop(light, "energy")
        layout.prop(light, "exposure")
        layout.prop(light, "normalize")

        if arnold.dome_light:
            pass
        elif light.type == 'POINT':
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

        light = context.light
        arnold = light.arnold

        layout.prop(arnold, "samples")
        layout.prop(arnold, "sampling_mode")
        layout.prop(arnold, "volume_samples")

        layout.separator()

        if arnold.dome_light:
            layout.prop(arnold, "resolution")
        elif light.type in {'POINT', 'SPOT', 'SUN'}:
            layout.prop(arnold, "spread")
        elif light.type == 'AREA':
            layout.prop(arnold, "roundness")
            layout.prop(arnold, "spread")
            layout.prop(arnold, "soft_edge")
            layout.prop(arnold, "aspect_ratio")
            layout.prop(arnold, "lens_radius")

        layout.separator()

        layout.prop(arnold, "shadow_density")
        layout.prop(arnold, "cast_volumetric_shadows")

        layout.separator()

        layout.prop(arnold, "camera_contribution")
        layout.prop(arnold, "diffuse_contribution")
        layout.prop(arnold, "specular_contribution")
        layout.prop(arnold, "transmission_contribution")
        layout.prop(arnold, "subsurface_contribution")
        layout.prop(arnold, "volume_contribution")
        layout.prop(arnold, "indirect_contribution")
        layout.prop(arnold, "max_bounces")

        layout.separator()

        layout.prop(arnold, "aov_light_group")


def register():
    bpy.utils.register_class(ARNOLD_HYDRA_LIGHT_PT_light)
    bpy.utils.register_class(ARNOLD_HYDRA_LIGHT_PT_arnold)


def unregister():
    bpy.utils.unregister_class(ARNOLD_HYDRA_LIGHT_PT_arnold)
    bpy.utils.unregister_class(ARNOLD_HYDRA_LIGHT_PT_light)
