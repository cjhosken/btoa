import bpy
from ..usd import USDProperty

def make_traceset(prop_name, default=None):
    """Custom Traceset function based on USDProperty to convert strings into string[] (for arnold)"""
    if default is None:
        default = []

    def getter(self):
        value = self.id_data.get(prop_name, default)
        return " ".join(value)

    def setter(self, value):
        self.id_data[prop_name] = value.split()

    return getter, setter

class ArnoldShapeProperties(bpy.types.PropertyGroup):

    ### Subdivision

    subdiv_type: USDProperty(
        name="Subdivision Type",
        description="Subdivision algorithm (None, Catmull-Clark, Linear)",
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
        description="Maximum number of subdivision iterations",
        usd="primvars:arnold:subdiv_iterations",
        type=bpy.props.IntProperty,
        default=1, soft_min=0, soft_max=100
    )

    subdiv_adaptive_metric: USDProperty(
        name="Adaptive Metric",
        description="Metric used to determine adaptive tessellation (Edge Length or Flatness)",
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
        description="Tessellation error threshold (in pixels for raster space)",
        usd="primvars:arnold:subdiv_adaptive_error",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=10.0
    )

    subdiv_adaptive_space: USDProperty(
        name="Adaptive Space",
        description="Coordinate space for error measurement (Raster or Object)",
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
        description="Tessellation UV coordinates interpolation smoothing type",
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
        description="Smooth limit surface derivatives",
        usd="primvars:arnold:subdiv_smooth_derivs",
        type=bpy.props.BoolProperty,
        default=False,
    )

    subdiv_frustum_ignore: USDProperty(
        name="Frustum Ignore",
        description="Ignore camera frustum culling for subdivision",
        usd="primvars:arnold:subdiv_frustum_ignore",
        type=bpy.props.BoolProperty,
        default=False,
    )

    ### Displacement

    disp_height: USDProperty(
        name="Height",
        description="Displacement height scaling multiplier",
        usd="primvars:arnold:disp_height",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=10.0
    )

    disp_zero_value: USDProperty(
        name="Zero Value",
        description="Displacement zero-level value offset",
        usd="primvars:arnold:disp_zero_value",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=10.0
    )

    disp_padding: USDProperty(
        name="Padding",
        description="Additional bounding box padding for displacement",
        usd="primvars:arnold:disp_padding",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=10.0
    )

    disp_autobump: USDProperty(
        name="Autobump",
        description="Enable autobump which maps displacement details onto bump map calculations",
        usd="primvars:arnold:disp_autobump",
        type=bpy.props.BoolProperty,
        default=False,
    )

    autobump_camera: USDProperty(
        name="Camera Ray Autobump Visibility",
        description="Autobump visibility for camera rays",
        usd="primvars:arnold:autobump_visibility:camera",
        type=bpy.props.BoolProperty,
        default=True,
    )

    autobump_shadow: USDProperty(
        name="Shadow Ray Autobump Visibility",
        description="Autobump visibility for shadow rays",
        usd="primvars:arnold:autobump_visibility:shadow",
        type=bpy.props.BoolProperty,
        default=True,
    )

    autobump_diffuse_transmit: USDProperty(
        name="Diffuse Transmit Ray Autobump Visibility",
        description="Autobump visibility for diffuse transmission rays",
        usd="primvars:arnold:autobump_visibility:diffuse_transmit",
        type=bpy.props.BoolProperty,
        default=True,
    )

    autobump_specular_transmit: USDProperty(
        name="Specular Transmit Ray Autobump Visibility",
        description="Autobump visibility for specular transmission rays",
        usd="primvars:arnold:autobump_visibility:specular_transmit",
        type=bpy.props.BoolProperty,
        default=True,
    )

    autobump_volume: USDProperty(
        name="Volume Ray Autobump Visibility",
        description="Autobump visibility for volume scattering rays",
        usd="primvars:arnold:autobump_visibility:volume",
        type=bpy.props.BoolProperty,
        default=True,
    )

    autobump_diffuse_reflect: USDProperty(
        name="Diffuse Reflect Ray Autobump Visibility",
        description="Autobump visibility for diffuse reflection rays",
        usd="primvars:arnold:autobump_visibility:diffuse_reflect",
        type=bpy.props.BoolProperty,
        default=True,
    )

    autobump_specular_reflect: USDProperty(
        name="Specular Reflect Ray Autobump Visibility",
        description="Autobump visibility for specular reflection rays",
        usd="primvars:arnold:autobump_visibility:specular_reflect",
        type=bpy.props.BoolProperty,
        default=True,
    )

    autobump_subsurface: USDProperty(
        name="Subsurface Ray Autobump Visibility",
        description="Autobump visibility for subsurface scattering rays",
        usd="primvars:arnold:autobump_visibility:subsurface",
        type=bpy.props.BoolProperty,
        default=True,
    )

    ### Volume

    step_size: USDProperty(
        name="Step Size",
        description="Ray marching step size for volume shapes (0 for auto-calculation)",
        usd="primvars:arnold:step_size",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=10.0
    )

    step_scale: USDProperty(
        name="Step Scale",
        description="Ray marching step scale factor",
        usd="primvars:arnold:step_scale",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=10.0
    )

    volume_padding: USDProperty(
        name="Padding",
        description="Additional bounding box padding for volumes",
        usd="primvars:arnold:volume_padding",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=10.0
    )

    mipmap_bias: USDProperty(
        name="MipMap Bias",
        description="Mipmap LOD selection bias offset for volumes",
        usd="primvars:arnold:mipmap_bias",
        type=bpy.props.IntProperty,
        default=0, soft_min=-31, soft_max=31
    )

    ### Motion Blur

    transform_type: USDProperty(
        name="Transform Type",
        description="Interpolation type for motion blur transforms",
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
        description="Number of motion keys for deformation",
        usd="primvars:arnold:deform_keys",
        type=bpy.props.IntProperty,
        default=3, soft_min=0, soft_max=10
    )

    transform_keys: USDProperty(
        name="Transform Keys",
        description="Number of motion keys for transformation",
        usd="primvars:arnold:transform_keys",
        type=bpy.props.IntProperty,
        default=3, soft_min=0, soft_max=10 
    )

    ### Visibility
    vis_camera: USDProperty(
        name="Camera Ray Visibility",
        description="Shape visibility to camera rays",
        usd="primvars:arnold:visibility:camera",
        type=bpy.props.BoolProperty,
        default=True
    )

    vis_shadow: USDProperty(
        name="Shadow Ray Visibility",
        description="Shape visibility to shadow rays",
        usd="primvars:arnold:visibility:shadow",
        type=bpy.props.BoolProperty,
        default=True
    )
    vis_diffuse_transmit: USDProperty(
        name="Diffuse Transmit Ray Visibility",
        description="Shape visibility to diffuse transmission rays",
        usd="primvars:arnold:visibility:diffuse_transmit",
        type=bpy.props.BoolProperty,
        default=True
    )
    vis_specular_transmit: USDProperty(
        name="Specular Transmit Ray Visibility",
        description="Shape visibility to specular transmission rays",
        usd="primvars:arnold:visibility:specular_transmit",
        type=bpy.props.BoolProperty,
        default=True
    )
    vis_volume: USDProperty(
        name="Volume Ray Visibility",
        description="Shape visibility to volume scattering rays",
        usd="primvars:arnold:visibility:volume",
        type=bpy.props.BoolProperty,
        default=True
    )
    vis_diffuse_reflect: USDProperty(
        name="Diffuse Reflect Ray Visibility",
        description="Shape visibility to diffuse reflection rays",
        usd="primvars:arnold:visibility:diffuse_reflect",
        type=bpy.props.BoolProperty,
        default=True
    )
    vis_specular_reflect: USDProperty(
        name="Specular Reflect Ray Visibility",
        description="Shape visibility to specular reflection/glossy rays",
        usd="primvars:arnold:visibility:specular_reflect",
        type=bpy.props.BoolProperty,
        default=True
    )

    receive_shadows: USDProperty(
        name="Receive Shadows",
        description="Receive shadows from other objects",
        usd="primvars:arnold:receive_shadows",
        type=bpy.props.BoolProperty,
        default=True,
    )
    
    self_shadows: USDProperty(
        name="Self Shadows",
        description="Enable self-shadowing",
        usd="primvars:arnold:self_shadows",
        type=bpy.props.BoolProperty,
        default=True,
    )

    opaque: USDProperty(
        name="Opaque",
        description="Render the shape as opaque (ignores shader transparency for shadow/transmission rays)",
        usd="primvars:arnold:opaque",
        type=bpy.props.BoolProperty,
        default=False,
    )

    matte: USDProperty(
        name="Matte",
        description="Render the shape as a matte object",
        usd="primvars:arnold:matte",
        type=bpy.props.BoolProperty,
        default=False,
    )

    trace_sets: bpy.props.StringProperty(
        name="Trace Sets",
        description="",
        default="",
        get=make_traceset("primvars:arnold:trace_sets", True)[0],
        set=make_traceset("primvars:arnold:trace_sets", True)[1]
    )

    interior_set: USDProperty(
        name="Interior Set",
        description="",
        usd="primvars:interior_set",
        type=bpy.props.StringProperty,
        default=""
    )

    ### Normals

    smoothing: USDProperty(
        name="Smoothing",
        description="Smooth vertex normals",
        usd="primvars:arnold:smoothing",
        type=bpy.props.BoolProperty,
        default=True,
    )

    invert_normals: USDProperty(
        name="Invert Normals",
        description="Flip normal directions",
        usd="primvars:arnold:invert_normals",
        type=bpy.props.BoolProperty,
        default=False,
    )

    double_sided_camera: USDProperty(
        name="Camera Ray Double Sided",
        description="Double-sided rendering for camera rays",
        usd="primvars:arnold:sidedness:camera",
        type=bpy.props.BoolProperty,
        default=True,
    )

    double_sided_shadow: USDProperty(
        name="Shadow Ray Double Sided",
        description="Double-sided rendering for shadow rays",
        usd="primvars:arnold:sidedness:shadow",
        type=bpy.props.BoolProperty,
        default=True,
    )

    double_sided_diffuse_transmit: USDProperty(
        name="Diffuse Transmit Ray Double Sided",
        description="Double-sided rendering for diffuse transmission rays",
        usd="primvars:arnold:sidedness:diffuse_transmit",
        type=bpy.props.BoolProperty,
        default=True,
    )

    double_sided_specular_transmit: USDProperty(
        name="Specular Transmit Ray Double Sided",
        description="Double-sided rendering for specular transmission rays",
        usd="primvars:arnold:sidedness:specular_transmit",
        type=bpy.props.BoolProperty,
        default=True,
    )

    double_sided_volume: USDProperty(
        name="Volume Ray Double Sided",
        description="Double-sided rendering for volume rays",
        usd="primvars:arnold:sidedness:volume",
        type=bpy.props.BoolProperty,
        default=True,
    )

    double_sided_diffuse_reflect: USDProperty(
        name="Diffuse Reflect Ray Double Sided",
        description="Double-sided rendering for diffuse reflection rays",
        usd="primvars:arnold:sidedness:diffuse_reflect",
        type=bpy.props.BoolProperty,
        default=True,
    )

    double_sided_specular_reflect: USDProperty(
        name="Specular Reflect Ray Double Sided",
        description="Double-sided rendering for specular reflection rays",
        usd="primvars:arnold:sidedness:specular_reflect",
        type=bpy.props.BoolProperty,
        default=True,
    )

    ### Shape

    min_pixel_width: USDProperty(
        name="Min. Pixel Width",
        description="Minimum pixel width threshold for curve/hair shapes",
        usd="primvars:arnold:min_pixel_width",
        type=bpy.props.FloatProperty,
        default=0.0,
    )

    default_radius: USDProperty(
        name="Default Radius",
        description="Default radius thickness for curve/hair shapes",
        usd="primvars:arnold:radius",
        type=bpy.props.FloatProperty,
        default=0.0,
    )

    basis: USDProperty(
        name="Basis",
        description="Interpolation spline basis for curves",
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
        description="Spline geometry mode (Ribbon, Thick, Oriented)",
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
        description="Enable geometry mesh light emission",
        usd="primvars:arnold:light",
        type=bpy.props.BoolProperty,
        default=False,
    )

    light_color: USDProperty(
        name="Color", subtype='COLOR',
        description="Mesh light emission color",
        usd="primvars:arnold:light:color",
        type=bpy.props.FloatVectorProperty,
        default=(1.0, 1.0, 1.0), soft_min=0.0, soft_max=1.0
    )

    light_intensity: USDProperty(
        name="Intensity",
        description="Mesh light emission intensity",
        usd="primvars:arnold:light:intensity",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=10.0
    )

    light_exposure: USDProperty(
        name="Exposure",
        description="Mesh light exposure",
        usd="primvars:arnold:light:exposure",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=-5.0, soft_max=5.0
    )

    light_cast_shadows: USDProperty(
        name="Cast Shadows",
        description="Mesh light casts shadows",
        usd="primvars:arnold:light:cast_shadows",
        type=bpy.props.BoolProperty,
        default=True,
    )

    light_cast_volumetric_shadows: USDProperty(
        name="Cast Volumetric Shadows",
        description="Mesh light casts volumetric shadows",
        usd="primvars:arnold:light:cast_volumetric_shadows",
        type=bpy.props.BoolProperty,
        default=True,
    )

    light_shadow_density: USDProperty(
        name="Shadow Density", 
        description="Mesh light shadow density",
        usd="primvars:arnold:light:shadow_density",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0
    )

    light_shadow_color: USDProperty(
        name="Shadow Color", subtype='COLOR',
        description="Mesh light shadow tint color",
        usd="primvars:arnold:light:shadow_color",
        type=bpy.props.FloatVectorProperty,
        default=(0.0, 0.0, 0.0), soft_min=0.0, soft_max=1.0
    )

    light_samples: USDProperty(
        name="Samples",
        description="Mesh light samples",
        usd="primvars:arnold:light:samples",
        type=bpy.props.IntProperty,
        default=1, soft_min=0, soft_max=10
    )

    light_normalize: USDProperty(
        name="Normalize",
        description="Normalize mesh light intensity by surface area",
        usd="primvars:arnold:light:normalize",
        type=bpy.props.BoolProperty,
        default=True
    )

    light_diffuse: USDProperty(
        name="Diffuse",
        description="Mesh light diffuse reflection contribution scale",
        usd="primvars:arnold:light:diffuse",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0
    )

    light_specular: USDProperty(
        name="Specular",
        description="Mesh light specular reflection contribution scale",
        usd="primvars:arnold:light:specular",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0
    )

    light_sss: USDProperty(
        name="SSS",
        description="Mesh light subsurface scattering contribution scale",
        usd="primvars:arnold:light:sss",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0
    )

    light_indirect: USDProperty(
        name="Indirect",
        description="Mesh light indirect lighting contribution scale",
        usd="primvars:arnold:light:indirect",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0
    )
    
    light_max_bounces: USDProperty(
        name="Max Bounces",
        description="Mesh light maximum bounces",
        usd="primvars:arnold:light:max_bounces",
        type=bpy.props.IntProperty,
        default=999, soft_min=0, soft_max=1000
    )

    light_volume_samples: USDProperty(
        name="Volume Samples",
        description="Mesh light volume samples",
        usd="primvars:arnold:light:volume_samples",
        type=bpy.props.IntProperty,
        default=2, soft_min=0, soft_max=8
    )

    light_volume: USDProperty(
        name="Volume",
        description="Mesh light volume contribution scale",
        usd="primvars:arnold:light:volume",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0
    )

    light_aov: USDProperty(
        name="AOV",
        description="",
        usd="primvars:arnold:light:aov",
        type=bpy.props.StringProperty,
        default=""
    )

    light_sampling_mode: USDProperty(
        name="Sampling Mode",
        description="Mesh light sampling mode",
        usd="primvars:arnold:light:sampling_mode",
        type=bpy.props.EnumProperty,
        items=[
            ("auto", "Auto", ""),
            ("local", "Local", ""),
        ],
        default="auto",
    )

    light_shaders: USDProperty(
        name="Shaders",
        description="",
        usd="primvars:arnold:light:shaders",
        type=bpy.props.StringProperty,
        default=""
    )


def register():
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
