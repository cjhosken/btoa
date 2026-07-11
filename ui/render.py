import bpy

from ..engine import ArnoldHydraRenderEngine


class ARNOLD_UL_aovs(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "name", text="", emboss=False, icon='RENDERPASS')


class ARNOLD_OT_aov_add(bpy.types.Operator):
    bl_idname = "arnold.aov_add"
    bl_label = "Add AOV"

    def execute(self, context):
        r = getattr(context.scene.arnold, "global")
        item = r.aov_shaders.add()
        item.name = "AOV"
        r.aov_active_index = len(r.aov_shaders) - 1
        context.scene.update_tag()
        return {'FINISHED'}


class ARNOLD_OT_aov_remove(bpy.types.Operator):
    bl_idname = "arnold.aov_remove"
    bl_label = "Remove AOV"

    def execute(self, context):
        r = getattr(context.scene.arnold, "global")
        if len(r.aov_shaders) > 0:
            r.aov_shaders.remove(r.aov_active_index)
            r.aov_active_index = min(r.aov_active_index, len(r.aov_shaders) - 1)
            context.scene.update_tag()
        return {'FINISHED'}


class ARNOLD_HYDRA_RENDER_PT_aovs(bpy.types.Panel):
    bl_label = "Arnold AOVs"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'view_layer'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        r = getattr(context.scene.arnold, "global")
        if not r:
            return

        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column(heading="Passes")
        col.prop(r, "aov_combined", text="Combined (RGBA)")
        col.prop(r, "aov_depth", text="Depth (Z)")
        col.prop(r, "aov_position", text="Position (P)")
        col.prop(r, "aov_normal", text="Normal (N)")

        layout.separator()
        layout.label(text="Custom AOVs")

        row = layout.row()
        row.template_list("ARNOLD_UL_aovs", "", r, "aov_shaders", r, "aov_active_index")

        col = row.column(align=True)
        col.operator("arnold.aov_add", icon='ADD', text="")
        col.operator("arnold.aov_remove", icon='REMOVE', text="")


class Panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES


class ARNOLD_HYDRA_RENDER_PT_render(Panel):
    bl_label = "Render"
    bl_order = 0

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")
        layout.prop(r, "render_device", text="Device", expand=True)


class ARNOLD_HYDRA_RENDER_PT_sampling(Panel):
    bl_label = "Sampling"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "AA_samples")
        col.prop(r, "AA_samples_max")
        col.prop(r, "enable_adaptive_sampling")
        col.prop(r, "AA_adaptive_threshold")
        col.prop(r, "enable_progressive_render")
        col.prop(r, "AA_seed")


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


class ARNOLD_HYDRA_RENDER_PT_gi_samples(Panel):
    bl_label = "GI Samples"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "GI_diffuse_samples")
        col.prop(r, "GI_specular_samples")
        col.prop(r, "GI_transmission_samples")
        col.prop(r, "GI_sss_samples")
        col.prop(r, "GI_volume_samples")


class ARNOLD_HYDRA_RENDER_PT_device(Panel):
    bl_label = "Device & Clamping"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "render_device_fallback")
        col.prop(r, "manual_device_selection")
        col.prop(r, "gpu_default_min_memory_MB")
        col.prop(r, "gpu_default_names")

        col.separator()
        col.prop(r, "AA_sample_clamp")
        col.prop(r, "AA_sample_clamp_affects_aovs")
        col.prop(r, "indirect_sample_clamp")
        col.prop(r, "indirect_specular_blur")


class ARNOLD_HYDRA_RENDER_PT_textures(Panel):
    bl_label = "Textures"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "texture_searchpath")
        col.prop(r, "texture_max_open_files")
        col.prop(r, "texture_auto_generate_tx")
        col.prop(r, "texture_auto_tx_path")
        col.prop(r, "texture_use_existing_tx")
        col.prop(r, "texture_automip")
        col.prop(r, "texture_autotile")
        col.prop(r, "texture_accept_unmipped")
        col.prop(r, "texture_accept_untiled")


class ARNOLD_HYDRA_RENDER_PT_ignores(Panel):
    bl_label = "Ignore Flags"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "ignore_textures")
        col.prop(r, "ignore_shaders")
        col.prop(r, "ignore_lights")
        col.prop(r, "ignore_shadows")
        col.prop(r, "ignore_subdivision")
        col.prop(r, "ignore_displacement")
        col.prop(r, "ignore_bump")
        col.prop(r, "ignore_motion_blur")
        col.prop(r, "ignore_dof")
        col.prop(r, "ignore_smoothing")
        col.prop(r, "ignore_sss")
        col.prop(r, "ignore_operators")
        col.prop(r, "ignore_atmosphere")
        col.prop(r, "ignore_imagers")


class ARNOLD_HYDRA_RENDER_PT_diagnostics(Panel):
    bl_label = "Diagnostics & Paths"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        box = layout.box()
        box.label(text="Logging")
        box.prop(r, "log_verbosity")
        box.prop(r, "log_file")

        box = layout.box()
        box.label(text="Profiling & Reports")
        box.prop(r, "profile_file", text="Profile File")
        box.prop(r, "report_file", text="Report File")
        box.prop(r, "stats_file", text="Stats File")

        col = layout.column(align=True)
        col.prop(r, "asset_searchpath")
        col.prop(r, "plugin_searchpath")
        col.prop(r, "osl_includepath")
        col.prop(r, "subdiv_dicing_camera")


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
        col.prop(r, "low_light_threshold")
        col.prop(r, "nits_per_unit")
        col.prop(r, "stochastic_volume_interpolation")
        col.prop(r, "skip_license_check")
        col.prop(r, "abort_on_error")
        col.prop(r, "abort_on_license_fail")



register_classes, unregister_classes = bpy.utils.register_classes_factory((
    ARNOLD_UL_aovs,
    ARNOLD_OT_aov_add,
    ARNOLD_OT_aov_remove,
    ARNOLD_HYDRA_RENDER_PT_aovs,
    ARNOLD_HYDRA_RENDER_PT_render,
    ARNOLD_HYDRA_RENDER_PT_sampling,
    ARNOLD_HYDRA_RENDER_PT_ray_depth,
    ARNOLD_HYDRA_RENDER_PT_gi_samples,
    ARNOLD_HYDRA_RENDER_PT_device,
    ARNOLD_HYDRA_RENDER_PT_textures,
    ARNOLD_HYDRA_RENDER_PT_ignores,
    ARNOLD_HYDRA_RENDER_PT_diagnostics,
    ARNOLD_HYDRA_RENDER_PT_system,
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
    for panel_cls in get_panels():
        panel_cls.COMPAT_ENGINES.add(ArnoldHydraRenderEngine.bl_idname)


def unregister():
    for panel_cls in get_panels():
        if ArnoldHydraRenderEngine.bl_idname in panel_cls.COMPAT_ENGINES:
            panel_cls.COMPAT_ENGINES.remove(ArnoldHydraRenderEngine.bl_idname)
    unregister_classes()
