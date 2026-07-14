import bpy

# ---------------------------------------------------------------------------
# Filter type constants
# ---------------------------------------------------------------------------

# Filters that only take a width param
_FILTERS_WIDTH = [
    ("blackman_harris_filter", "Blackman-Harris", ""),
    ("gaussian_filter",        "Gaussian",        ""),
    ("contour_filter",         "Contour",         ""),
    ("sinc_filter",            "Sinc",            ""),
    ("triangle_filter",        "Triangle",        ""),
]

# Filters with no extra params
_FILTERS_SIMPLE = [
    ("box_filter",      "Box",      ""),
    ("catmullrom_filter", "Catrom", ""),
    ("closest_filter",  "Closest",  ""),
    ("farthest_filter", "Farthest", ""),
    ("heatmap_filter",  "Heatmap",  ""),
    ("mitchell_filter", "Mitnet",   ""),
]

# Composite filters
_FILTERS_COMPOSITE = [
    ("diff_filter",         "Diff",         ""),
    ("cryptomatte_filter",  "Cryptomatte",  ""),
    ("variance_filter",     "Variance",     ""),
]

FILTER_ITEMS = _FILTERS_WIDTH + _FILTERS_SIMPLE + _FILTERS_COMPOSITE

# Items for the nested filter_weights sub-selector (diff / variance)
FILTER_WEIGHT_ITEMS = [
    ("blackman_harris_filter", "Blackman-Harris", ""),
    ("box_filter",             "Box",             ""),
    ("catmullrom_filter",      "Catrom",          ""),
    ("gaussian_filter",        "Gaussian",        ""),
    ("mitchell_filter",        "Mitnet",          ""),
    ("sinc_filter",            "Sinc",            ""),
    ("triangle_filter",        "Triangle",        ""),
]

# Items for the cryptomatte sub-filter selector
CRYPTOMATTE_FILTER_ITEMS = [
    ("box_filter",             "Box",            ""),
    ("triangle_filter",        "Triangle",       ""),
    ("catmullrom_filter",      "Catrom",         ""),
    ("mitchell_filter",        "Mitnet",         ""),
    ("gaussian_filter",        "Gaussian",       ""),
    ("sinc_filter",            "Sinc",           ""),
    ("blackman_harris_filter", "Blackman-Harris",""),
    ("disk_filter",            "Disk",           ""),
    ("cone_filter",            "Cone",           ""),
]

# Helpers
FILTERS_WITH_WIDTH = {f[0] for f in _FILTERS_WIDTH} | {
    "diff_filter", "cryptomatte_filter", "variance_filter"
}
FILTERS_COMPOSITE = {f[0] for f in _FILTERS_COMPOSITE}

# ---------------------------------------------------------------------------
# BUILTIN_AOVS — (internal_name, blender_label, default_filter, default_fmt)
# ---------------------------------------------------------------------------

