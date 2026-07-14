import bpy


GLOBAL_SETTINGS = {
    "arnold:global:viewport_update_trigger": "viewport_update_trigger",
    "arnold:global:enable_progressive_render": "enable_progressive_render",
    "arnold:global:enable_adaptive_sampling": "enable_adaptive_sampling",
    "arnold:global:threads": "threads",
    "arnold:global:dialectric_priorities": "dialectric_priorities",
    "arnold:global:enable_aa_sample_clamp": "enable_aa_sample_clamp",
    "arnold:global:AA_sample_clamp": "AA_sample_clamp",
    "arnold:global:AA_sample_clamp_affects_aovs": "AA_sample_clamp_affects_aovs",
    "arnold:global:indirect_sample_clamp": "indirect_sample_clamp",
    "arnold:global:light_samples": "light_samples",
    "arnold:global:AA_samples": "AA_samples",
    "arnold:global:AA_samples_max": "AA_samples_max",
    "arnold:global:GI_diffuse_samples": "GI_diffuse_samples",
    "arnold:global:GI_specular_samples": "GI_specular_samples",
    "arnold:global:GI_transmission_samples": "GI_transmission_samples",
    "arnold:global:GI_sss_samples": "GI_sss_samples",
    "arnold:global:GI_volume_samples": "GI_volume_samples",
    "arnold:global:auto_transparency_depth": "auto_transparency_depth",
    "arnold:global:GI_diffuse_depth": "GI_diffuse_depth",
    "arnold:global:GI_specular_depth": "GI_specular_depth",
    "arnold:global:GI_transmission_depth": "GI_transmission_depth",
    "arnold:global:GI_volume_depth": "GI_volume_depth",
    "arnold:global:GI_total_depth": "GI_total_depth",
    "arnold:global:abort_on_error": "abort_on_error",
    "arnold:global:ignore_textures": "ignore_textures",
    "arnold:global:ignore_shaders": "ignore_shaders",
    "arnold:global:ignore_atmosphere": "ignore_atmosphere",
    "arnold:global:ignore_lights": "ignore_lights",
    "arnold:global:ignore_shadows": "ignore_shadows",
    "arnold:global:ignore_subdivision": "ignore_subdivision",
    "arnold:global:ignore_displacement": "ignore_displacement",
    "arnold:global:ignore_bump": "ignore_bump",
    "arnold:global:ignore_motion_blur": "ignore_motion_blur",
    "arnold:global:ignore_dof": "ignore_dof",
    "arnold:global:ignore_sss": "ignore_sss",
    "arnold:global:plugin_searchpath": "plugin_searchpath",
    "arnold:global:asset_searchpath": "asset_searchpath",
    "arnold:global:subdiv_dicing_camera": "subdiv_dicing_camera",
    "arnold:global:subdiv_frustum_culling": "subdiv_frustum_culling",
    "arnold:global:render_device": "render_device",
    "arnold:global:render_device_fallback": "render_device_fallback",
    "arnold:global:log_verbosity": "log_verbosity",
    "arnold:global:log_file": "log_file",
    "arnold:global:profile_file": "profile_file",
    "arnold:global:report_file": "report_file",
    "arnold:global:stats_file": "stats_file",
    "arnold:global:stochastic_volume_interpolation": "stochastic_volume_interpolation",
    "arnold:global:procedural_instancing_optimization": "procedural_instancing_optimization",
    "arnold:global:indirect_specular_blur": "indirect_specular_blur",
    "arnold:global:low_light_threshold": "low_light_threshold",
    "arnold:global:nits_per_unit": "nits_per_unit",
    "arnold:global:subdiv_frustum_padding": "subdiv_frustum_padding",
    "arnold:global:texture_max_memory_MB": "texture_max_memory_MB",
    "arnold:global:texture_max_open_files": "texture_max_open_files",
    "arnold:global:texture_automip": "texture_automip",
    "arnold:global:texture_accept_untiled": "texture_accept_untiled",
    "arnold:global:texture_autotile": "texture_autotile",
    "arnold:global:texture_accept_unmipped": "texture_accept_unmipped",
    "arnold:global:texture_auto_generate_tx": "texture_auto_generate_tx",
    "arnold:global:texture_use_existing_tx": "texture_use_existing_tx",
    "arnold:global:texture_auto_tx_path": "texture_auto_tx_path",
    "arnold:global:gpu_default_names": "gpu_default_names",
    "arnold:global:gpu_default_min_memory_MB": "gpu_default_min_memory_MB",
    "arnold:global:manual_device_selection": "manual_device_selection",
    "arnold:global:device_selection": "device_selection",
    "arnold:global:bucket_size": "bucket_size",
    "arnold:global:bucket_scanning": "bucket_scanning",
    "arnold:global:parallel_node_init": "parallel_node_init",
    "arnold:global:abort_on_license_fail": "abort_on_license_fail",
    "arnold:global:skip_license_check": "skip_license_check",
    "arnold:global:enable_report": "enable_report",
    "arnold:global:enable_stats": "enable_stats",
    "arnold:global:enable_profile": "enable_profile",
    "arnold:global:ignore_operators": "ignore_operators",
    "arnold:global:ignore_imagers": "ignore_imagers",
}


