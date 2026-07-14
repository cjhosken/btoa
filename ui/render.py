import bpy
from ..engine import ArnoldHydraRenderEngine

class Panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

def draw_device(self, context):
    scene = context.scene
    layout = self.layout
    layout.use_property_split = True
    layout.use_property_decorate = False

    if context.engine == ArnoldHydraRenderEngine.bl_idname:
        r = getattr(scene.arnold, "global")
        layout.prop(r, "render_device", text="Device")
        

class ARNOLD_HYDRA_RENDER_PT_sampling(Panel):
    bl_label = "Sampling"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "AA_samples")
        col.prop(r, "GI_diffuse_samples")
        col.prop(r, "GI_specular_samples")
        col.prop(r, "GI_transmission_samples")
        col.prop(r, "GI_sss_samples")
        col.prop(r, "GI_volume_samples")
        col.separator()
        col.prop(r, "enable_progressive_render")


class ARNOLD_HYDRA_RENDER_PT_sampling_adaptive(bpy.types.Panel):
    bl_label = "Adaptive Sampling"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_sampling"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        layout.prop(r, "enable_adaptive_sampling")

        col = layout.column(align=True)
        col.enabled = r.enable_adaptive_sampling
        col.prop(r, "AA_samples_max")
        col.prop(r, "AA_adaptive_threshold")


class ARNOLD_HYDRA_RENDER_PT_sampling_clamping(bpy.types.Panel):
    bl_label = "Clamping"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_sampling"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "AA_sample_clamp_affects_aovs")
        col.prop(r, "AA_sample_clamp")
        layout.prop(r, "indirect_sample_clamp")


class ARNOLD_HYDRA_RENDER_PT_sampling_advanced(bpy.types.Panel):
    bl_label = "Advanced"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_sampling"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        layout.prop(r, "AA_seed")
        layout.prop(r, "stochastic_volume_interpolation")
        layout.prop(r, "procedural_instancing_optimization")
        layout.prop(r, "dialectric_priorities")
        layout.prop(r, "indirect_specular_blur")

class ARNOLD_HYDRA_RENDER_PT_ray_depth(Panel):
    bl_label = "Ray Depth"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "GI_total_depth")
        col.prop(r, "GI_diffuse_depth")
        col.prop(r, "GI_specular_depth")
        col.prop(r, "GI_transmission_depth")
        col.prop(r, "GI_volume_depth")
        col.prop(r, "auto_transparency_depth")



        # FOR SHADERS
        # col.prop(r, "background")
        # col.prop(r, "atmosphere")
        # col.prop(r, "aov_shaders")
        # col.prop(r, "imager")

class ARNOLD_HYDRA_RENDER_PT_subdivision(Panel):
    bl_label = "Subdivision"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "subdiv_dicing_camera")
        col.prop(r, "subdiv_frustum_culling")

        col = layout.column(align=True)
        col.enabled = r.subdiv_frustum_culling
        col.prop(r, "subdiv_frustum_padding")

class ARNOLD_HYDRA_RENDER_PT_lights(Panel):
    bl_label = "Lights"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        layout.prop(r, "light_samples")
        layout.prop(r, "low_light_threshold")
        layout.prop(r, "nits_per_unit")

class ARNOLD_HYDRA_RENDER_PT_textures(Panel):
    bl_label = "Textures"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "texture_max_memory_MB")
        col.prop(r, "texture_max_open_files")

        col.prop(r, "texture_automip")
        col.prop(r, "texture_accept_untiled")
        col.prop(r, "texture_autotile")

        col.prop(r, "texture_accept_unmipped")
        col.prop(r, "texture_auto_generate_tx")

        col = layout.column(align=True)
        col.enabled = not r.texture_auto_generate_tx
        col.prop(r, "texture_use_existing_tx")

        col = layout.column(align=True)
        col.enabled = r.texture_auto_generate_tx
        col.prop(r, "texture_auto_tx_path")

class ARNOLD_HYDRA_RENDER_PT_device(Panel):
    bl_label = "Device"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "render_device")
        col.prop(r, "render_device_fallback")

class ARNOLD_HYDRA_RENDER_PT_device_automatic(Panel):
    bl_label = "Automatic Device Selection"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_device"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "gpu_default_names")
        col.prop(r, "gpu_default_min_memory_MB")

class ARNOLD_HYDRA_RENDER_PT_device_manual(Panel):
    bl_label = "Manual Device Selection"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_device"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "manual_device_selection")

        col = layout.column(align=True)
        col.enabled = r.manual_device_selection
        col.prop(r, "device_selection")

class ARNOLD_HYDRA_RENDER_PT_system(Panel):
    bl_label = "System"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "threads")
        col.prop(r, "bucket_size")
        col.prop(r, "bucket_scanning")
        col.prop(r, "parallel_node_init")
        col.prop(r, "abort_on_error")
        col.prop(r, "abort_on_license_fail")
        col.prop(r, "skip_license_check")
        col.prop(r, "plugin_searchpath")
        col.prop(r, "asset_searchpath")

class ARNOLD_HYDRA_RENDER_PT_diagnostics(Panel):
    bl_label = "Diagnostics"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "log_file")
        col.prop(r, "log_verbosity")
        
        col.separator()

        row = col.row()
        row.prop(r, "enable_report", text="Report File")
        col_rep = row.column(align=True)
        col_rep.enabled = r.enable_report
        col_rep.prop(r, "report_file", text="")

        row = col.row()
        row.prop(r, "enable_stats", text="Stats File")
        col_stat = row.column(align=True)
        col_stat.enabled = r.enable_stats
        col_stat.prop(r, "stats_file", text="")

        row = col.row()
        row.prop(r, "enable_profile", text="Profile File")
        col_prof = row.column(align=True)
        col_prof.enabled = r.enable_profile
        col_prof.prop(r, "profile_file", text="")

        col.separator()

        col.prop(r, "ignore_operators")
        col.prop(r, "ignore_imagers")
        col.prop(r, "ignore_textures")
        col.prop(r, "ignore_shaders")
        col.prop(r, "ignore_atmosphere")
        col.prop(r, "ignore_lights")
        col.prop(r, "ignore_shadows")
        col.prop(r, "ignore_subdivision")
        col.prop(r, "ignore_displacement")
        col.prop(r, "ignore_bump")
        col.prop(r, "ignore_motion_blur")
        col.prop(r, "ignore_dof")
        col.prop(r, "ignore_sss")




# ---------------------------------------------------------------------------
# Class registration
# ---------------------------------------------------------------------------

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
