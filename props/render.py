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


class ArnoldImager(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="Imager")
    enabled: bpy.props.BoolProperty(name="Enabled", default=True)
    imager_type: bpy.props.EnumProperty(
        name="Type",
        items=[
            ("defaultArnoldDenoiser", "Arnold Denoiser", ""),
            ("aiImagerColorCorrect", "Color Correct", ""),
            ("aiImagerColorCurves", "Color Curves", ""),
            ("aiImagerDenoiserNoise", "Denoiser Noise", ""),
            ("aiImagerDenoiserOidn", "Denoiser Oidn", ""),
            ("aiImagerDenoiserOptix", "Denoiser Optix", ""),
            ("aiImagerExposure", "Exposure", ""),
            ("aiImagerLensEffects", "Lens Effects", ""),
            ("aiImagerOverlay", "Overlay", ""),
            ("aiImagerTonemap", "Tonemap", ""),
            ("aiImagerWhiteBalance", "WhiteBalance", ""),
        ],
        default="defaultArnoldDenoiser"
    )


class ArnoldGlobalRenderProperties(bpy.types.PropertyGroup):

    AA_adaptive_threshold: bpy.props.FloatProperty(
        name="Adaptive Threshold",
        default=0.15
    )

    enable_aa_sample_clamp: bpy.props.BoolProperty(
        name="Clamp AA Samples",
        default=False
    )

    AA_sample_clamp: bpy.props.FloatProperty(
        name="AA Clamp Value",
        default=10.0
    )

    AA_sample_clamp_affects_aovs: bpy.props.BoolProperty(
        name="Affect AOVs",
        default=False
    )

    AA_samples: bpy.props.IntProperty(
        name="Camera (AA)",
        default=3, min=0
    )

    AA_samples_max: bpy.props.IntProperty(
        name="Max. Camera (AA)",
        default=20, min=0
    )

    AA_seed: bpy.props.IntProperty(
        name="Seed",
        default=1
    )

    abort_on_error: bpy.props.BoolProperty(
        name="Abort On Error",
        default=False
    )

    abort_on_license_fail: bpy.props.BoolProperty(
        name="Abort On License Fail",
        default=False
    )

    asset_searchpath: bpy.props.StringProperty(
        name="Asset Search Path",
        default=""
    )

    atmosphere: bpy.props.PointerProperty(
        type=bpy.types.Material,
        name="Atmosphere"
    )

    auto_transparency_depth: bpy.props.IntProperty(
        name="Transparency Depth",
        default=10, min=0
    )

    background: bpy.props.PointerProperty(
        type=bpy.types.Image,
        name="Background"
    )

    bucket_scanning: bpy.props.EnumProperty(
        name="Bucket Scanning",
        items=[
            ("top", "Top", ""),
            ("left", "Left", ""),
            ("random", "Random", ""),
            ("spiral", "Spiral", ""),
            ("hilbert", "Hilbert", "")
        ],
        default="spiral"
    )

    bucket_size: bpy.props.IntProperty(
        name="Bucket Size",
        default=64, min=0
    )

    dialectric_priorities: bpy.props.BoolProperty(
        name="Nested Dielectrics",
        default=True
    )

    enable_adaptive_sampling: bpy.props.BoolProperty(
        name="Enable",
        default=False
    )

    enable_progressive_render: bpy.props.BoolProperty(
        name="Progressive Render",
        default=False
    )

    GI_diffuse_depth: bpy.props.IntProperty(
        name="Diffuse",
        default=1, min=0
    )
    GI_diffuse_samples: bpy.props.IntProperty(
        name="Diffuse",
        default=2, min=0
    )
    GI_specular_depth: bpy.props.IntProperty(
        name="Specular",
        default=1, min=0
    )
    GI_specular_samples: bpy.props.IntProperty(
        name="Specular",
        default=2, min=0
    )
    GI_sss_samples: bpy.props.IntProperty(
        name="SSS",
        default=2, min=0
    )
    GI_total_depth: bpy.props.IntProperty(
        name="Total",
        default=10, min=0
    )
    GI_transmission_depth: bpy.props.IntProperty(
        name="Transmission",
        default=8, min=0
    )
    GI_transmission_samples: bpy.props.IntProperty(
        name="Transmission",
        default=2, min=0
    )
    GI_volume_depth: bpy.props.IntProperty(
        name="Volume",
        default=0, min=0
    )
    GI_volume_samples: bpy.props.IntProperty(
        name="Volume Indirect",
        default=2, min=0
    )

    gpu_default_min_memory_MB: bpy.props.IntProperty(
        name="Min. Memory (MB)",
        default=512, min=0
    )
    gpu_default_names: bpy.props.StringProperty(
        name="GPU Names",
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
        name="Ignore Depth of Field", default=False
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

    imagers: bpy.props.CollectionProperty(
        type=ArnoldImager
    )

    imager_active_index: bpy.props.IntProperty(
        name="Active Imager Index",
        default=0
    )

    indirect_sample_clamp: bpy.props.FloatProperty(
        name="Indirect Clamp Value", default=10.0, min=0.0
    )

    indirect_specular_blur: bpy.props.FloatProperty(
        name="Indirect Specular Blur", default=1.0, min=0.0
    )

    enable_light_samples: bpy.props.BoolProperty(
        name="Global Light Sampling",
        default=False
    )

    light_samples: bpy.props.IntProperty(
        name="Light Samples", default=4, min=0
    )

    log_file: bpy.props.StringProperty(
        name="Filename",
        default=""
    )
    
    log_verbosity: bpy.props.EnumProperty(
        name="Verbosity Level",
        items=[
            ("error", "Errors", ""),
            ("warning", "Warnings", ""),
            ("info", "Info", ""),
            ("debug", "Debug", "")
        ],
        default="info"
    )

    log_to_console: bpy.props.BoolProperty(
        name="Console",
        default=True
    )

    log_to_file: bpy.props.BoolProperty(
        name="File",
        default=False
    )

    stats_to_file: bpy.props.BoolProperty(
        name="Render Statistics",
        default=False
    )

    profile_to_file: bpy.props.BoolProperty(
        name="Profile",
        default=False
    )

    absolute_texture_paths: bpy.props.BoolProperty(
        name="Absolute Texture Paths",
        default=False
    )

    absolute_procedural_paths: bpy.props.BoolProperty(
        name="Absolute Procedural Paths",
        default=False
    )

    procedural_searchpath: bpy.props.StringProperty(
        name="Procedural Search Path",
        default=""
    )

    gpu_max_texture_resolution: bpy.props.IntProperty(
        name="Max Texture Resolution",
        default=0, min=0
    )

    autodetect_threads: bpy.props.BoolProperty(
        name="Autodetect Threads",
        default=False
    )

    low_light_threshold: bpy.props.FloatProperty(
        name="Low Light Threshold", default=0.001, min=0.0
    )
    
    manual_device_selection: bpy.props.BoolProperty(
        name="Manual Device Selection", default=False
    )

    max_subdivisions: bpy.props.IntProperty(
        name="Max. Subdivisions", default=255
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
        name="Profile File Path",
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
        name="Render with Watermarks (Skip License Check)", default=False
    )

    stats_file: bpy.props.StringProperty(
        name="Stats File Path",
        default="$HOME/arnold_stats.json"
    )

    stochastic_volume_interpolation: bpy.props.BoolProperty(
        name="Stochastic Volume Interpolation", default=True
    )

    subdiv_dicing_camera: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Subdiv Dicing Camera",
        poll=lambda self, object: object.type == 'CAMERA'
    )

    subdiv_frustum_culling: bpy.props.BoolProperty(
        name="Frustum Culling", default=False
    )

    subdiv_frustum_padding: bpy.props.FloatProperty(
        name="Frustum Padding", default=0.0
    )

    texture_accept_unmipped: bpy.props.BoolProperty(
        name="Accept Unmipped", default=True
    )

    texture_accept_untiled: bpy.props.BoolProperty(
        name="Accept Untiled", default=True
    )

    texture_auto_generate_tx: bpy.props.BoolProperty(
        name="Auto-convert Textures to TX", default=False
    )

    texture_auto_tx_path: bpy.props.StringProperty(
        name="TX Path", default=""
    )

    texture_autotile: bpy.props.BoolProperty(
        name="Auto-tile", default=True
    )

    textre_max_memory_MB: bpy.props.FloatProperty(
        name="Max Cache Size (MB)", default=4096.0, min=0.0
    )

    texture_max_open_files: bpy.props.IntProperty(
        name="Max Open Files", default=0, min=0
    )

    texture_searchpath: bpy.props.StringProperty(
        name="Texture Search Path", default=""
    )

    texture_use_existing_tx: bpy.props.BoolProperty(
        name="Use Existing TX Textures", default=True
    )

    threads: bpy.props.IntProperty(
        name="Threads",
        default=1
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
    bpy.utils.register_class(ArnoldImager)
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
    bpy.utils.unregister_class(ArnoldImager)
    bpy.utils.unregister_class(ArnoldAovShader)
