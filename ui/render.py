import bpy
from ..engine import ArnoldHydraRenderEngine

class ArnoldRenderPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES
    
    def setup(self, context):
        layout = self.layout
        layout.use_property_split = True
        settings = getattr(context.scene.arnold, "global")
        return layout, settings

def draw_device(self, context):
    scene = context.scene
    layout = self.layout
    layout.use_property_split = True
    layout.use_property_decorate = False

    if context.engine == ArnoldHydraRenderEngine.bl_idname:
        settings = getattr(scene.arnold, "global")
        layout.prop(settings, "render_device")
        

class ARNOLD_HYDRA_RENDER_PT_sampling(ArnoldRenderPanel):
    bl_label = "Sampling"

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "AA_samples")
        layout.prop(settings, "GI_diffuse_samples")
        layout.prop(settings, "GI_specular_samples")
        layout.prop(settings, "GI_transmission_samples")
        layout.prop(settings, "GI_sss_samples")
        layout.prop(settings, "GI_volume_samples")

        layout.separator()

        layout.prop(settings, "enable_progressive_render")


class ARNOLD_HYDRA_RENDER_PT_sampling_adaptive(ArnoldRenderPanel):
    bl_label = "Adaptive Sampling"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_sampling"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "enable_adaptive_sampling")

        col = layout.column(align=True)
        col.enabled = settings.enable_adaptive_sampling
        col.prop(settings, "AA_samples_max")
        col.prop(settings, "AA_adaptive_threshold")


class ARNOLD_HYDRA_RENDER_PT_sampling_clamping(ArnoldRenderPanel):
    bl_label = "Clamping"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_sampling"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "AA_sample_clamp_affects_aovs")
        layout.prop(settings, "AA_sample_clamp")
        layout.prop(settings, "indirect_sample_clamp")


class ARNOLD_HYDRA_RENDER_PT_sampling_advanced(ArnoldRenderPanel):
    bl_label = "Advanced"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_sampling"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "AA_seed")
        layout.prop(settings, "stochastic_volume_interpolation")
        layout.prop(settings, "procedural_instancing_optimization")
        layout.prop(settings, "dialectric_priorities")
        layout.prop(settings, "indirect_specular_blur")


class ARNOLD_HYDRA_RENDER_PT_ray_depth(ArnoldRenderPanel):
    bl_label = "Ray Depth"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "GI_total_depth")
        layout.prop(settings, "GI_diffuse_depth")
        layout.prop(settings, "GI_specular_depth")
        layout.prop(settings, "GI_transmission_depth")
        layout.prop(settings, "GI_volume_depth")
        layout.prop(settings, "auto_transparency_depth")

        # FOR SHADERS
        # col.prop(r, "background")
        # col.prop(r, "atmosphere")
        # col.prop(r, "aov_shaders")
        # col.prop(r, "imager")


class ARNOLD_HYDRA_RENDER_PT_subdivision(ArnoldRenderPanel):
    bl_label = "Subdivision"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "subdiv_dicing_camera")
        layout.prop(settings, "subdiv_frustum_culling")

        col = layout.column(align=True)
        col.enabled = settings.subdiv_frustum_culling
        col.prop(settings, "subdiv_frustum_padding")


class ARNOLD_HYDRA_RENDER_PT_lights(ArnoldRenderPanel):
    bl_label = "Lights"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "light_samples")
        layout.prop(settings, "low_light_threshold")
        layout.prop(settings, "nits_per_unit")


class ARNOLD_HYDRA_RENDER_PT_textures(ArnoldRenderPanel):
    bl_label = "Textures"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "texture_max_memory_MB")
        layout.prop(settings, "texture_max_open_files")

        layout.prop(settings, "texture_automip")
        layout.prop(settings, "texture_accept_untiled")
        layout.prop(settings, "texture_autotile")

        layout.prop(settings, "texture_accept_unmipped")
        layout.prop(settings, "texture_auto_generate_tx")

        col = layout.column(align=True)
        col.enabled = not settings.texture_auto_generate_tx
        col.prop(settings, "texture_use_existing_tx")

        col = layout.column(align=True)
        col.enabled = settings.texture_auto_generate_tx
        col.prop(settings, "texture_auto_tx_path")


class ARNOLD_HYDRA_RENDER_PT_device(ArnoldRenderPanel):
    bl_label = "Device"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "render_device")
        layout.prop(settings, "render_device_fallback")


class ARNOLD_HYDRA_RENDER_PT_device_automatic(ArnoldRenderPanel):
    bl_label = "Automatic Device Selection"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_device"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "gpu_default_names")
        layout.prop(settings, "gpu_default_min_memory_MB")


class ARNOLD_HYDRA_RENDER_PT_device_manual(ArnoldRenderPanel):
    bl_label = "Manual Device Selection"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_device"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "manual_device_selection")

        col = layout.column(align=True)
        col.enabled = settings.manual_device_selection
        col.prop(settings, "device_selection")


