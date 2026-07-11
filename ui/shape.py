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
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        arnold = obj.arnold

        # Settings Section
        layout.label(text="Settings")
        layout.prop(arnold, "opaque")
        layout.prop(arnold, "matte")
        layout.prop(arnold, "smoothing")
        layout.prop(arnold, "invert_normals")
        layout.prop(arnold, "receive_shadows")
        layout.prop(arnold, "self_shadows")

        layout.separator()
        layout.label(text="Subdivision")
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

        layout.separator()
        layout.label(text="Height")
        layout.prop(arnold, "disp_height")
        layout.prop(arnold, "disp_zero_value")
        layout.prop(arnold, "disp_padding")

        layout.separator()
        layout.label(text="Autobump Visibility")
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

        layout.separator()
        layout.label(text="Volume")
        layout.prop(arnold, "step_size")
        layout.prop(arnold, "step_scale")
        layout.prop(arnold, "volume_padding")
        layout.prop(arnold, "mipmap_bias")

        layout.separator()
        layout.label(text="Motion Blur")
        layout.prop(arnold, "transform_type")
        layout.prop(arnold, "deform_keys")
        layout.prop(arnold, "transform_keys")

        layout.separator()
        layout.label(text="Visibility")
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

        layout.separator()
        layout.label(text="Curves / Points")
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


def register():
    bpy.utils.register_class(ARNOLD_HYDRA_GEOM_PT_arnold)
    bpy.utils.register_class(ARNOLD_HYDRA_GEOM_PT_mesh_light)


def unregister():
    bpy.utils.unregister_class(ARNOLD_HYDRA_GEOM_PT_mesh_light)
    bpy.utils.unregister_class(ARNOLD_HYDRA_GEOM_PT_arnold)
