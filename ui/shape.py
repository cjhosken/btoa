import bpy

from ..engine import ArnoldHydraRenderEngine


class Panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.object and context.object.type == 'MESH'


class ARNOLD_HYDRA_GEOM_PT_arnold(Panel):
    bl_label = "Arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        pass


class ARNOLD_HYDRA_GEOM_PT_render_stats(bpy.types.Panel):
    bl_label = "Render Stats"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.object and context.object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.object.arnold

        layout.prop(arnold, "opaque")
        layout.prop(arnold, "matte")
        layout.prop(arnold, "smoothing")
        layout.prop(arnold, "invert_normals")
        layout.prop(arnold, "receive_shadows")
        layout.prop(arnold, "self_shadows")


class ARNOLD_HYDRA_GEOM_PT_subdivision(bpy.types.Panel):
    bl_label = "Subdivision"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.object and context.object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.object.arnold

        layout.prop(arnold, "subdiv_type")
        layout.prop(arnold, "subdiv_iterations")
        layout.prop(arnold, "subdiv_frustum_ignore")
        layout.prop(arnold, "subdiv_uv_smoothing")
        layout.prop(arnold, "subdiv_smooth_derivs")

        layout.separator()
        layout.label(text="Adaptive Subdivision")
        layout.prop(arnold, "subdiv_adaptive_metric")
        layout.prop(arnold, "subdiv_adaptive_error")
        layout.prop(arnold, "subdiv_adaptive_space")


class ARNOLD_HYDRA_GEOM_PT_displacement(bpy.types.Panel):
    bl_label = "Displacement"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.object and context.object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.object.arnold

        layout.prop(arnold, "disp_height")
        layout.prop(arnold, "disp_zero_value")
        layout.prop(arnold, "disp_padding")

        layout.separator()
        layout.prop(arnold, "disp_autobump")
        
        col = layout.column(align=True)
        col.active = arnold.disp_autobump
        col.prop(arnold, "autobump_camera")
        col.prop(arnold, "autobump_shadow")
        col.prop(arnold, "autobump_diffuse_transmit")
        col.prop(arnold, "autobump_specular_transmit")
        col.prop(arnold, "autobump_volume")
        col.prop(arnold, "autobump_diffuse_reflect")
        col.prop(arnold, "autobump_specular_reflect")
        col.prop(arnold, "autobump_subsurface")


class ARNOLD_HYDRA_GEOM_PT_visibility(bpy.types.Panel):
    bl_label = "Visibility"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.object and context.object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.object.arnold

        col = layout.column(align=True)
        col.prop(arnold, "vis_camera")
        col.prop(arnold, "vis_shadow")
        col.prop(arnold, "vis_diffuse_transmit")
        col.prop(arnold, "vis_specular_transmit")
        col.prop(arnold, "vis_volume")
        col.prop(arnold, "vis_diffuse_reflect")
        col.prop(arnold, "vis_specular_reflect")
        col.prop(arnold, "vis_subsurface")

        layout.separator()
        layout.label(text="Double Sided")
        col = layout.column(align=True)
        col.prop(arnold, "double_sided_diffuse_reflect")
        col.prop(arnold, "double_sided_specular_reflect")
        col.prop(arnold, "double_sided_volume")


class ARNOLD_HYDRA_GEOM_PT_volume(bpy.types.Panel):
    bl_label = "Volume"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.object and context.object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.object.arnold

        layout.prop(arnold, "step_size")
        layout.prop(arnold, "step_scale")
        layout.prop(arnold, "volume_padding")
        layout.prop(arnold, "mipmap_bias")


class ARNOLD_HYDRA_GEOM_PT_motion_blur(bpy.types.Panel):
    bl_label = "Motion Blur"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.object and context.object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.object.arnold

        layout.prop(arnold, "transform_type")
        layout.prop(arnold, "deform_keys")
        layout.prop(arnold, "transform_keys")


class ARNOLD_HYDRA_GEOM_PT_curves_points(bpy.types.Panel):
    bl_label = "Curves / Points"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.object and context.object.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.object.arnold

        layout.prop(arnold, "min_pixel_width")
        layout.prop(arnold, "radius")
        layout.prop(arnold, "default_radius")
        layout.prop(arnold, "basis")
        layout.prop(arnold, "mode")


class ARNOLD_HYDRA_GEOM_PT_mesh_light(Panel):
    bl_label = "Mesh Light"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        arnold = context.object.arnold

        layout.prop(arnold, "light")

        col = layout.column(align=True)
        col.active = arnold.light
        col.prop(arnold, "light_color")
        col.prop(arnold, "light_intensity")
        col.prop(arnold, "light_exposure")
        col.prop(arnold, "light_cast_shadows")
        col.prop(arnold, "light_cast_volumetric_shadows")
        col.prop(arnold, "light_shadow_density")
        col.prop(arnold, "light_shadow_color")
        col.prop(arnold, "light_samples")
        col.prop(arnold, "light_normalize")
        col.prop(arnold, "light_diffuse")
        col.prop(arnold, "light_specular")
        col.prop(arnold, "light_sss")
        col.prop(arnold, "light_indirect")
        col.prop(arnold, "light_max_bounces")
        col.prop(arnold, "light_volume_samples")
        col.prop(arnold, "light_volume")
        col.prop(arnold, "light_sampling_mode")
        col.prop(arnold, "light_aov")


register_classes, unregister_classes = bpy.utils.register_classes_factory((
    ARNOLD_HYDRA_GEOM_PT_arnold,
    ARNOLD_HYDRA_GEOM_PT_render_stats,
    ARNOLD_HYDRA_GEOM_PT_subdivision,
    ARNOLD_HYDRA_GEOM_PT_displacement,
    ARNOLD_HYDRA_GEOM_PT_visibility,
    ARNOLD_HYDRA_GEOM_PT_volume,
    ARNOLD_HYDRA_GEOM_PT_motion_blur,
    ARNOLD_HYDRA_GEOM_PT_curves_points,
    ARNOLD_HYDRA_GEOM_PT_mesh_light,
))


def register():
    register_classes()


def unregister():
    unregister_classes()