def build_global_settings(settings, is_viewport):
    result = {}

    for usd_name, prop_name in GLOBAL_SETTINGS.items():
        value = getattr(settings, prop_name)

        if prop_name == "subdiv_dicing_camera":
            result[usd_name] = value.name if value else ""
        else:
            result[usd_name] = value

    result["arnold:global:enable_gpu_rendering"] = (settings.render_device == "GPU")
    result["arnold:global:enable_progressive_render"] = (
        True if is_viewport else settings.enable_progressive_render
    )

    return result


def update_render_device(self, context):
    if context is None:
        return
    arnold = getattr(context.scene.arnold, "global", None)
    if arnold:
        arnold.viewport_update_trigger = not arnold.viewport_update_trigger
    viewport = getattr(context.scene.arnold, "viewport", None)
    if viewport:
        viewport.viewport_update_trigger = not viewport.viewport_update_trigger
    context.scene.update_tag()
    if context.scene.world:
        context.scene.world.update_tag()
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def get_device_selection_items(self, context):
    items = []
    try:
        import ctypes
        import os
        lib_path = os.path.expanduser("~/.btoa/btoa-5.2-7.4.5.1/bin/libai.so")
        if os.path.exists(lib_path):
            lib = ctypes.CDLL(lib_path)
            lib.AiDeviceGetCount.argtypes = [ctypes.c_int]
            lib.AiDeviceGetCount.restype = ctypes.c_uint
            lib.AiDeviceGetName.argtypes = [ctypes.c_int, ctypes.c_uint]
            lib.AiDeviceGetName.restype = ctypes.c_char_p

            count = lib.AiDeviceGetCount(1) # 1 = GPU
            for i in range(count):
                name_bytes = lib.AiDeviceGetName(1, i)
                name_str = name_bytes.decode('utf-8') if name_bytes else f"GPU {i}"
                items.append((f"gpu{i}", f"GPU {i}: {name_str}", ""))
    except BaseException:
        pass

    if not items:
        items = [("gpu0", "GPU 0", "")]
    return items


