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
        layout.prop(arnold, "subdiv_adaptive_metric")
        layout.prop(arnold, "subdiv_adaptive_error")
        layout.prop(arnold, "subdiv_adaptive_space")
        layout.prop(arnold, "subdiv_uv_smoothing")
        layout.prop(arnold, "subdiv_smooth_derivs")
        layout.prop(arnold, "subdiv_frustum_ignore")

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
        layout.prop(arnold, "disp_autobump")
        
        layout.prop(arnold, "autobump_camera")
        layout.prop(arnold, "autobump_shadow")
        layout.prop(arnold, "autobump_diffuse_transmit")
        layout.prop(arnold, "autobump_specular_transmit")
        layout.prop(arnold, "autobump_volume")
        layout.prop(arnold, "autobump_diffuse_reflect")
        layout.prop(arnold, "autobump_specular_reflect")
        layout.prop(arnold, "autobump_subsurface")

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
        col.prop(arnold, "receive_shadows")
        col.prop(arnold, "self_shadows")
        col.prop(arnold, "opaque")
        col.prop(arnold, "matte")

        #layout.separator()
        #layout.prop(arnold, "trace_sets")
        #layout.prop(arnold, "interior_set")

class ARNOLD_HYDRA_GEOM_PT_normals(bpy.types.Panel):
    bl_label = "Normals"
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
        col.prop(arnold, "smoothing")
        col.prop(arnold, "invert_normals")
        col.prop(arnold, "double_sided_camera")
        col.prop(arnold, "double_sided_shadow")
        col.prop(arnold, "double_sided_diffuse_transmit")
        col.prop(arnold, "double_sided_specular_transmit")
        col.prop(arnold, "double_sided_volume")
        col.prop(arnold, "double_sided_diffuse_reflect")
        col.prop(arnold, "double_sided_specular_reflect")
        

class ARNOLD_HYDRA_GEOM_PT_shape(bpy.types.Panel):
    bl_label = "Shape"
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
        layout.prop(arnold, "default_radius")
        layout.prop(arnold, "basis")
        layout.prop(arnold, "mode")


class ARNOLD_HYDRA_GEOM_PT_light(Panel):
    bl_label = "Light"
    bl_parent_id = "ARNOLD_HYDRA_GEOM_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        arnold = context.object.arnold

        layout.prop(arnold, "light")

        col = layout.column(align=True)
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
        #col.prop(arnold, "light_aov")
        col.prop(arnold, "light_sampling_mode")
        #col.prop(arnold, "shaders")


register_classes, unregister_classes = bpy.utils.register_classes_factory((
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


def register():
    register_classes()


def unregister():
    unregister_classes()
