import bpy

from .utils import make_id_prop, make_vector_id_prop, make_enum_id_prop


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


class ArnoldTraceSet(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="")


class ArnoldShapeProperties(bpy.types.PropertyGroup):
    # Visibility (flat properties)
    vis_camera: bpy.props.BoolProperty(
        name="Camera", default=True,
        get=make_id_prop("primvars:arnold:visibility:camera", True)[0],
        set=make_id_prop("primvars:arnold:visibility:camera", True)[1]
    )
    vis_shadow: bpy.props.BoolProperty(
        name="Shadow", default=True,
        get=make_id_prop("primvars:arnold:visibility:shadow", True)[0],
        set=make_id_prop("primvars:arnold:visibility:shadow", True)[1]
    )
    vis_diffuse_transmit: bpy.props.BoolProperty(
        name="Diffuse Transmit", default=True,
        get=make_id_prop("primvars:arnold:visibility:diffuse_transmit", True)[0],
        set=make_id_prop("primvars:arnold:visibility:diffuse_transmit", True)[1]
    )
    vis_specular_transmit: bpy.props.BoolProperty(
        name="Specular Transmit", default=True,
        get=make_id_prop("primvars:arnold:visibility:specular_transmit", True)[0],
        set=make_id_prop("primvars:arnold:visibility:specular_transmit", True)[1]
    )
    vis_volume: bpy.props.BoolProperty(
        name="Volume", default=True,
        get=make_id_prop("primvars:arnold:visibility:volume", True)[0],
        set=make_id_prop("primvars:arnold:visibility:volume", True)[1]
    )
    vis_diffuse_reflect: bpy.props.BoolProperty(
        name="Diffuse Reflect", default=True,
        get=make_id_prop("primvars:arnold:visibility:diffuse_reflect", True)[0],
        set=make_id_prop("primvars:arnold:visibility:diffuse_reflect", True)[1]
    )
    vis_specular_reflect: bpy.props.BoolProperty(
        name="Specular Reflect", default=True,
        get=make_id_prop("primvars:arnold:visibility:specular_reflect", True)[0],
        set=make_id_prop("primvars:arnold:visibility:specular_reflect", True)[1]
    )
    vis_subsurface: bpy.props.BoolProperty(
        name="Subsurface", default=True,
        get=make_id_prop("primvars:arnold:visibility:subsurface", True)[0],
        set=make_id_prop("primvars:arnold:visibility:subsurface", True)[1]
    )

    # Autobump Visibility (flat properties)
    autobump_camera: bpy.props.BoolProperty(
        name="Camera", default=True,
        get=make_id_prop("primvars:arnold:autobump_visibility:camera", True)[0],
        set=make_id_prop("primvars:arnold:autobump_visibility:camera", True)[1]
    )
    autobump_shadow: bpy.props.BoolProperty(
        name="Shadow", default=True,
        get=make_id_prop("primvars:arnold:autobump_visibility:shadow", True)[0],
        set=make_id_prop("primvars:arnold:autobump_visibility:shadow", True)[1]
    )
    autobump_diffuse_transmit: bpy.props.BoolProperty(
        name="Diffuse Transmit", default=True,
        get=make_id_prop("primvars:arnold:autobump_visibility:diffuse_transmit", True)[0],
        set=make_id_prop("primvars:arnold:autobump_visibility:diffuse_transmit", True)[1]
    )
    autobump_specular_transmit: bpy.props.BoolProperty(
        name="Specular Transmit", default=True,
        get=make_id_prop("primvars:arnold:autobump_visibility:specular_transmit", True)[0],
        set=make_id_prop("primvars:arnold:autobump_visibility:specular_transmit", True)[1]
    )
    autobump_volume: bpy.props.BoolProperty(
        name="Volume", default=True,
        get=make_id_prop("primvars:arnold:autobump_visibility:volume", True)[0],
        set=make_id_prop("primvars:arnold:autobump_visibility:volume", True)[1]
    )
    autobump_diffuse_reflect: bpy.props.BoolProperty(
        name="Diffuse Reflect", default=True,
        get=make_id_prop("primvars:arnold:autobump_visibility:diffuse_reflect", True)[0],
        set=make_id_prop("primvars:arnold:autobump_visibility:diffuse_reflect", True)[1]
    )
    autobump_specular_reflect: bpy.props.BoolProperty(
        name="Specular Reflect", default=True,
        get=make_id_prop("primvars:arnold:autobump_visibility:specular_reflect", True)[0],
        set=make_id_prop("primvars:arnold:autobump_visibility:specular_reflect", True)[1]
    )
    autobump_subsurface: bpy.props.BoolProperty(
        name="Subsurface", default=True,
        get=make_id_prop("primvars:arnold:autobump_visibility:subsurface", True)[0],
        set=make_id_prop("primvars:arnold:autobump_visibility:subsurface", True)[1]
    )

    # Double Sided / Sideness (flat properties)
    double_sided_diffuse_reflect: bpy.props.BoolProperty(
        name="Diffuse Reflect", default=True,
        get=make_id_prop("primvars:arnold:sideness:diffuse_reflect", True)[0],
        set=make_id_prop("primvars:arnold:sideness:diffuse_reflect", True)[1]
    )
    double_sided_specular_reflect: bpy.props.BoolProperty(
        name="Specular Reflect", default=True,
        get=make_id_prop("primvars:arnold:sideness:specular_reflect", True)[0],
        set=make_id_prop("primvars:arnold:sideness:specular_reflect", True)[1]
    )
    double_sided_volume: bpy.props.BoolProperty(
        name="Volume", default=True,
        get=make_id_prop("primvars:arnold:sideness:volume", True)[0],
        set=make_id_prop("primvars:arnold:sideness:volume", True)[1]
    )

    # Geometry Light / Mesh Light (flat properties)
    light: bpy.props.BoolProperty(
        name="Geometry Light",
        get=make_id_prop("primvars:arnold:light", False)[0],
        set=make_id_prop("primvars:arnold:light", False)[1]
    )
    light_color: bpy.props.FloatVectorProperty(
        name="Color", subtype='COLOR', default=(1.0, 1.0, 1.0), min=0.0, max=1.0,
        get=make_vector_id_prop("primvars:arnold:light:color", (1.0, 1.0, 1.0))[0],
        set=make_vector_id_prop("primvars:arnold:light:color", (1.0, 1.0, 1.0))[1]
    )
    light_intensity: bpy.props.FloatProperty(
        name="Intensity", default=1.0, min=0.0,
        get=make_id_prop("primvars:arnold:light:intensity", 1.0)[0],
        set=make_id_prop("primvars:arnold:light:intensity", 1.0)[1]
    )
    light_exposure: bpy.props.FloatProperty(
        name="Exposure", default=0.0,
        get=make_id_prop("primvars:arnold:light:exposure", 0.0)[0],
        set=make_id_prop("primvars:arnold:light:exposure", 0.0)[1]
    )
    light_cast_shadows: bpy.props.BoolProperty(
        name="Cast Shadows", default=True,
        get=make_id_prop("primvars:arnold:light:cast_shadows", True)[0],
        set=make_id_prop("primvars:arnold:light:cast_shadows", True)[1]
    )
    light_cast_volumetric_shadows: bpy.props.BoolProperty(
        name="Cast Volumetric Shadows", default=True,
        get=make_id_prop("primvars:arnold:light:cast_volumetric_shadows", True)[0],
        set=make_id_prop("primvars:arnold:light:cast_volumetric_shadows", True)[1]
    )
    light_shadow_density: bpy.props.FloatProperty(
        name="Shadow Density", default=1.0, min=0.0,
        get=make_id_prop("primvars:arnold:light:shadow_density", 1.0)[0],
        set=make_id_prop("primvars:arnold:light:shadow_density", 1.0)[1]
    )
    light_shadow_color: bpy.props.FloatVectorProperty(
        name="Shadow Color", subtype='COLOR', default=(0.0, 0.0, 0.0), min=0.0, max=1.0,
        get=make_vector_id_prop("primvars:arnold:light:shadow_color", (0.0, 0.0, 0.0))[0],
        set=make_vector_id_prop("primvars:arnold:light:shadow_color", (0.0, 0.0, 0.0))[1]
    )
    light_samples: bpy.props.IntProperty(
        name="Samples", default=1, min=0,
        get=make_id_prop("primvars:arnold:light:samples", 1)[0],
        set=make_id_prop("primvars:arnold:light:samples", 1)[1]
    )
    light_normalize: bpy.props.BoolProperty(
        name="Normalize", default=True,
        get=make_id_prop("primvars:arnold:light:normalize", True)[0],
        set=make_id_prop("primvars:arnold:light:normalize", True)[1]
    )
    light_diffuse: bpy.props.FloatProperty(
        name="Diffuse", default=1.0, min=0.0,
        get=make_id_prop("primvars:arnold:light:diffuse", 1.0)[0],
        set=make_id_prop("primvars:arnold:light:diffuse", 1.0)[1]
    )
    light_specular: bpy.props.FloatProperty(
        name="Specular", default=1.0, min=0.0,
        get=make_id_prop("primvars:arnold:light:specular", 1.0)[0],
        set=make_id_prop("primvars:arnold:light:specular", 1.0)[1]
    )
    light_sss: bpy.props.FloatProperty(
        name="SSS", default=1.0, min=0.0,
        get=make_id_prop("primvars:arnold:light:sss", 1.0)[0],
        set=make_id_prop("primvars:arnold:light:sss", 1.0)[1]
    )
    light_indirect: bpy.props.FloatProperty(
        name="Indirect", default=1.0, min=0.0,
        get=make_id_prop("primvars:arnold:light:indirect", 1.0)[0],
        set=make_id_prop("primvars:arnold:light:indirect", 1.0)[1]
    )
    light_max_bounces: bpy.props.IntProperty(
        name="Max Bounces", default=-1, min=-1,
        get=make_id_prop("primvars:arnold:light:max_bounces", -1)[0],
        set=make_id_prop("primvars:arnold:light:max_bounces", -1)[1]
    )
    light_volume_samples: bpy.props.IntProperty(
        name="Volume Samples", default=1, min=0,
        get=make_id_prop("primvars:arnold:light:volume_samples", 1)[0],
        set=make_id_prop("primvars:arnold:light:volume_samples", 1)[1]
    )
    light_volume: bpy.props.FloatProperty(
        name="Volume", default=1.0, min=0.0,
        get=make_id_prop("primvars:arnold:light:volume", 1.0)[0],
        set=make_id_prop("primvars:arnold:light:volume", 1.0)[1]
    )
    light_sampling_mode: bpy.props.EnumProperty(
        name="Sampling Mode",
        items=[
            ("IMPORTANCE", "Importance", ""),
            ("SHADE", "Shade All", ""),
        ],
        get=make_enum_id_prop("primvars:arnold:light:sampling_mode", [("IMPORTANCE", "Importance", ""), ("SHADE", "Shade All", "")], "IMPORTANCE")[0],
        set=make_enum_id_prop("primvars:arnold:light:sampling_mode", [("IMPORTANCE", "Importance", ""), ("SHADE", "Shade All", "")], "IMPORTANCE")[1]
    )
    light_aov: bpy.props.StringProperty(
        name="AOV", default="",
        get=make_id_prop("primvars:arnold:light:aov", "")[0],
        set=make_id_prop("primvars:arnold:light:aov", "")[1]
    )

    # General properties
    basis: bpy.props.EnumProperty(
        name="Basis",
        items=BasisType.items,
        get=make_enum_id_prop("primvars:arnold:basis", BasisType.items, "bezier")[0],
        set=make_enum_id_prop("primvars:arnold:basis", BasisType.items, "bezier")[1]
    )

    deform_keys: bpy.props.IntProperty(
        name="Deform Keys",
        get=make_id_prop("primvars:arnold:deform_keys", 3)[0],
        set=make_id_prop("primvars:arnold:deform_keys", 3)[1]
    )

    disp_autobump: bpy.props.BoolProperty(
        name="Displacement Autobump",
        get=make_id_prop("primvars:arnold:disp_autobump", False)[0],
        set=make_id_prop("primvars:arnold:disp_autobump", False)[1]
    )
    
    disp_height: bpy.props.FloatProperty(
        name="Displacement Height",
        get=make_id_prop("primvars:arnold:disp_height", 1.0)[0],
        set=make_id_prop("primvars:arnold:disp_height", 1.0)[1]
    )

    disp_padding: bpy.props.FloatProperty(
        name="Displacement Padding",
        get=make_id_prop("primvars:arnold:disp_padding", 0.0)[0],
        set=make_id_prop("primvars:arnold:disp_padding", 0.0)[1]
    )

    disp_zero_value: bpy.props.FloatProperty(
        name="Displacement Zero Value",
        get=make_id_prop("primvars:arnold:disp_zero_value", 0.0)[0],
        set=make_id_prop("primvars:arnold:disp_zero_value", 0.0)[1]
    )

    invert_normals: bpy.props.BoolProperty(
        name="Invert Normals",
        get=make_id_prop("primvars:arnold:invert_normals", False)[0],
        set=make_id_prop("primvars:arnold:invert_normals", False)[1]
    )

    matte: bpy.props.BoolProperty(
        name="Matte",
        get=make_id_prop("primvars:arnold:matte", False)[0],
        set=make_id_prop("primvars:arnold:matte", False)[1]
    )

    min_pixel_width: bpy.props.FloatProperty(
        name="Min Pixel Width",
        get=make_id_prop("primvars:arnold:min_pixel_width", 0.0)[0],
        set=make_id_prop("primvars:arnold:min_pixel_width", 0.0)[1]
    )

    mipmap_bias: bpy.props.IntProperty(
        name="MipMap Bias",
        get=make_id_prop("primvars:arnold:mipmap_bias", 0)[0],
        set=make_id_prop("primvars:arnold:mipmap_bias", 0)[1]
    )

    mode: bpy.props.EnumProperty(
        name="Mode",
        items=[
            ("strip", "Strip", ""),
            ("ribbon", "Ribbon", ""),
            ("thick", "Thick", ""),
        ],
        get=make_enum_id_prop("primvars:arnold:mode", [("strip", "Strip", ""), ("ribbon", "Ribbon", ""), ("thick", "Thick", "")], "ribbon")[0],
        set=make_enum_id_prop("primvars:arnold:mode", [("strip", "Strip", ""), ("ribbon", "Ribbon", ""), ("thick", "Thick", "")], "ribbon")[1]
    )

    opaque: bpy.props.BoolProperty(
        name="Opaque",
        get=make_id_prop("primvars:arnold:opaque", False)[0],
        set=make_id_prop("primvars:arnold:opaque", False)[1]
    )

    radius: bpy.props.FloatProperty(
        name="Radius",
        get=make_id_prop("primvars:arnold:radius", 0.5)[0],
        set=make_id_prop("primvars:arnold:radius", 0.5)[1]
    )

    receive_shadows: bpy.props.BoolProperty(
        name="Receive Shadows",
        get=make_id_prop("primvars:arnold:receive_shadows", True)[0],
        set=make_id_prop("primvars:arnold:receive_shadows", True)[1]
    )
    
    self_shadows: bpy.props.BoolProperty(
        name="Self Shadows",
        get=make_id_prop("primvars:arnold:self_shadows", True)[0],
        set=make_id_prop("primvars:arnold:self_shadows", True)[1]
    )

    smoothing: bpy.props.BoolProperty(
        name="Smoothing",
        get=make_id_prop("primvars:arnold:smoothing", True)[0],
        set=make_id_prop("primvars:arnold:smoothing", True)[1]
    )

    step_size: bpy.props.FloatProperty(
        name="Step Size",
        get=make_id_prop("primvars:arnold:step_size", 0.0)[0],
        set=make_id_prop("primvars:arnold:step_size", 0.0)[1]
    )

    subdiv_adaptive_error: bpy.props.FloatProperty(
        name="Adaptive Error",
        get=make_id_prop("primvars:arnold:subdiv_adaptive_error", 0.0)[0],
        set=make_id_prop("primvars:arnold:subdiv_adaptive_error", 0.0)[1]
    )

    subdiv_adaptive_metric: bpy.props.EnumProperty(
        name="Adaptive Metric",
        items=[
            ("edge_length", "Edge Length", ""),
            ("flatness", "Flatness", ""),
            ("both", "Both", ""),
        ],
        get=make_enum_id_prop("primvars:arnold:subdiv_adaptive_metric", [("edge_length", "Edge Length", ""), ("flatness", "Flatness", ""), ("both", "Both", "")], "edge_length")[0],
        set=make_enum_id_prop("primvars:arnold:subdiv_adaptive_metric", [("edge_length", "Edge Length", ""), ("flatness", "Flatness", ""), ("both", "Both", "")], "edge_length")[1]
    )

    subdiv_adaptive_space: bpy.props.EnumProperty(
        name="Adaptive Space",
        items=AdaptiveSpace.items,
        get=make_enum_id_prop("primvars:arnold:subdiv_adaptive_space", AdaptiveSpace.items, "raster")[0],
        set=make_enum_id_prop("primvars:arnold:subdiv_adaptive_space", AdaptiveSpace.items, "raster")[1]
    )
    
    subdiv_frustum_ignore: bpy.props.BoolProperty(
        name="Frustum Ignore",
        get=make_id_prop("primvars:arnold:subdiv_frustum_ignore", False)[0],
        set=make_id_prop("primvars:arnold:subdiv_frustum_ignore", False)[1]
    )

    subdiv_iterations: bpy.props.IntProperty(
        name="Subdivision Iterations",
        get=make_id_prop("primvars:arnold:subdiv_iterations", 0)[0],
        set=make_id_prop("primvars:arnold:subdiv_iterations", 0)[1]
    )

    subdiv_smooth_derivs: bpy.props.BoolProperty(
        name="Smooth Derivatives",
        get=make_id_prop("primvars:arnold:subdiv_smooth_derivs", False)[0],
        set=make_id_prop("primvars:arnold:subdiv_smooth_derivs", False)[1]
    )

    subdiv_type: bpy.props.EnumProperty(
        name="Subdivision Type",
        items=SubdivType.items,
        get=make_enum_id_prop("primvars:arnold:subdiv_type", SubdivType.items, "none")[0],
        set=make_enum_id_prop("primvars:arnold:subdiv_type", SubdivType.items, "none")[1]
    )

    subdiv_uv_smoothing: bpy.props.EnumProperty(
        name="UV Smoothing",
        items=UVSmoothing.items,
        get=make_enum_id_prop("primvars:arnold:subdiv_uv_smoothing", UVSmoothing.items, "linear")[0],
        set=make_enum_id_prop("primvars:arnold:subdiv_uv_smoothing", UVSmoothing.items, "linear")[1]
    )

    trace_sets: bpy.props.CollectionProperty(
        type=ArnoldTraceSet
    )

    transform_keys: bpy.props.IntProperty(
        name="Transform Keys",
        get=make_id_prop("primvars:arnold:transform_keys", -1)[0],
        set=make_id_prop("primvars:arnold:transform_keys", -1)[1]
    )

    transform_type: bpy.props.EnumProperty(
        name="Transform Type",
        items=[
            ("linear", "Linear", "Linear interpolation"),
            ("step", "Step", "Step interpolation"),
            ("deform", "Deform", "Deformation blur"),
        ],
        get=make_enum_id_prop("primvars:arnold:transform_type", [("linear", "Linear", ""), ("step", "Step", ""), ("deform", "Deform", "")], "linear")[0],
        set=make_enum_id_prop("primvars:arnold:transform_type", [("linear", "Linear", ""), ("step", "Step", ""), ("deform", "Deform", "")], "linear")[1]
    )

    volume_padding: bpy.props.FloatProperty(
        name="Padding",
        get=make_id_prop("primvars:arnold:volume_padding", 0.0)[0],
        set=make_id_prop("primvars:arnold:volume_padding", 0.0)[1]
    )

    step_scale: bpy.props.FloatProperty(
        name="Step Scale",
        get=make_id_prop("primvars:arnold:step_scale", 1.0)[0],
        set=make_id_prop("primvars:arnold:step_scale", 1.0)[1]
    )
    default_radius: bpy.props.FloatProperty(
        name="Default Radius",
        get=make_id_prop("primvars:arnold:default_radius", 0.0)[0],
        set=make_id_prop("primvars:arnold:default_radius", 0.0)[1]
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