class ARNOLD_HYDRA_RENDER_PT_system(ArnoldRenderPanel):
    bl_label = "System"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "threads")
        layout.prop(settings, "bucket_size")
        layout.prop(settings, "bucket_scanning")
        layout.prop(settings, "parallel_node_init")
        layout.prop(settings, "abort_on_error")
        layout.prop(settings, "abort_on_license_fail")
        layout.prop(settings, "skip_license_check")
        layout.prop(settings, "plugin_searchpath")
        layout.prop(settings, "asset_searchpath")


class ARNOLD_HYDRA_RENDER_PT_diagnostics(ArnoldRenderPanel):
    bl_label = "Diagnostics"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "log_file")
        layout.prop(settings, "log_verbosity")
        
        layout.separator()

        row = layout.row()
        row.prop(settings, "enable_report", text="Report File")
        col_rep = row.column(align=True)
        col_rep.enabled = settings.enable_report
        col_rep.prop(settings, "report_file", text="")

        row = layout.row()
        row.prop(settings, "enable_stats", text="Stats File")
        col_stat = row.column(align=True)
        col_stat.enabled = settings.enable_stats
        col_stat.prop(settings, "stats_file", text="")

        row = layout.row()
        row.prop(settings, "enable_profile", text="Profile File")
        col_prof = row.column(align=True)
        col_prof.enabled = settings.enable_profile
        col_prof.prop(settings, "profile_file", text="")

        layout.separator()

        layout.prop(settings, "ignore_operators")
        layout.prop(settings, "ignore_imagers")
        layout.prop(settings, "ignore_textures")
        layout.prop(settings, "ignore_shaders")
        layout.prop(settings, "ignore_atmosphere")
        layout.prop(settings, "ignore_lights")
        layout.prop(settings, "ignore_shadows")
        layout.prop(settings, "ignore_subdivision")
        layout.prop(settings, "ignore_displacement")
        layout.prop(settings, "ignore_bump")
        layout.prop(settings, "ignore_motion_blur")
        layout.prop(settings, "ignore_dof")
        layout.prop(settings, "ignore_sss")


register_classes, unregister_classes = bpy.utils.register_classes_factory((
    ARNOLD_HYDRA_RENDER_PT_sampling,
    ARNOLD_HYDRA_RENDER_PT_sampling_adaptive,
    ARNOLD_HYDRA_RENDER_PT_sampling_clamping,
    ARNOLD_HYDRA_RENDER_PT_sampling_advanced,
    ARNOLD_HYDRA_RENDER_PT_ray_depth,
    ARNOLD_HYDRA_RENDER_PT_subdivision,
    ARNOLD_HYDRA_RENDER_PT_lights,
    ARNOLD_HYDRA_RENDER_PT_textures,
    ARNOLD_HYDRA_RENDER_PT_device,
    ARNOLD_HYDRA_RENDER_PT_device_automatic,
    ARNOLD_HYDRA_RENDER_PT_device_manual,
    ARNOLD_HYDRA_RENDER_PT_system,
    ARNOLD_HYDRA_RENDER_PT_diagnostics
))


def get_panels():
    exclude_panels = {
        'RENDER_PT_stamp',
        'DATA_PT_light',
        'DATA_PT_spot',
        'NODE_DATA_PT_light',
        'DATA_PT_falloff_curve',
        'RENDER_PT_post_processing',
        'RENDER_PT_simplify',
        'SCENE_PT_audio',
        'RENDER_PT_freestyle'
    }
    include_eevee_panels = {
        'MATERIAL_PT_preview',
        'EEVEE_MATERIAL_PT_context_material',
        'EEVEE_MATERIAL_PT_surface',
        'EEVEE_MATERIAL_PT_volume',
        'EEVEE_MATERIAL_PT_settings',
        'EEVEE_WORLD_PT_surface',
    }
    for panel_cls in bpy.types.Panel.__subclasses__():
        if (compat_engines := getattr(panel_cls, 'COMPAT_ENGINES', None)) is None:
            continue
        if (
            (
                'BLENDER_RENDER' in compat_engines
                and panel_cls.__name__ not in exclude_panels
            )
            or (
                'BLENDER_EEVEE' in compat_engines
                and panel_cls.__name__ in include_eevee_panels
            )
        ):
            yield panel_cls


def register():
    register_classes()

    bpy.types.RENDER_PT_context.append(draw_device)

    for panel_cls in get_panels():
        panel_cls.COMPAT_ENGINES.add(ArnoldHydraRenderEngine.bl_idname)


def unregister():
    for panel_cls in get_panels():
        if ArnoldHydraRenderEngine.bl_idname in panel_cls.COMPAT_ENGINES:
            panel_cls.COMPAT_ENGINES.remove(ArnoldHydraRenderEngine.bl_idname)

    bpy.types.RENDER_PT_context.remove(draw_device)

    unregister_classes()