BUILTIN_AOVS = {
    "Beauty": [
        ("RGBA",  "Combined",           "box_filter",     "float"),
    ],
    "Utility": [
        ("A",            "Alpha",            "box_filter",     "float"),
        ("Z",            "Depth",            "closest_filter", "float"),
        ("Z_Back",       "Depth_Back",       "closest_filter", "float"),
        ("P",            "Position",         "closest_filter", "float"),
        ("Pref",         "Reference_Pos",    "closest_filter", "float"),
        ("N",            "Normal",           "closest_filter", "float"),
        ("N_Denoise",    "Normal_Denoise",   "closest_filter", "float"),
        ("Opacity",      "Opacity",          "box_filter",     "float"),
        ("Motion_Vector","Motion_Vector",    "box_filter",     "float"),
    ],
    "Lighting": [
        ("Diffuse_Direct",       "Diffuse_Direct",       "box_filter", "float"),
        ("Diffuse_Indirect",     "Diffuse_Indirect",     "box_filter", "float"),
        ("Diffuse_Albedo",       "Diffuse_Albedo",       "box_filter", "float"),
        ("Specular_Direct",      "Specular_Direct",      "box_filter", "float"),
        ("Specular_Indirect",    "Specular_Indirect",    "box_filter", "float"),
        ("Specular_Albedo",      "Specular_Albedo",      "box_filter", "float"),
        ("Coat_Direct",          "Coat_Direct",          "box_filter", "float"),
        ("Coat_Indirect",        "Coat_Indirect",        "box_filter", "float"),
        ("Coat_Albedo",          "Coat_Albedo",          "box_filter", "float"),
        ("Sheen_Direct",         "Sheen_Direct",         "box_filter", "float"),
        ("Sheen_Indirect",       "Sheen_Indirect",       "box_filter", "float"),
        ("Sheen_Albedo",         "Sheen_Albedo",         "box_filter", "float"),
        ("SSS_Direct",           "SSS_Direct",           "box_filter", "float"),
        ("SSS_Indirect",         "SSS_Indirect",         "box_filter", "float"),
        ("SSS_Albedo",           "SSS_Albedo",           "box_filter", "float"),
        ("Transmission_Direct",  "Transmission_Direct",  "box_filter", "float"),
        ("Transmission_Indirect","Transmission_Indirect","box_filter", "float"),
        ("Transmission_Albedo",  "Transmission_Albedo",  "box_filter", "float"),
        ("Volume_Direct",        "Volume_Direct",        "box_filter", "float"),
        ("Volume_Indirect",      "Volume_Indirect",      "box_filter", "float"),
        ("Volume_Albedo",        "Volume_Albedo",        "box_filter", "float"),
        ("Volume_Opacity",       "Volume_Opacity",       "box_filter", "float"),
        ("Volume_Z",             "Volume_Depth",         "closest_filter", "float"),
        ("Shadow_Matte",         "Shadow_Matte",         "box_filter", "float"),
        ("Denoise_Albedo",       "Denoise_Albedo",       "box_filter", "float"),
    ],
    "Debug": [
        ("ID",            "ID",            "closest_filter", "int"),
        ("Object",        "Object",        "closest_filter", "int"),
        ("Shader",        "Shader",        "closest_filter", "int"),
        ("CPU_Time",      "CPU_Time",      "box_filter",     "float"),
        ("Ray_Count",     "Ray_Count",     "box_filter",     "float"),
        ("AA_Inv_Density","AA_Inv_Density","box_filter",     "float"),
    ],
}

# Flat list for easy iteration
_ALL_BUILTIN_AOVS = [entry for aovs in BUILTIN_AOVS.values() for entry in aovs]

# ---------------------------------------------------------------------------
# update callback for render device restart
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# ArnoldAovFilter — reusable filter property group
# ---------------------------------------------------------------------------

class ArnoldAovFilter(bpy.types.PropertyGroup):
    type: bpy.props.EnumProperty(
        name="Filter",
        items=FILTER_ITEMS,
        default="box_filter",
    )

    width: bpy.props.FloatProperty(
        name="Width",
        description="Filter kernel width",
        default=2.0, min=0.01, soft_max=10.0,
    )

    # --- diff / variance ---
    filter_weights: bpy.props.EnumProperty(
        name="Filter Weights",
        items=FILTER_WEIGHT_ITEMS,
        default="gaussian_filter",
    )

    # --- variance ---
    scalar_mode: bpy.props.BoolProperty(
        name="Scalar Mode",
        default=False,
    )

    # --- cryptomatte ---
    sub_filter: bpy.props.EnumProperty(
        name="Sub-Filter",
        items=CRYPTOMATTE_FILTER_ITEMS,
        default="box_filter",
    )

    noop: bpy.props.BoolProperty(
        name="No-op",
        description="Do not filter — pass through samples unchanged",
        default=False,
    )

    source_filter: bpy.props.StringProperty(
        name="Source Filter",
        default="",
    )


# ---------------------------------------------------------------------------
# ArnoldCustomRenderVar — user-defined AOV
# ---------------------------------------------------------------------------

