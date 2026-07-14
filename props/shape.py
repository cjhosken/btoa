import bpy

from ..usd import USDProperty

class ArnoldTraceSet(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="")


class ArnoldShapeProperties(bpy.types.PropertyGroup):

    ### Subdivision
    subdiv_type: USDProperty(
        name="Subdivision Type",
        usd="primvars:arnold:subdiv_type",
        type=bpy.props.EnumProperty,
        items=[
            ("none", "None", "No subdivision"),
            ("catclark", "Catmull-Clark", "Catmull-Clark subdivision"),
            ("linear", "Linear", "linear")
        ],
        default="none",
    )

    subdiv_iterations: USDProperty(
        name="Subdivision Iterations",
        usd="primvars:arnold:subdiv_iterations",
        type=bpy.props.IntProperty,
        default=1, min=0, max=100
    )

    subdiv_adaptive_metric: USDProperty(
        name="Adaptive Metric",
        usd="primvars:arnold:subdiv_adaptive_metric",
        type=bpy.props.EnumProperty,
        items=[
            ("auto", "Auto", ""),
            ("edge_length", "Edge Length", ""),
            ("flatness", "Flatness", ""),
        ],
        default="auto",
    )

    subdiv_adaptive_error: USDProperty(
        name="Adaptive Error",
        usd="primvars:arnold:subdiv_adaptive_error",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=10.0
    )

    subdiv_adaptive_space: USDProperty(
        name="Adaptive Space",
        usd="primvars:arnold:subdiv_adaptive_space",
        type=bpy.props.EnumProperty,
        items=[
            ("raster", "Raster", "Measure error in raster space"),
            ("object", "Object", "Measure error in object space"),
        ],
        default="raster",
    )

    subdiv_uv_smoothing: USDProperty(
        name="UV Smoothing",
        usd="primvars:arnold:subdiv_uv_smoothing",
        type=bpy.props.EnumProperty,
        items=[
            ("pin_corners", "Pin Corners", "Pin UV corners"),
            ("pin_borders", "Pin Borders", "Pin UV seams"),
            ("linear", "Linear", "Linear UV smoothing"),
            ("smooth", "Smooth", "Smooth UV interpolation"),
        ],
        default="pin_corners",
    )
    
    subdiv_smooth_derivs: USDProperty(
        name="Smooth Derivatives",
        usd="primvars:arnold:subdiv_smooth_derivs",
        type=bpy.props.BoolProperty,
        default=False,
    )

    subdiv_frustum_ignore: USDProperty(
        name="Frustum Ignore",
        usd="primvars:arnold:subdiv_frustum_ignore",
        type=bpy.props.BoolProperty,
        default=False,
    )

    ### Displacement

    disp_height: USDProperty(
        name="Height",
        usd="primvars:arnold:disp_height",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=10.0
    )

    disp_zero_value: USDProperty(
        name="Zero Value",
        usd="primvars:arnold:disp_zero_value",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=10.0
    )

    disp_padding: USDProperty(
        name="Padding",
        usd="primvars:arnold:disp_padding",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=10.0
    )

    disp_autobump: USDProperty(
        name="Autobump",
        usd="primvars:arnold:disp_autobump",
        type=bpy.props.BoolProperty,
        default=False,
    )

    autobump_camera: USDProperty(
        name="Camera Ray Autobump Visibility", default=True,
        usd="primvars:arnold:autobump_visibility:camera",
        type=bpy.props.BoolProperty,
    )

    autobump_shadow: USDProperty(
        name="Shadow Ray Autobump Visibility", default=True,
        usd="primvars:arnold:autobump_visibility:shadow",
        type=bpy.props.BoolProperty,
    )

    autobump_diffuse_transmit: USDProperty(
        name="Diffuse Transmit Ray Autobump Visibility", default=True,
        usd="primvars:arnold:autobump_visibility:diffuse_transmit",
        type=bpy.props.BoolProperty,
    )

    autobump_specular_transmit: USDProperty(
        name="Specular Transmit Ray Autobump Visibility", default=True,
        usd="primvars:arnold:autobump_visibility:specular_transmit",
        type=bpy.props.BoolProperty,
    )

    autobump_volume: USDProperty(
        name="Volume Ray Autobump Visibility", default=True,
        usd="primvars:arnold:autobump_visibility:volume",
        type=bpy.props.BoolProperty,
    )

    autobump_diffuse_reflect: USDProperty(
        name="Diffuse Reflect Ray Autobump Visibility", default=True,
        usd="primvars:arnold:autobump_visibility:diffuse_reflect",
        type=bpy.props.BoolProperty,
    )

    autobump_specular_reflect: USDProperty(
        name="Specular Reflect Ray Autobump Visibility", default=True,
        usd="primvars:arnold:autobump_visibility:specular_reflect",
        type=bpy.props.BoolProperty,
    )

    autobump_subsurface: USDProperty(
        name="Subsurface Ray Autobump Visibility", default=True,
        usd="primvars:arnold:autobump_visibility:subsurface",
        type=bpy.props.BoolProperty,
    )

    ### Volume

    step_size: USDProperty(
        name="Step Size",
        usd="primvars:arnold:step_size",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=10.0
    )

    step_scale: USDProperty(
        name="Step Scale",
        usd="primvars:arnold:step_scale",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=10.0
    )

    volume_padding: USDProperty(
        name="Padding",
        usd="primvars:arnold:volume_padding",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=10.0
    )

    mipmap_bias: USDProperty(
        name="MipMap Bias",
        usd="primvars:arnold:mipmap_bias",
        type=bpy.props.IntProperty,
        default=0, min=-31, max=31
    )

    ### Motion Blur

    transform_type: USDProperty(
        name="Transform Type",
        usd="primvars:arnold:transform_type",
        type=bpy.props.EnumProperty,
        items=[
            ("linear", "Linear", ""),
            ("rotate_about_origin", "Rotate About Origin", ""),
            ("rotate_about_center", "Rotate About Center", ""),
        ],
        default="rotate_about_center",
    )

    deform_keys: USDProperty(
        name="Deform Keys",
        usd="primvars:arnold:deform_keys",
        type=bpy.props.IntProperty,
        default=3, min=0, soft_max=10
    )

    transform_keys: USDProperty(
        name="Transform Keys",
        usd="primvars:arnold:transform_keys",
        type=bpy.props.IntProperty,
        default=3, min=0, soft_max=10 
    )

    ### Visibility
    vis_camera: USDProperty(
        name="Camera Ray Visibility",
        usd="primvars:arnold:visibility:camera",
        type=bpy.props.BoolProperty,
        default=True
    )

    vis_shadow: USDProperty(
        name="Shadow Ray Visibility",
        usd="primvars:arnold:visibility:shadow",
        type=bpy.props.BoolProperty,
        default=True
    )
    vis_diffuse_transmit: USDProperty(
        name="Diffuse Transmit Ray Visibility",
        usd="primvars:arnold:visibility:diffuse_transmit",
        type=bpy.props.BoolProperty,
        default=True
    )
    vis_specular_transmit: USDProperty(
        name="Specular Transmit Ray Visibility",
        usd="primvars:arnold:visibility:specular_transmit",
        type=bpy.props.BoolProperty,
        default=True
    )
    vis_volume: USDProperty(
        name="Volume Ray Visibility",
        usd="primvars:arnold:visibility:volume",
        type=bpy.props.BoolProperty,
        default=True
    )
    vis_diffuse_reflect: USDProperty(
        name="Diffuse Reflect Ray Visibility",
        usd="primvars:arnold:visibility:diffuse_reflect",
        type=bpy.props.BoolProperty,
        default=True
    )
    vis_specular_reflect: USDProperty(
        name="Specular Reflect Ray Visibility",
        usd="primvars:arnold:visibility:specular_reflect",
        type=bpy.props.BoolProperty,
        default=True
    )

    receive_shadows: USDProperty(
        name="Receive Shadows",
        usd="primvars:arnold:receive_shadows",
        type=bpy.props.BoolProperty,
        default=True,
    )
    
    self_shadows: USDProperty(
        name="Self Shadows",
        usd="primvars:arnold:self_shadows",
        type=bpy.props.BoolProperty,
        default=True,
    )

    opaque: USDProperty(
        name="Opaque",
        usd="primvars:arnold:opaque",
        type=bpy.props.BoolProperty,
        default=False,
    )

    matte: USDProperty(
        name="Matte",
        usd="primvars:arnold:matte",
        type=bpy.props.BoolProperty,
        default=False,
    )

    ### Normals

    smoothing: USDProperty(
        name="Smoothing",
        usd="primvars:arnold:smoothing",
        type=bpy.props.BoolProperty,
        default=True,
    )

    invert_normals: USDProperty(
        name="Invert Normals",
        usd="primvars:arnold:invert_normals",
        type=bpy.props.BoolProperty,
        default=False,
    )

    double_sided_camera: USDProperty(
        name="Camera Ray Double Sided", default=True,
        usd="primvars:arnold:sidedness:camera",
        type=bpy.props.BoolProperty,
    )

    double_sided_shadow: USDProperty(
        name="Shadow Ray Double Sided", default=True,
        usd="primvars:arnold:sidedness:shadow",
        type=bpy.props.BoolProperty,
    )

    double_sided_diffuse_transmit: USDProperty(
        name="Diffuse Transmit Ray Double Sided", default=True,
        usd="primvars:arnold:sidedness:diffuse_transmit",
        type=bpy.props.BoolProperty,
    )

    double_sided_specular_transmit: USDProperty(
        name="Specular Transmit Ray Double Sided", default=True,
        usd="primvars:arnold:sidedness:specular_transmit",
        type=bpy.props.BoolProperty,
    )

    double_sided_volume: USDProperty(
        name="Volume Ray Double Sided", default=True,
        usd="primvars:arnold:sidedness:volume",
        type=bpy.props.BoolProperty,
    )

    double_sided_diffuse_reflect: USDProperty(
        name="Diffuse Reflect Ray Double Sided", default=True,
        usd="primvars:arnold:sidedness:diffuse_reflect",
        type=bpy.props.BoolProperty,
    )

    double_sided_specular_reflect: USDProperty(
        name="Specular Reflect Ray Double Sided", default=True,
        usd="primvars:arnold:sidedness:specular_reflect",
        type=bpy.props.BoolProperty,
    )

    ### Shape

    min_pixel_width: USDProperty(
        name="Min. Pixel Width",
        usd="primvars:arnold:min_pixel_width",
        type=bpy.props.FloatProperty,
        default=0.0,
    )

    default_radius: USDProperty(
        name="Default Radius",
        usd="primvars:arnold:radius",
        type=bpy.props.FloatProperty,
        default=0.0,
    )

    basis: USDProperty(
        name="Basis",
        usd="primvars:arnold:basis",
        type=bpy.props.EnumProperty,
        items=[
            ("bezier", "Bezier", "Cubic Bezier"),
            ("b-spline", "B-Spline", "Cubic B-Spline"),
            ("catmull-rom", "Catmull-Rom", "Catmull-Rom spline"),
            ("linear", "Linear", "Linear basis"),
        ],
        default="bezier",
    )

    mode: USDProperty(
        name="Mode",
        usd="primvars:arnold:mode",
        type=bpy.props.EnumProperty,
        items=[
            ("ribbon", "Ribbon", ""),
            ("thick", "Thick", ""),
            ("oriented", "Oriented", "")
        ],
        default="ribbon",
    )

    ### Light
    light: USDProperty(
        name="Geometry Light",
        usd="primvars:arnold:light",
        type=bpy.props.BoolProperty,
        default=False,
    )

    light_color: USDProperty(
        name="Color", subtype='COLOR',
        usd="primvars:arnold:light:color",
        type=bpy.props.FloatVectorProperty,
        default=(1.0, 1.0, 1.0), min=0.0, max=1.0
    )

    light_intensity: USDProperty(
        name="Intensity",
        usd="primvars:arnold:light:intensity",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=10.0
    )

    light_exposure: USDProperty(
        name="Exposure",
        usd="primvars:arnold:light:exposure",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=-5.0, soft_max=5.0
    )

    light_cast_shadows: USDProperty(
        name="Cast Shadows", default=True,
        usd="primvars:arnold:light:cast_shadows",
        type=bpy.props.BoolProperty,
    )

    light_cast_volumetric_shadows: USDProperty(
        name="Cast Volumetric Shadows", default=True,
        usd="primvars:arnold:light:cast_volumetric_shadows",
        type=bpy.props.BoolProperty,
    )

    light_shadow_density: USDProperty(
        name="Shadow Density", 
        usd="primvars:arnold:light:shadow_density",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0
    )

    light_shadow_color: USDProperty(
        name="Shadow Color", subtype='COLOR',
        usd="primvars:arnold:light:shadow_color",
        type=bpy.props.FloatVectorProperty,
        default=(0.0, 0.0, 0.0), min=0.0, max=1.0
    )

    light_samples: USDProperty(
        name="Samples",
        usd="primvars:arnold:light:samples",
        type=bpy.props.IntProperty,
        default=1, min=0, soft_max=10
    )

    light_normalize: USDProperty(
        name="Normalize",
        usd="primvars:arnold:light:normalize",
        type=bpy.props.BoolProperty,
        default=True
    )

    light_diffuse: USDProperty(
        name="Diffuse",
        usd="primvars:arnold:light:diffuse",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0
    )

    light_specular: USDProperty(
        name="Specular",
        usd="primvars:arnold:light:specular",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0
    )

    light_sss: USDProperty(
        name="SSS",
        usd="primvars:arnold:light:sss",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0
    )

    light_indirect: USDProperty(
        name="Indirect",
        usd="primvars:arnold:light:indirect",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0
    )
    
    light_max_bounces: USDProperty(
        name="Max Bounces",
        usd="primvars:arnold:light:max_bounces",
        type=bpy.props.IntProperty,
        default=999, min=0, soft_max=1000
    )

    light_volume_samples: USDProperty(
        name="Volume Samples",
        usd="primvars:arnold:light:volume_samples",
        type=bpy.props.IntProperty,
        default=2, min=0, soft_max=8
    )

    light_volume: USDProperty(
        name="Volume",
        usd="primvars:arnold:light:volume",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0
    )

    light_sampling_mode: USDProperty(
        name="Sampling Mode",
        usd="primvars:arnold:light:sampling_mode",
        type=bpy.props.EnumProperty,
        items=[
            ("auto", "Auto", ""),
            ("local", "Local", ""),
        ],
        default="auto",
    )


def register():
    bpy.utils.register_class(ArnoldTraceSet)
    bpy.utils.register_class(ArnoldShapeProperties)

    if not hasattr(bpy.types.Object, "arnold"):
        bpy.types.Object.arnold = bpy.props.PointerProperty(
            name="Arnold",
            description="Arnold shape properties",
            type=ArnoldShapeProperties,
        )


def unregister():
    if hasattr(bpy.types.Object, "arnold"):
        del bpy.types.Object.arnold

    bpy.utils.unregister_class(ArnoldShapeProperties)
    bpy.utils.unregister_class(ArnoldTraceSet)