class ArnoldGlobalRenderProperties(bpy.types.PropertyGroup):

    ### Sampling

    #### Samples

    AA_samples: bpy.props.IntProperty(
        name="Camera (AA)",
        description="Anti-aliasing (AA) sample rate. Controls the number of rays per pixel from the camera",
        default=3, soft_min=0, soft_max=1020
    )

    GI_diffuse_samples: bpy.props.IntProperty(
        name="Diffuse",
        description="Controls the number of rays used for calculating indirect diffuse (GI) lighting",
        default=2, soft_min=0, soft_max=100
    )

    GI_specular_samples: bpy.props.IntProperty(
        name="Specular",
        description="Controls the number of rays used for calculating indirect specular (glossy reflection) lighting",
        default=2, soft_min=0, soft_max=100
    )

    GI_transmission_samples: bpy.props.IntProperty(
        name="Transmission",
        description="Controls the number of rays used for calculating transmission (refraction) lighting",
        default=2, soft_min=0, soft_max=100
    )

    GI_sss_samples: bpy.props.IntProperty(
        name="SSS",
        description="Controls the number of rays used for calculating subsurface scattering (SSS) lighting",
        default=2, soft_min=0, soft_max=100
    )

    GI_volume_samples: bpy.props.IntProperty(
        name="Volume Indirect",
        description="Controls the number of rays used for calculating volume indirect lighting",
        default=2, soft_min=0, soft_max=100
    )

    enable_progressive_render: bpy.props.BoolProperty(
        name="Progressive Render",
        description="Enable progressive rendering mode",
        default=False
    )

    #### Adaptive Sampling

    enable_adaptive_sampling: bpy.props.BoolProperty(
        name="Enable Adaptive Sampling",
        description="Enable adaptive AA sampling",
        default=False
    )

    AA_adaptive_threshold: bpy.props.FloatProperty(
        name="Adaptive Threshold",
        description="Determines the threshold at which adaptive sampling is terminated",
        default=0.15, soft_min=0.0, soft_max=1.0
    )

    AA_samples_max: bpy.props.IntProperty(
        name="Max. Camera (AA)",
        description="The maximum AA samples allowed when adaptive sampling is active",
        default=20, soft_min=0, soft_max=1020
    )

    #### Clamping

    AA_sample_clamp_affects_aovs: bpy.props.BoolProperty(
        name="AA Sample Clamp Affects AOVs",
        description="Apply AA clamping to all color AOVs",
        default=False
    )

    AA_sample_clamp: bpy.props.FloatProperty(
        name="AA Sample Clamp",
        description="Clamp the value of AA samples to this maximum",
        default=1e+30, soft_min=0.0, soft_max=100.0
    )

    enable_aa_sample_clamp: bpy.props.BoolProperty(
        name="Enable AA Sample Clamp",
        description="Toggle clamping of AA samples",
        default=False
    )

    indirect_sample_clamp: bpy.props.FloatProperty(
        name="Indirect Sample Clamp",
        description="Clamp the value of indirect samples to this maximum to reduce fireflies",
        default=10.0, soft_min=0.0, soft_max=100.0
    )

    ### Advanced

    AA_seed: bpy.props.IntProperty(
        name="AA Seed",
        description="A seed value for the pseudorandom sample pattern generator",
        default=1, soft_min=0, soft_max=10
    )

    stochastic_volume_interpolation: bpy.props.BoolProperty(
        name="Stochastic Volume Interpolation",
        description="Enable stochastic sampling of volume interpolation nodes",
        default=True
    )

    procedural_instancing_optimization: bpy.props.EnumProperty(
        name="Procedural Instancing Optimization",
        description="Optimization strategy for instancing procedurals",
        items=[
            ("none",        "None",        ""),
            ("conservative","Conservative",""),
            ("exhaustive",  "Exhaustive",  "")
        ],
        default="conservative"
    )

    dialectric_priorities: bpy.props.BoolProperty(
        name="Nested Dielectrics",
        description="Enable nested dielectrics priorities",
        default=True
    )

    indirect_specular_blur: bpy.props.FloatProperty(
        name="Indirect Specular Blur",
        description="Blur indirect specular reflections to reduce noise",
        default=1.0, soft_min=0.0, soft_max=2.0
    )

    ### Ray Depth

    GI_total_depth: bpy.props.IntProperty(
        name="Total",
        description="Maximum total ray depth (diffuse + specular + transmission + volume)",
        default=10, soft_min=0, soft_max=100
    )

    GI_diffuse_depth: bpy.props.IntProperty(
        name="Diffuse",
        description="Maximum diffuse ray bounces",
        default=1, soft_min=0, soft_max=100
    )

    GI_specular_depth: bpy.props.IntProperty(
        name="Specular",
        description="Maximum specular ray bounces",
        default=1, soft_min=0, soft_max=100
    )

    GI_transmission_depth: bpy.props.IntProperty(
        name="Transmission",
        description="Maximum transmission ray bounces",
        default=8, soft_min=0, soft_max=100
    )

    GI_volume_depth: bpy.props.IntProperty(
        name="Volume",
        description="Maximum volume indirect ray bounces",
        default=0, soft_min=0, soft_max=100
    )

    auto_transparency_depth: bpy.props.IntProperty(
        name="Auto Transp. Depth",
        description="The number of transparent bounces before transparency is ignored",
        default=10, soft_min=0, soft_max=16
    )

    ### Lights

    light_samples: bpy.props.IntProperty(
        name="Light Samples",
        description="Overrides the samples parameter for all lights in the scene",
        default=4, soft_min=0, soft_max=1024
    )

    low_light_threshold: bpy.props.FloatProperty(
        name="Low Light Threshold",
        description="Rays below this luminance value are ignored to optimize speed",
        default=0.001, soft_min=0.0, soft_max=1.0
    )

    nits_per_unit: bpy.props.FloatProperty(
        name="Nits Per Unit",
        description="Specifies the physical brightness scale in nits",
        default=1000.0, soft_min=0.0, soft_max=10000.0
    )

    ### Subdivision

    subdiv_dicing_camera: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Subdiv Dicing Camera",
        description="Camera used for subdiv dicing calculations",
        poll=lambda self, object: object.type == 'CAMERA'
    )

    subdiv_frustum_culling: bpy.props.BoolProperty(
        name="Frustum Culling",
        description="Enable subdiv dicing frustum culling",
        default=False
    )

    subdiv_frustum_padding: bpy.props.FloatProperty(
        name="Frustum Padding",
        description="Padding size for frustum culling boundary",
        default=0.0, soft_min=0.0, soft_max=10.0
    )

    ### Texture

    texture_max_memory_MB: bpy.props.FloatProperty(
        name="Cache Size (MB)",
        description="Maximum memory allowed for the texture cache in megabytes",
        default=4096.0, soft_min=0.0, soft_max=16384.0
    )

    texture_max_open_files: bpy.props.IntProperty(
        name="Max Open Textures",
        description="Maximum number of texture files that can be kept open at once",
        default=0, soft_min=0, soft_max=1024
    )

    texture_automip: bpy.props.BoolProperty(
        name="Auto-mipmap",
        description="Automatically generate mipmaps for textures if missing",
        default=True
    )

    texture_accept_untiled: bpy.props.BoolProperty(
        name="Accept Untiled",
        description="Accept textures that are not tiled",
        default=True
    )

    texture_autotile: bpy.props.IntProperty(
        name="Auto-tile",
        description="Automatically tile textures of size greater than this value (in pixels)",
        default=0, soft_min=0, soft_max=64
    )

    texture_accept_unmipped: bpy.props.BoolProperty(
        name="Accept Unmipped",
        description="Accept textures that do not have mipmaps",
        default=True
    )

    texture_auto_generate_tx: bpy.props.BoolProperty(
        name="Auto Generate Tx",
        description="Auto-generate .tx files from source textures",
        default=True
    )

    texture_use_existing_tx: bpy.props.BoolProperty(
        name="Use Existing Tx",
        description="Use existing .tx files if they exist",
        default=True
    )

    texture_auto_tx_path: bpy.props.StringProperty(
        name="Auto-Tx Path",
        description="Output folder for auto-generated .tx textures",
        default=""
    )

    ### Device

    render_device: bpy.props.EnumProperty(
        name="Render Device",
        description="Select render device (CPU or GPU)",
        items=[
            ("CPU", "CPU", "Use CPU for rendering"),
            ("GPU", "GPU", "Use GPU for rendering")
        ],
        default="CPU",
        update=update_render_device
    )

    render_device_fallback: bpy.props.EnumProperty(
        name="Render Device Fallback",
        description="Behavior if GPU rendering fails (Abort or Fallback to CPU)",
        items=[
            ("error", "Error", "Abort on error if GPU rendering fails"),
            ("CPU",   "CPU",   "Fallback to CPU if GPU rendering fails")
        ],
        default="error"
    )

    gpu_default_names: bpy.props.StringProperty(
        name="Device Expression",
        description="Device string expression to select GPU devices",
        default="*"
    )

    gpu_default_min_memory_MB: bpy.props.IntProperty(
        name="Min. Memory (MB)",
        description="Minimum GPU memory required to render",
        default=512, soft_min=0, soft_max=65536
    )

    manual_device_selection: bpy.props.BoolProperty(
        name="Manual Device Selection",
        description="Manually select which GPU devices to use",
        default=False
    )

    device_selection: bpy.props.EnumProperty(
        name="Device Selection",
        description="Explicit GPU device to use for rendering when manual device selection is enabled",
        items=get_device_selection_items
    )
    ### System

    threads: bpy.props.IntProperty(
        name="Threads",
        description="Explicit number of threads to use for rendering",
        default=0, soft_min=0, soft_max=256
    )

    bucket_size: bpy.props.IntProperty(
        name="Bucket Size",
        description="Size of the image buckets used for rendering (in pixels)",
        default=64, soft_min=0, soft_max=256
    )

    bucket_scanning: bpy.props.EnumProperty(
        name="Bucket Scanning",
        description="Scanning pattern order used for rendering buckets",
        items=[
            ("top",     "Top",     ""),
            ("left",    "Left",    ""),
            ("random",  "Random",  ""),
            ("spiral",  "Spiral",  ""),
            ("hilbert", "Hilbert", ""),
            ("list",    "List",    "")
        ],
        default="spiral"
    )

    parallel_node_init: bpy.props.BoolProperty(
        name="Parallel Node Init",
        description="Enable parallel initialization of scene nodes",
        default=True
    )

    abort_on_error: bpy.props.BoolProperty(
        name="Abort On Error",
        description="Abort rendering immediately if an error is encountered",
        default=True
    )

    abort_on_license_fail: bpy.props.BoolProperty(
        name="Abort On License Fail",
        description="Abort rendering immediately if an Arnold license is not found",
        default=False
    )

    skip_license_check: bpy.props.BoolProperty(
        name="Skip License Check",
        description="Do not check for Arnold licenses (renders with a watermark)",
        default=False
    )

    plugin_searchpath: bpy.props.StringProperty(
        name="Plugin Search Path",
        description="Folder paths to search for Arnold plugin shaders",
        default=""
    )

    asset_searchpath: bpy.props.StringProperty(
        name="Asset Search Path",
        description="Folder paths to search for assets (textures, procedurals, etc.)",
        default=""
    )
    
    ### Diagnostics

    log_file: bpy.props.StringProperty(
        name="Log File",
        description="Output file path to save render log messages",
        default=""
    )

    log_verbosity: bpy.props.IntProperty(
        name="Log Verbosity",
        description="Verbosity level for log messages (0 = none, 5 = maximum)",
        default=2, soft_min=0, soft_max=5
    )

    enable_report: bpy.props.BoolProperty(
        name="Enable HTML Report",
        description="Generate an HTML summary report of the render",
        default=False
    )

    report_file: bpy.props.StringProperty(
        name="HTML Report File",
        description="Output file path to save the HTML report",
        default="//arnold_report.html"
    )

    enable_stats: bpy.props.BoolProperty(
        name="Enable Stats",
        description="Collect and output render statistics",
        default=False
    )

    stats_file: bpy.props.StringProperty(
        name="Stats File",
        description="Output file path to save render statistics (JSON)",
        default="//arnold_stats.json"
    )

    enable_profile: bpy.props.BoolProperty(
        name="Enable Profile",
        description="Collect and output profile performance trace data",
        default=False
    )

    profile_file: bpy.props.StringProperty(
        name="Profile File",
        description="Output file path to save profile performance trace data (JSON)",
        default="//arnold_profile.json"
    )

    ### Ignore flags

    ignore_operators: bpy.props.BoolProperty(
        name="Ignore Operators",
        description="Ignore Arnold operators during render",
        default=False
    )

    ignore_imagers: bpy.props.BoolProperty(
        name="Ignore Imagers",
        description="Ignore post-processing imagers during render",
        default=False
    )

    ignore_textures: bpy.props.BoolProperty(
        name="Ignore Textures",
        description="Ignore texture maps during render",
        default=False
    )

    ignore_shaders: bpy.props.BoolProperty(
        name="Ignore Shaders",
        description="Ignore surface shaders (renders flat color) during render",
        default=False
    )

    ignore_atmosphere: bpy.props.BoolProperty(
        name="Ignore Atmosphere",
        description="Ignore atmospheric effects during render",
        default=False
    )

    ignore_lights: bpy.props.BoolProperty(
        name="Ignore Lights",
        description="Ignore all light sources during render",
        default=False
    )

    ignore_shadows: bpy.props.BoolProperty(
        name="Ignore Shadows",
        description="Ignore shadow calculations during render",
        default=False
    )

    ignore_subdivision: bpy.props.BoolProperty(
        name="Ignore Subdivision",
        description="Ignore subdivision surfaces (renders base meshes) during render",
        default=False
    )

    ignore_displacement: bpy.props.BoolProperty(
        name="Ignore Displacement",
        description="Ignore displacement maps during render",
        default=False
    )

    ignore_bump: bpy.props.BoolProperty(
        name="Ignore Bump",
        description="Ignore bump maps during render",
        default=False
    )

    ignore_motion_blur: bpy.props.BoolProperty(
        name="Ignore Motion Blur",
        description="Ignore motion blur calculations during render",
        default=False
    )

    ignore_dof: bpy.props.BoolProperty(
        name="Ignore Depth of Field",
        description="Ignore depth of field calculations during render",
        default=False
    )

    ignore_sss: bpy.props.BoolProperty(
        name="Ignore SSS",
        description="Ignore subsurface scattering (SSS) calculations during render",
        default=False
    )

    ### Misc

    viewport_update_trigger: bpy.props.BoolProperty(
        name="Viewport Update Trigger",
        description="Internal trigger property to refresh the viewport render session",
        default=False,
        options={'HIDDEN'},
    )


class ArnoldRenderProperties(bpy.types.PropertyGroup):
    viewport: bpy.props.PointerProperty(type=ArnoldGlobalRenderProperties)


ArnoldRenderProperties.__annotations__['global'] = bpy.props.PointerProperty(
    type=ArnoldGlobalRenderProperties
)

register_classes, unregister_classes = bpy.utils.register_classes_factory([ArnoldGlobalRenderProperties, ArnoldRenderProperties])


def _add_seed_driver():
    scene = bpy.context.scene

    if not scene:
        return
    
    try:
        fcurve = scene.driver_add("arnold.global.AA_seed")
    except (TypeError, ValueError):
        return
    
    fcurve.driver.expression = "frame"


def register():
    register_classes()

    if not hasattr(bpy.types.Scene, "arnold"):
        bpy.types.Scene.arnold = bpy.props.PointerProperty(
            type=ArnoldRenderProperties
        )

        bpy.app.timers.register(_add_seed_driver, first_interval=0.1)


def unregister():
    if hasattr(bpy.types.Scene, "arnold"):
        del bpy.types.Scene.arnold

    unregister_classes()