class ArnoldCustomRenderVar(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="")

    source_name: bpy.props.StringProperty(
        name="Source",
        description="Arnold AOV source name",
        default="",
    )

    source_type: bpy.props.EnumProperty(
        name="Source Type",
        items=[
            ("raw",     "Raw",     ""),
            ("lpe",     "LPE",     ""),
            ("primvar", "Primvar", ""),
        ],
        default="raw",
    )

    data_type: bpy.props.EnumProperty(
        name="Data Type",
        items=[
            ("color4f", "RGBA (color4f)", ""),
            ("color3f", "RGB (color3f)",  ""),
            ("float3",  "Vector (float3)",""),
            ("float",   "Float",          ""),
            ("int",     "Int",            ""),
        ],
        default="color3f",
    )

    format: bpy.props.EnumProperty(
        name="Precision",
        items=[
            ("float", "Full (32-bit)",  ""),
            ("half",  "Half (16-bit)",  ""),
        ],
        default="float",
    )

    filter: bpy.props.PointerProperty(type=ArnoldAovFilter)


# ---------------------------------------------------------------------------
# ArnoldGlobalRenderProperties
# ---------------------------------------------------------------------------

class ArnoldGlobalRenderProperties(bpy.types.PropertyGroup):

    ### Sampling

    #### Samples

    AA_samples: bpy.props.IntProperty(
        name="Camera (AA)",
        default=3, min=0, soft_max=1020
    )

    GI_diffuse_samples: bpy.props.IntProperty(
        name="Diffuse",
        default=2, min=0, soft_max=100
    )

    GI_specular_samples: bpy.props.IntProperty(
        name="Specular",
        default=2, min=0, soft_max=100
    )

    GI_transmission_samples: bpy.props.IntProperty(
        name="Transmission",
        default=2, min=0, soft_max=100
    )

    GI_sss_samples: bpy.props.IntProperty(
        name="SSS",
        default=2, min=0, soft_max=100
    )

    GI_volume_samples: bpy.props.IntProperty(
        name="Volume Indirect",
        default=2, min=0, soft_max=100
    )

    enable_progressive_render: bpy.props.BoolProperty(
        name="Progressive Render",
        default=False
    )

    #### Adaptive Sampling

    enable_adaptive_sampling: bpy.props.BoolProperty(
        name="Enable Adaptive Sampling",
        default=False
    )

    AA_adaptive_threshold: bpy.props.FloatProperty(
        name="Adaptive Threshold",
        default=0.15, min=0.0, max=1.0
    )

    AA_samples_max: bpy.props.IntProperty(
        name="Max. Camera (AA)",
        default=20, min=0, soft_max=1020
    )

    #### Clamping

    AA_sample_clamp_affects_aovs: bpy.props.BoolProperty(
        name="AA Sample Clamp Affects AOVs",
        default=False
    )

    AA_sample_clamp: bpy.props.FloatProperty(
        name="AA Sample Clamp",
        default=1e+30, min=0.0, soft_max=100.0
    )

    enable_aa_sample_clamp: bpy.props.BoolProperty(
        name="Enable AA Sample Clamp",
        default=False
    )

    indirect_sample_clamp: bpy.props.FloatProperty(
        name="Indirect Sample Clamp", default=10.0, min=0.0, soft_max=100.0
    )

    ### Advanced

    AA_seed: bpy.props.IntProperty(
        name="AA Seed",
        default=1, min=0, soft_max=10
    )

    stochastic_volume_interpolation: bpy.props.BoolProperty(
        name="Stochastic Volume Interpolation", default=True
    )

    procedural_instancing_optimization: bpy.props.EnumProperty(
        name="Procedural Instancing Optimization",
        items=[
            ("none",        "None",        ""),
            ("conservative","Conservative",""),
            ("exhaustive",  "Exhaustive",  "")
        ],
        default="conservative"
    )

    dialectric_priorities: bpy.props.BoolProperty(
        name="Nested Dielectrics",
        default=True
    )

    indirect_specular_blur: bpy.props.FloatProperty(
        name="Indirect Specular Blur", default=1.0, min=0.0, soft_max=2.0
    )

    ### Ray Depth

    GI_total_depth: bpy.props.IntProperty(
        name="Total",
        default=10, min=0, soft_max=100
    )

    GI_diffuse_depth: bpy.props.IntProperty(
        name="Diffuse",
        default=1, min=0, soft_max=100
    )

    GI_specular_depth: bpy.props.IntProperty(
        name="Specular",
        default=1, min=0, soft_max=100
    )

    GI_transmission_depth: bpy.props.IntProperty(
        name="Transmission",
        default=8, min=0, soft_max=100
    )

    GI_volume_depth: bpy.props.IntProperty(
        name="Volume",
        default=0, min=0, soft_max=100
    )

    auto_transparency_depth: bpy.props.IntProperty(
        name="Auto Transp. Depth",
        default=10, min=0, soft_max=16
    )

    ### Lights

    light_samples: bpy.props.IntProperty(
        name="Light Samples", default=4, min=0, soft_max=1024
    )

    enable_light_samples: bpy.props.BoolProperty(
        name="Enable Light Samples", default=False
    )

    low_light_threshold: bpy.props.FloatProperty(
        name="Low Light Threshold", default=0.001, min=0.0, max=1.0
    )

    nits_per_unit: bpy.props.FloatProperty(
        name="Nits Per Unit", default=1000.0, min=0.0, soft_max=10000.0
    )

    ### Subdivision

    subdiv_dicing_camera: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Subdiv Dicing Camera",
        poll=lambda self, object: object.type == 'CAMERA'
    )

    subdiv_frustum_culling: bpy.props.BoolProperty(
        name="Frustum Culling", default=False
    )

    subdiv_frustum_padding: bpy.props.FloatProperty(
        name="Frustum Padding", default=0.0, min=0.0, soft_max=10.0
    )

    ### Texture

    texture_max_memory_MB: bpy.props.FloatProperty(
        name="Cache Size (MB)", default=4096.0, min=0.0, soft_max=16384.0
    )

    texture_max_open_files: bpy.props.IntProperty(
        name="Max Open Textures", default=0, min=0, soft_max=1024
    )

    texture_automip: bpy.props.BoolProperty(
        name="Auto-mipmap", default=True
    )

    texture_accept_untiled: bpy.props.BoolProperty(
        name="Accept Untiled", default=True
    )

    texture_autotile: bpy.props.IntProperty(
        name="Auto-tile", default=0, min=0, soft_max=64
    )

    texture_accept_unmipped: bpy.props.BoolProperty(
        name="Accept Unmipped", default=True
    )

    texture_auto_generate_tx: bpy.props.BoolProperty(
        name="Auto Generate Tx", default=True
    )

    texture_use_existing_tx: bpy.props.BoolProperty(
        name="Use Existing Tx", default=True
    )

    texture_auto_tx_path: bpy.props.StringProperty(
        name="Auto-Tx Path", default=""
    )

    texture_searchpath: bpy.props.StringProperty(
        name="Texture Search Path", default=""
    )

    ### Device

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
            ("CPU",   "CPU",   "Fallback to CPU if GPU rendering fails")
        ],
        default="error"
    )

    gpu_default_names: bpy.props.StringProperty(
        name="Device Expression",
        default="*"
    )

    gpu_default_min_memory_MB: bpy.props.IntProperty(
        name="Min. Memory (MB)",
        default=512, min=0, soft_max=65536
    )

    manual_device_selection: bpy.props.BoolProperty(
        name="Manual Device Selection", default=False
    )

    device_selection: bpy.props.StringProperty(
        name="Device Selection",
        default="gpu0"
    )

    autodetect_threads: bpy.props.BoolProperty(
        name="Auto-detect Threads", default=True
    )

    ### System

    threads: bpy.props.IntProperty(
        name="Threads",
        default=0, min=0, soft_max=256
    )

    bucket_size: bpy.props.IntProperty(
        name="Bucket Size",
        default=64, min=0, soft_max=256
    )

    bucket_scanning: bpy.props.EnumProperty(
        name="Bucket Scanning",
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
        name="Parallel Node Init", default=True
    )

    abort_on_error: bpy.props.BoolProperty(
        name="Abort On Error",
        default=True
    )

    abort_on_license_fail: bpy.props.BoolProperty(
        name="Abort On License Fail",
        default=False
    )

    skip_license_check: bpy.props.BoolProperty(
        name="Skip License Check", default=False
    )

    plugin_searchpath: bpy.props.StringProperty(
        name="Plugin Search Path", default=""
    )

    asset_searchpath: bpy.props.StringProperty(
        name="Asset Search Path",
        default=""
    )

    osl_includepath: bpy.props.StringProperty(
        name="OSL Include Path", default=""
    )

    ### Diagnostics

    log_file: bpy.props.StringProperty(
        name="Log File",
        default=""
    )

    log_verbosity: bpy.props.IntProperty(
        name="Log Verbosity",
        default=2, min=0, max=5
    )

    enable_report: bpy.props.BoolProperty(
        name="Enable HTML Report",
        default=False
    )

    report_file: bpy.props.StringProperty(
        name="HTML Report File",
        default="//arnold_report.html"
    )

    enable_stats: bpy.props.BoolProperty(
        name="Enable Stats",
        default=False
    )

    stats_file: bpy.props.StringProperty(
        name="Stats File",
        default="//arnold_stats.json"
    )

    enable_profile: bpy.props.BoolProperty(
        name="Enable Profile",
        default=False
    )

    profile_file: bpy.props.StringProperty(
        name="Profile File",
        default="//arnold_profile.json"
    )

    ### Ignore flags

    ignore_operators: bpy.props.BoolProperty(
        name="Ignore Operators", default=False
    )

    ignore_imagers: bpy.props.BoolProperty(
        name="Ignore Imagers", default=False
    )

    ignore_textures: bpy.props.BoolProperty(
        name="Ignore Textures", default=False
    )

    ignore_shaders: bpy.props.BoolProperty(
        name="Ignore Shaders", default=False
    )

    ignore_atmosphere: bpy.props.BoolProperty(
        name="Ignore Atmosphere", default=False
    )

    ignore_lights: bpy.props.BoolProperty(
        name="Ignore Lights", default=False
    )

    ignore_shadows: bpy.props.BoolProperty(
        name="Ignore Shadows", default=False
    )

    ignore_subdivision: bpy.props.BoolProperty(
        name="Ignore Subdivision", default=False
    )

    ignore_displacement: bpy.props.BoolProperty(
        name="Ignore Displacement", default=False
    )

    ignore_bump: bpy.props.BoolProperty(
        name="Ignore Bump", default=False
    )

    ignore_motion_blur: bpy.props.BoolProperty(
        name="Ignore Motion Blur", default=False
    )

    ignore_dof: bpy.props.BoolProperty(
        name="Ignore Depth of Field", default=False
    )

    ignore_sss: bpy.props.BoolProperty(
        name="Ignore SSS", default=False
    )

    ignore_smoothing: bpy.props.BoolProperty(
        name="Ignore Smoothing", default=False
    )

    ### Misc

    viewport_update_trigger: bpy.props.BoolProperty(
        name="Viewport Update Trigger",
        default=False,
        options={'HIDDEN'},
    )

    ### Custom render vars

    custom_render_vars: bpy.props.CollectionProperty(
        type=ArnoldCustomRenderVar,
        name="Custom AOVs",
    )

    custom_render_vars_index: bpy.props.IntProperty(
        name="Active Custom AOV",
        default=0,
    )


