import bpy
from ..engine import ArnoldHydraRenderEngine


class ArnoldShapePanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.object and context.object.type == 'MESH'

    def setup(self, context):
        layout = self.layout
        layout.use_property_split = True
        settings = context.object.arnold
        return layout, settings


class ARNOLD_HYDRA_GEOM_PT_arnold(ArnoldShapePanel):
    bl_label = "Arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        pass


class ARNOLD_HYDRA_GEOM_PT_subdivision(ArnoldShapePanel):
    bl_label = "Subdivision"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "subdiv_type")
        layout.prop(settings, "subdiv_iterations")
        layout.prop(settings, "subdiv_adaptive_metric")
        layout.prop(settings, "subdiv_adaptive_error")
        layout.prop(settings, "subdiv_adaptive_space")
        layout.prop(settings, "subdiv_uv_smoothing")
        layout.prop(settings, "subdiv_smooth_derivs")
        layout.prop(settings, "subdiv_frustum_ignore")


class ARNOLD_HYDRA_GEOM_PT_displacement(ArnoldShapePanel):
    bl_label = "Displacement"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "disp_height")
        layout.prop(settings, "disp_zero_value")
        layout.prop(settings, "disp_padding")
        layout.prop(settings, "disp_autobump")
        
        layout.prop(settings, "autobump_camera")
        layout.prop(settings, "autobump_shadow")
        layout.prop(settings, "autobump_diffuse_transmit")
        layout.prop(settings, "autobump_specular_transmit")
        layout.prop(settings, "autobump_volume")
        layout.prop(settings, "autobump_diffuse_reflect")
        layout.prop(settings, "autobump_specular_reflect")
        layout.prop(settings, "autobump_subsurface")


class ARNOLD_HYDRA_GEOM_PT_volume(ArnoldShapePanel):
    bl_label = "Volume"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "step_size")
        layout.prop(settings, "step_scale")
        layout.prop(settings, "volume_padding")
        layout.prop(settings, "mipmap_bias")


class ARNOLD_HYDRA_GEOM_PT_motion_blur(ArnoldShapePanel):
    bl_label = "Motion Blur"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "transform_type")
        layout.prop(settings, "deform_keys")
        layout.prop(settings, "transform_keys")


class ARNOLD_HYDRA_GEOM_PT_visibility(ArnoldShapePanel):
    bl_label = "Visibility"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "vis_camera")
        layout.prop(settings, "vis_shadow")
        layout.prop(settings, "vis_diffuse_transmit")
        layout.prop(settings, "vis_specular_transmit")
        layout.prop(settings, "vis_volume")
        layout.prop(settings, "vis_diffuse_reflect")
        layout.prop(settings, "vis_specular_reflect")
        layout.prop(settings, "receive_shadows")
        layout.prop(settings, "self_shadows")
        layout.prop(settings, "opaque")
        layout.prop(settings, "matte")

        #layout.separator()
        #layout.prop(arnold, "trace_sets")
        #layout.prop(arnold, "interior_set")


class ARNOLD_HYDRA_GEOM_PT_normals(ArnoldShapePanel):
    bl_label = "Normals"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "smoothing")
        layout.prop(settings, "invert_normals")
        layout.prop(settings, "double_sided_camera")
        layout.prop(settings, "double_sided_shadow")
        layout.prop(settings, "double_sided_diffuse_transmit")
        layout.prop(settings, "double_sided_specular_transmit")
        layout.prop(settings, "double_sided_volume")
        layout.prop(settings, "double_sided_diffuse_reflect")
        layout.prop(settings, "double_sided_specular_reflect")
        

class ARNOLD_HYDRA_GEOM_PT_shape(ArnoldShapePanel):
    bl_label = "Shape"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "min_pixel_width")
        layout.prop(settings, "default_radius")
        layout.prop(settings, "basis")
        layout.prop(settings, "mode")


class ARNOLD_HYDRA_GEOM_PT_light(ArnoldShapePanel):
    bl_label = "Light"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "light")

        col = layout.column(align=True)
        col.enabled = settings.light
        col.prop(settings, "light_color")
        col.prop(settings, "light_intensity")
        col.prop(settings, "light_exposure")
        col.prop(settings, "light_cast_shadows")
        col.prop(settings, "light_cast_volumetric_shadows")
        col.prop(settings, "light_shadow_density")
        col.prop(settings, "light_shadow_color")
        col.prop(settings, "light_samples")
        col.prop(settings, "light_normalize")
        col.prop(settings, "light_diffuse")
        col.prop(settings, "light_specular")
        col.prop(settings, "light_sss")
        col.prop(settings, "light_indirect")
        col.prop(settings, "light_max_bounces")
        col.prop(settings, "light_volume_samples")
        col.prop(settings, "light_volume")
        #col.prop(arnold, "light_aov")
        col.prop(settings, "light_sampling_mode")
        #col.prop(arnold, "shaders")


register, unregister = bpy.utils.register_classes_factory((
    ARNOLD_HYDRA_GEOM_PT_arnold,
    ARNOLD_HYDRA_GEOM_PT_subdivision,
    ARNOLD_HYDRA_GEOM_PT_displacement,
    ARNOLD_HYDRA_GEOM_PT_volume,
    ARNOLD_HYDRA_GEOM_PT_motion_blur,
    ARNOLD_HYDRA_GEOM_PT_visibility,
    ARNOLD_HYDRA_GEOM_PT_normals,
    ARNOLD_HYDRA_GEOM_PT_shape,
    ARNOLD_HYDRA_GEOM_PT_light,
))
