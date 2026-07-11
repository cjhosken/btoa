import bpy

def update_render_device(self, context):
    if context is None:
        return
    context.scene.update_tag()
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEWPORT_3D':
                area.tag_redraw()


class ArnoldAovShader(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="")


class ArnoldGlobalRenderProperties(bpy.types.PropertyGroup):

    AA_adaptive_threshold: bpy.props.FloatProperty(
        name="AA Adaptive Threshold",
        default=0.15
    )

    AA_sample_clamp: bpy.props.FloatProperty(
        name="AA Sample Clamp",
        default=10000000.0
    )

    AA_sample_clamp_affects_aovs: bpy.props.BoolProperty(
        name="AA Sample Clamp Affects AOVs",
        default=False
    )

    AA_samples: bpy.props.IntProperty(
        name="AA Samples",
        default=3, min=0
    )

    AA_samples_max: bpy.props.IntProperty(
        name="AA Samples Max",
        default=20, min=0
    )

    AA_seed: bpy.props.IntProperty(
        name="AA Seed",
        default=1
    )

    abort_on_error: bpy.props.BoolProperty(
        name="Abort on Error",
        default=False
    )

    abort_on_license_fail: bpy.props.BoolProperty(
        name="Abort on License Fail",
        default=False
    )

    asset_searchpath: bpy.props.StringProperty(
        name="Asset Search Path",
        default=""
    )

    atmosphere: bpy.props.StringProperty(
        name="Atmosphere",
        default=""
    )

    auto_transparency_depth: bpy.props.IntProperty(
        name="Auto Transparency Depth",
        default=10, min=0
    )

    background: bpy.props.StringProperty(
        name="Background",
        default=""
    )

    bucket_scanning: bpy.props.EnumProperty(
        name="Bucket Scanning",
        items=[
            ("spiral", "Spiral", ""),
            ("left_to_right", "Left to Right", ""),
            ("random", "Random", "")
        ],
        default="spiral"
    )

    bucket_size: bpy.props.IntProperty(
        name="Bucket Size",
        default=64, min=0
    )

    dialectric_priorities: bpy.props.BoolProperty(
        name="Dialectric Priorities",
        default=True
    )

    enable_adaptive_sampling: bpy.props.BoolProperty(
        name="Enable Adaptive Sampling",
        default=False
    )

    enable_progressive_render: bpy.props.BoolProperty(
        name="Enable Progressive Render",
        default=True
    )

    GI_diffuse_depth: bpy.props.IntProperty(
        name="Diffuse Depth",
        default=1, min=0
    )
    GI_diffuse_samples: bpy.props.IntProperty(
        name="Diffuse Samples",
        default=2, min=0
    )
    GI_specular_depth: bpy.props.IntProperty(
        name="Specular Depth",
        default=1, min=0
    )
    GI_specular_samples: bpy.props.IntProperty(
        name="Specular Samples",
        default=2, min=0
    )
    GI_sss_samples: bpy.props.IntProperty(
        name="SSS Samples",
        default=2, min=0
    )
    GI_total_depth: bpy.props.IntProperty(
        name="Total Depth",
        default=10, min=0
    )
    GI_transmission_depth: bpy.props.IntProperty(
        name="Transmission Depth",
        default=8, min=0
    )
    GI_transmission_samples: bpy.props.IntProperty(
        name="Transmission Samples",
        default=2, min=0
    )
    GI_volume_depth: bpy.props.IntProperty(
        name="Volume Depth",
        default=0, min=0
    )
    GI_volume_samples: bpy.props.IntProperty(
        name="Volume Samples",
        default=2, min=0
    )

    gpu_default_min_memory_MB: bpy.props.IntProperty(
        name="GPU Default Min Memory MB",
        default=512, min=0
    )
    gpu_default_names: bpy.props.StringProperty(
        name="GPU Default Names",
        default="*"
    )
    
    ignore_atmosphere: bpy.props.BoolProperty(
        name="Ignore Atmosphere", default=False
    )
    ignore_bump: bpy.props.BoolProperty(
        name="Ignore Bump", default=False
    )
    ignore_displacement: bpy.props.BoolProperty(
        name="Ignore Displacement", default=False
    )
    ignore_dof: bpy.props.BoolProperty(
        name="Ignore DOF", default=False
    )
    ignore_imagers: bpy.props.BoolProperty(
        name="Ignore Imagers", default=False
    )
    ignore_lights: bpy.props.BoolProperty(
        name="Ignore Lights", default=False
    )
    ignore_motion_blur: bpy.props.BoolProperty(
        name="Ignore Motion Blur", default=False
    )
    ignore_operators: bpy.props.BoolProperty(
        name="Ignore Operators", default=False
    )
    ignore_shaders: bpy.props.BoolProperty(
        name="Ignore Shaders", default=False
    )
    ignore_shadows: bpy.props.BoolProperty(
        name="Ignore Shadows", default=False
    )
    ignore_smoothing: bpy.props.BoolProperty(
        name="Ignore Smoothing", default=False
    )
    ignore_sss: bpy.props.BoolProperty(
        name="Ignore SSS", default=False
    )
    ignore_subdivision: bpy.props.BoolProperty(
        name="Ignore Subdivision", default=False
    )
    ignore_textures: bpy.props.BoolProperty(
        name="Ignore Textures", default=False
    )

    imager: bpy.props.StringProperty(
        name="Imager", default=""
    )
    indirect_sample_clamp: bpy.props.FloatProperty(
        name="Indirect Sample Clamp", default=10.0, min=0.0
    )
    indirect_specular_blur: bpy.props.FloatProperty(
        name="Indirect Specular Blur", default=1.0, min=0.0
    )
    light_samples: bpy.props.IntProperty(
        name="Light Samples", default=0, min=0
    )

    log_file: bpy.props.StringProperty(
        name="Log File",
        default=""
    )
    
    log_verbosity: bpy.props.IntProperty(
        name="Log Verbosity",
        default=2, min=0, max=5
    )

    low_light_threshold: bpy.props.FloatProperty(
        name="Low Light Threshold", default=0.001, min=0.0
    )
    manual_device_selection: bpy.props.BoolProperty(
        name="Manual Device Selection", default=False
    )
    nits_per_unit: bpy.props.FloatProperty(
        name="Nits Per Unit", default=1000.0, min=0.0
    )
    osl_includepath: bpy.props.StringProperty(
        name="OSL Include Path", default=""
    )
    parallel_node_init: bpy.props.BoolProperty(
        name="Parallel Node Init", default=True
    )
    plugin_searchpath: bpy.props.StringProperty(
        name="Plugin Search Path", default=""
    )
    procedural_instancing_optimization: bpy.props.EnumProperty(
        name="Procedural Instancing Optimization",
        items=[
            ("conservative", "Conservative", ""),
            ("aggressive", "Aggressive", "")
        ],
        default="conservative"
    )

    profile_file: bpy.props.StringProperty(
        name="Profile File",
        default="$HOME/arnold_profile.json"
    )

    render_device: bpy.props.EnumProperty(
        name="Render Device",
        items=[
            ("CPU", "CPU", "Use CPU for rendering"),
            ("GPU", "GPU", "Use GPU for rendering")
        ],
        default="CPU",
        update=update_render_device
    )

    render_device_fallback: bpy.props.EnumProperty(
        name="Render Device Fallback",
        items=[
            ("error", "Error", "Abort on error if GPU rendering fails"),
            ("cpu", "CPU", "Fallback to CPU if GPU rendering fails")
        ],
        default="error"
    )

    report_file: bpy.props.StringProperty(
        name="Report File",
        default="$HOME/arnold_report.html"
    )

    skip_license_check: bpy.props.BoolProperty(
        name="Skip License Check", default=False
    )

    stats_file: bpy.props.StringProperty(
        name="Stats File",
        default="$HOME/arnold_stats.json"
    )

    stochastic_volume_interpolation: bpy.props.BoolProperty(
        name="Stochastic Volume Interpolation", default=True
    )

    subdiv_dicing_camera: bpy.props.StringProperty(
        name="Subdiv Dicing Camera", default=""
    )

    subdiv_frustum_culling: bpy.props.BoolProperty(
        name="Subdiv Frustum Culling", default=False
    )

    texture_accept_unmipped: bpy.props.BoolProperty(
        name="Texture Accept Unmipped", default=True
    )

    texture_accept_untiled: bpy.props.BoolProperty(
        name="Texture Accept Untiled", default=True
    )

    texture_auto_generate_tx: bpy.props.BoolProperty(
        name="Texture Auto Generate TX", default=True
    )

    texture_auto_tx_path: bpy.props.StringProperty(
        name="Texture Auto TX Path", default=""
    )

    texture_automip: bpy.props.BoolProperty(
        name="Texture Automip", default=True
    )

    texture_autotile: bpy.props.IntProperty(
        name="Texture Autotile", default=0
    )

    textre_max_memory_MB: bpy.props.FloatProperty(
        name="Texture Max Memory MB", default=4096.0, min=0.0
    )

    texture_max_open_files: bpy.props.IntProperty(
        name="Texture Max Open Files", default=0, min=0
    )

    texture_searchpath: bpy.props.StringProperty(
        name="Texture Search Path", default=""
    )

    texture_use_existing_tx: bpy.props.BoolProperty(
        name="Texture Use Existing TX", default=True
    )

    threads: bpy.props.IntProperty(
        name="Threads",
        default=-1
    )

    aov_shaders: bpy.props.CollectionProperty(
        type=ArnoldAovShader
    )

    aov_active_index: bpy.props.IntProperty(
        name="Active AOV Index",
        default=0
    )

    aov_combined: bpy.props.BoolProperty(
        name="Combined",
        description="Enable Combined (beauty RGBA) AOV pass",
        default=True
    )

    aov_depth: bpy.props.BoolProperty(
        name="Depth",
        description="Enable Depth (Z) AOV pass",
        default=False
    )

    aov_position: bpy.props.BoolProperty(
        name="Position",
        description="Enable Position (P) AOV pass",
        default=False
    )

    aov_normal: bpy.props.BoolProperty(
        name="Normal",
        description="Enable Normal (N) AOV pass",
        default=False
    )


class ArnoldRenderProperties(bpy.types.PropertyGroup):
    viewport: bpy.props.PointerProperty(type=ArnoldGlobalRenderProperties)

ArnoldRenderProperties.__annotations__['global'] = bpy.props.PointerProperty(type=ArnoldGlobalRenderProperties)


def register():
    bpy.utils.register_class(ArnoldAovShader)
    bpy.utils.register_class(ArnoldGlobalRenderProperties)
    bpy.utils.register_class(ArnoldRenderProperties)

    if not hasattr(bpy.types.Scene, "arnold"):
        bpy.types.Scene.arnold = bpy.props.PointerProperty(
            type=ArnoldRenderProperties
        )


def unregister():
    if hasattr(bpy.types.Scene, "arnold"):
        del bpy.types.Scene.arnold

    bpy.utils.unregister_class(ArnoldRenderProperties)
    bpy.utils.unregister_class(ArnoldGlobalRenderProperties)
    bpy.utils.unregister_class(ArnoldAovShader)