# ---------------------------------------------------------------------------
# Inject per-built-in AOV properties after class definition
# (avoids hundreds of manual annotations while keeping the class body clean)
# ---------------------------------------------------------------------------

_FORMAT_ITEMS = [
    ("float", "Full (32-bit)", ""),
    ("half",  "Half (16-bit)", ""),
    ("int",   "Integer",       ""),
]

for _name, _label, _def_filt, _def_fmt in _ALL_BUILTIN_AOVS:
    _default_enabled = (_name == "RGBA")

    ArnoldGlobalRenderProperties.__annotations__[f"aov_{_name}_enabled"] = (
        bpy.props.BoolProperty(
            name=_label,
            description=f"Enable {_label} AOV pass",
            default=_default_enabled,
        )
    )

    ArnoldGlobalRenderProperties.__annotations__[f"aov_{_name}_format"] = (
        bpy.props.EnumProperty(
            name="Format",
            items=_FORMAT_ITEMS,
            default=_def_fmt if _def_fmt in {"float", "half", "int"} else "float",
        )
    )

    # --- flat filter properties (avoids PointerProperty resolution issues) ---
    ArnoldGlobalRenderProperties.__annotations__[f"aov_{_name}_filter_type"] = (
        bpy.props.EnumProperty(
            name="Filter",
            items=FILTER_ITEMS,
            default=_def_filt,
        )
    )
    ArnoldGlobalRenderProperties.__annotations__[f"aov_{_name}_filter_width"] = (
        bpy.props.FloatProperty(name="Width", default=2.0, min=0.01, soft_max=10.0)
    )
    ArnoldGlobalRenderProperties.__annotations__[f"aov_{_name}_filter_weights"] = (
        bpy.props.EnumProperty(
            name="Filter Weights", items=FILTER_WEIGHT_ITEMS, default="gaussian_filter"
        )
    )
    ArnoldGlobalRenderProperties.__annotations__[f"aov_{_name}_filter_scalar_mode"] = (
        bpy.props.BoolProperty(name="Scalar Mode", default=False)
    )
    ArnoldGlobalRenderProperties.__annotations__[f"aov_{_name}_filter_sub_filter"] = (
        bpy.props.EnumProperty(
            name="Sub-Filter", items=CRYPTOMATTE_FILTER_ITEMS, default="box_filter"
        )
    )
    ArnoldGlobalRenderProperties.__annotations__[f"aov_{_name}_filter_noop"] = (
        bpy.props.BoolProperty(name="No-op", default=False)
    )
    ArnoldGlobalRenderProperties.__annotations__[f"aov_{_name}_filter_source_filter"] = (
        bpy.props.StringProperty(name="Source Filter", default="")
    )


