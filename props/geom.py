import bpy


class SubdivType:
    items = (
        ("none", "None", "No subdivision"),
        ("catclark", "Catmull-Clark", "Catmull-Clark subdivision"),
    )


class AdaptiveSpace:
    items = (
        ("raster", "Raster", "Measure error in raster space"),
        ("world", "World", "Measure error in world space"),
    )


class UVSmoothing:
    items = (
        ("linear", "Linear", "Linear UV smoothing"),
        ("smooth", "Smooth", "Smooth UV interpolation"),
        ("pin_corners", "Pin Corners", "Pin UV corners"),
        ("pin_seams", "Pin Seams", "Pin UV seams"),
        ("pin_all", "Pin All", "Pin all UVs"),
    )


class BasisType:
    items = (
        ("linear", "Linear", "Linear basis"),
        ("bezier", "Bezier", "Cubic Bezier"),
        ("b-spline", "B-Spline", "Cubic B-Spline"),
        ("catmull-rom", "Catmull-Rom", "Catmull-Rom spline"),
    )


class ArnoldGeomProperties(bpy.types.PropertyGroup):

    # Subdivision
    subdiv_type: bpy.props.EnumProperty(
        name="Subdivision Type",
        items=SubdivType.items,
        default="none",
    )
    subdiv_iterations: bpy.props.IntProperty(
        name="Subdivision Iterations",
        default=0, min=0, soft_max=6,
    )
    adaptive_metric: bpy.props.EnumProperty(
        name="Adaptive Metric",
        items=[
            ("edge_length", "Edge Length", ""),
            ("flatness", "Flatness", ""),
            ("both", "Both", ""),
        ],
        default="edge_length",
    )
    adaptive_error: bpy.props.FloatProperty(
        name="Adaptive Error",
        default=0.0, min=0.0, soft_max=10.0,
    )
    adaptive_space: bpy.props.EnumProperty(
        name="Adaptive Space",
        items=AdaptiveSpace.items,
        default="raster",
    )
    uv_smoothing: bpy.props.EnumProperty(
        name="UV Smoothing",
        items=UVSmoothing.items,
        default="linear",
    )
    smooth_derivatives: bpy.props.BoolProperty(
        name="Smooth Derivatives",
        default=False,
    )
    frustum_ignore: bpy.props.BoolProperty(
        name="Frustum Ignore",
        description="Ignore frustum culling for this object",
        default=False,
    )

    # Ray Height
    height: bpy.props.FloatProperty(
        name="Height",
        default=0.0, min=0.0,
    )
    zero_value: bpy.props.FloatProperty(
        name="Zero Value",
        default=0.0,
    )
    padding: bpy.props.FloatProperty(
        name="Padding",
        default=0.0, min=0.0,
    )

    # Autobump
    autobump: bpy.props.BoolProperty(
        name="Autobump",
        default=False,
    )
    autobump_camera: bpy.props.BoolProperty(name="Camera", default=True)
    autobump_shadow: bpy.props.BoolProperty(name="Shadow", default=True)
    autobump_diffuse_transmit: bpy.props.BoolProperty(name="Diffuse Transmit", default=True)
    autobump_specular_transmit: bpy.props.BoolProperty(name="Specular Transmit", default=True)
    autobump_volume: bpy.props.BoolProperty(name="Volume", default=True)
    autobump_diffuse_reflect: bpy.props.BoolProperty(name="Diffuse Reflect", default=True)
    autobump_specular_reflect: bpy.props.BoolProperty(name="Specular Reflect", default=True)
    autobump_subsurface: bpy.props.BoolProperty(name="Subsurface", default=True)

    # Volume
    step_size: bpy.props.FloatProperty(
        name="Step Size",
        default=0.0, min=0.0,
    )
    step_scale: bpy.props.FloatProperty(
        name="Step Scale",
        default=1.0, min=0.0,
    )
    volume_padding: bpy.props.FloatProperty(
        name="Padding",
        default=0.0, min=0.0,
    )
    mipmap_bias: bpy.props.FloatProperty(
        name="Mipmap Bias",
        default=0.0,
    )

    # Motion
    transform_type: bpy.props.EnumProperty(
        name="Transform Type",
        items=[
            ("linear", "Linear", "Linear interpolation"),
            ("step", "Step", "Step interpolation"),
            ("deform", "Deform", "Deformation blur"),
        ],
        default="linear",
    )
    deform_keys: bpy.props.IntProperty(
        name="Deform Keys",
        default=-1, min=-1, soft_max=10,
    )
    transform_keys: bpy.props.IntProperty(
        name="Transform Keys",
        default=-1, min=-1, soft_max=10,
    )

    # Visibility
    vis_camera: bpy.props.BoolProperty(name="Camera", default=True)
    vis_shadow: bpy.props.BoolProperty(name="Shadow", default=True)
    vis_diffuse_transmit: bpy.props.BoolProperty(name="Diffuse Transmit", default=True)
    vis_specular_transmit: bpy.props.BoolProperty(name="Specular Transmit", default=True)
    vis_volume: bpy.props.BoolProperty(name="Volume", default=True)
    vis_diffuse_reflect: bpy.props.BoolProperty(name="Diffuse Reflect", default=True)
    vis_specular_reflect: bpy.props.BoolProperty(name="Specular Reflect", default=True)
    vis_subsurface: bpy.props.BoolProperty(name="Subsurface", default=True)

    # Double Sided (per ray)
    double_sided_diffuse_reflect: bpy.props.BoolProperty(name="Diffuse Reflect", default=True)
    double_sided_specular_reflect: bpy.props.BoolProperty(name="Specular Reflect", default=True)
    double_sided_volume: bpy.props.BoolProperty(name="Volume", default=True)

    # Shape / Points
    min_pixel_width: bpy.props.FloatProperty(
        name="Min. Pixel Width",
        default=0.0, min=0.0,
    )
    default_radius: bpy.props.FloatProperty(
        name="Default Radius",
        default=0.0, min=0.0,
    )
    basis: bpy.props.EnumProperty(
        name="Basis",
        items=BasisType.items,
        default="linear",
    )
    mode: bpy.props.EnumProperty(
        name="Mode",
        items=[
            ("strip", "Strip", ""),
            ("ribbon", "Ribbon", ""),
            ("thick", "Thick", ""),
        ],
        default="strip",
    )

    # Geometry Light (mesh light)
    geom_light: bpy.props.BoolProperty(
        name="Geometry Light",
        description="Treat mesh as an area light",
        default=False,
    )
    light_color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0, max=1.0,
    )
    light_intensity: bpy.props.FloatProperty(
        name="Intensity",
        default=1.0, min=0.0, soft_max=100.0,
    )
    light_exposure: bpy.props.FloatProperty(
        name="Exposure",
        default=0.0,
    )
    light_cast_shadows: bpy.props.BoolProperty(
        name="Cast Shadows",
        default=True,
    )
    light_cast_volumetric_shadows: bpy.props.BoolProperty(
        name="Cast Volumetric Shadows",
        default=True,
    )
    light_shadow_density: bpy.props.FloatProperty(
        name="Shadow Density",
        default=1.0, min=0.0, soft_max=10.0,
    )
    light_shadow_color: bpy.props.FloatVectorProperty(
        name="Shadow Color",
        subtype='COLOR',
        default=(0.0, 0.0, 0.0),
        min=0.0, max=1.0,
    )
    light_samples: bpy.props.IntProperty(
        name="Samples",
        default=1, min=0, soft_max=100,
    )
    light_normalize: bpy.props.BoolProperty(
        name="Normalize",
        default=True,
    )
    light_diffuse: bpy.props.FloatProperty(
        name="Diffuse",
        default=1.0, min=0.0, soft_max=10.0,
    )
    light_specular: bpy.props.FloatProperty(
        name="Specular",
        default=1.0, min=0.0, soft_max=10.0,
    )
    light_sss: bpy.props.FloatProperty(
        name="SSS",
        default=1.0, min=0.0, soft_max=10.0,
    )
    light_indirect: bpy.props.FloatProperty(
        name="Indirect",
        default=1.0, min=0.0, soft_max=10.0,
    )
    light_max_bounces: bpy.props.IntProperty(
        name="Max Bounces",
        default=-1, min=-1, soft_max=100,
    )
    light_volume_samples: bpy.props.IntProperty(
        name="Volume Samples",
        default=1, min=0, soft_max=100,
    )
    light_volume: bpy.props.FloatProperty(
        name="Volume",
        default=1.0, min=0.0, soft_max=10.0,
    )
    light_aov: bpy.props.StringProperty(
        name="AOV",
        default="",
    )
    light_sampling_mode: bpy.props.EnumProperty(
        name="Sampling Mode",
        items=[
            ("IMPORTANCE", "Importance", ""),
            ("SHADE", "Shade All", ""),
        ],
        default="IMPORTANCE",
    )


def register():
    bpy.utils.register_class(ArnoldGeomProperties)

    if not hasattr(bpy.types.Mesh, "arnold"):
        bpy.types.Mesh.arnold = bpy.props.PointerProperty(
            name="Arnold",
            description="Arnold geometry properties",
            type=ArnoldGeomProperties,
        )


def unregister():
    if hasattr(bpy.types.Mesh, "arnold"):
        del bpy.types.Mesh.arnold

    bpy.utils.unregister_class(ArnoldGeomProperties)