# ---------------------------------------------------------------------------
# ArnoldRenderProperties (top-level scene pointer)
# ---------------------------------------------------------------------------

class ArnoldRenderProperties(bpy.types.PropertyGroup):
    viewport: bpy.props.PointerProperty(type=ArnoldGlobalRenderProperties)

ArnoldRenderProperties.__annotations__['global'] = bpy.props.PointerProperty(
    type=ArnoldGlobalRenderProperties
)


# ---------------------------------------------------------------------------
# Registration helpers
# ---------------------------------------------------------------------------

def _add_seed_driver():
    scene = getattr(bpy.context, "scene", None)
    if scene:
        try:
            driver_fcurve = scene.driver_add('arnold.global.AA_seed')
            driver_fcurve.driver.expression = "frame"
        except Exception:
            pass
    return None


def register():
    bpy.utils.register_class(ArnoldAovFilter)
    bpy.utils.register_class(ArnoldCustomRenderVar)
    bpy.utils.register_class(ArnoldGlobalRenderProperties)
    bpy.utils.register_class(ArnoldRenderProperties)

    if not hasattr(bpy.types.Scene, "arnold"):
        bpy.types.Scene.arnold = bpy.props.PointerProperty(
            type=ArnoldRenderProperties
        )

        bpy.app.timers.register(_add_seed_driver, first_interval=0.1)


def unregister():
    if hasattr(bpy.types.Scene, "arnold"):
        del bpy.types.Scene.arnold

    bpy.utils.unregister_class(ArnoldRenderProperties)
    bpy.utils.unregister_class(ArnoldGlobalRenderProperties)
    bpy.utils.unregister_class(ArnoldCustomRenderVar)
    bpy.utils.unregister_class(ArnoldAovFilter)
