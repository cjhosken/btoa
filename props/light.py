import bpy

from .utils import make_id_prop, make_vector_id_prop, make_enum_id_prop


class ArnoldLightProperties(bpy.types.PropertyGroup):
    angle: bpy.props.FloatProperty(
        name="Angle",
        default=0.0, min=0.0, max=1.0,
        get=make_id_prop("primvars:arnold:angle", 0.0)[0],
        set=make_id_prop("primvars:arnold:angle", 0.0)[1]
    )

    aov_indirect: bpy.props.BoolProperty(
        name="AOV Indirect",
        default=False,
        get=make_id_prop("primvars:arnold:aov_indirect", False)[0],
        set=make_id_prop("primvars:arnold:aov_indirect", False)[1]
    )

    aspect_ratio: bpy.props.FloatProperty(
        name="Aspect Ratio",
        default=1.0, min=0.0, soft_max=10.0,
        get=make_id_prop("primvars:arnold:aspect_ratio", 1.0)[0],
        set=make_id_prop("primvars:arnold:aspect_ratio", 1.0)[1]
    )

    camera: bpy.props.FloatProperty(
        name="Camera",
        default=1.0, min=0.0, soft_max=10.0,
        get=make_id_prop("primvars:arnold:camera", 1.0)[0],
        set=make_id_prop("primvars:arnold:camera", 1.0)[1]
    )

    cast_shadows: bpy.props.BoolProperty(
        name="Cast Shadows",
        default=True,
        get=make_id_prop("primvars:arnold:cast_shadows", True)[0],
        set=make_id_prop("primvars:arnold:cast_shadows", True)[1]
    )

    cast_volumetric_shadows: bpy.props.BoolProperty(
        name="Cast Volumetric Shadows",
        default=True,
        get=make_id_prop("primvars:arnold:cast_volumetric_shadows", True)[0],
        set=make_id_prop("primvars:arnold:cast_volumetric_shadows", True)[1]
    )

    diffuse: bpy.props.FloatProperty(
        name="Diffuse",
        default=1.0, min=0.0, soft_max=10.0,
        get=make_id_prop("primvars:arnold:diffuse", 1.0)[0],
        set=make_id_prop("primvars:arnold:diffuse", 1.0)[1]
    )

    indirect: bpy.props.FloatProperty(
        name="Indirect",
        default=1.0, min=0.0, soft_max=10.0,
        get=make_id_prop("primvars:arnold:indirect", 1.0)[0],
        set=make_id_prop("primvars:arnold:indirect", 1.0)[1]
    )

    lens_radius: bpy.props.FloatProperty(
        name="Lens Radius",
        default=0.0, min=0.0,
        subtype='DISTANCE',
        get=make_id_prop("primvars:arnold:lens_radius", 0.0)[0],
        set=make_id_prop("primvars:arnold:lens_radius", 0.0)[1]
    )

    max_bounces: bpy.props.IntProperty(
        name="Max Bounces",
        default=999, min=0, soft_max=100,
        get=make_id_prop("primvars:arnold:max_bounces", 999)[0],
        set=make_id_prop("primvars:arnold:max_bounces", 999)[1]
    )

    portal: bpy.props.BoolProperty(
        name="Potal",
        default=False,
        get=make_id_prop("primvars:arnold:portal", False)[0],
        set=make_id_prop("primvars:arnold:portal", False)[1]
    )

    portal_mode: bpy.props.EnumProperty(
        name="Portal Mode",
        items=[
            ("off", "Off", ""),
            ("on", "On", ""),
            ("interior_only", "Interior Only", "")
        ],
        default="off",
        get=make_enum_id_prop("primvars:arnold:portal_mode", [("off", "Off", ""), ("on", "On", ""), ("interior_only", "Interior Only", "")], "off")[0],
        set=make_enum_id_prop("primvars:arnold:portal_mode", [("off", "Off", ""), ("on", "On", ""), ("interior_only", "Interior Only", "")], "off")[1]
    )

    resolution: bpy.props.IntProperty(
        name="Resolution",
        default=512, min=0, soft_max=1024,
        get=make_id_prop("primvars:arnold:resolution", 512)[0],
        set=make_id_prop("primvars:arnold:resolution", 512)[1]
    )

    roundness: bpy.props.FloatProperty(
        name="Roundness",
        default=0.0, min=0.0, max=1.0,
        get=make_id_prop("primvars:arnold:roundness", 0.0)[0],
        set=make_id_prop("primvars:arnold:roundness", 0.0)[1]
    )

    samples: bpy.props.IntProperty(
        name="Samples",
        default=1, min=0, soft_max=100,
        get=make_id_prop("primvars:arnold:samples", 1)[0],
        set=make_id_prop("primvars:arnold:samples", 1)[1]
    )

    sampling_mode: bpy.props.EnumProperty(
        name="Sampling Mode",
        items=[
            ("auto", "Auto", ""),
            ("IMPORTANCE", "Importance", ""),
            ("SHADE", "Shade All", ""),
        ],
        get=make_enum_id_prop("primvars:arnold:sampling_mode", [("auto", "Auto", ""), ("IMPORTANCE", "Importance", ""), ("SHADE", "Shade All", "")], "IMPORTANCE")[0],
        set=make_enum_id_prop("primvars:arnold:sampling_mode", [("auto", "Auto", ""), ("IMPORTANCE", "Importance", ""), ("SHADE", "Shade All", "")], "IMPORTANCE")[1]
    )

    shadow_color: bpy.props.FloatVectorProperty(
        name="Shadow Color", subtype='COLOR', default=(0.0, 0.0, 0.0), min=0.0, max=1.0,
        get=make_vector_id_prop("primvars:arnold:shadow_color", (0.0, 0.0, 0.0))[0],
        set=make_vector_id_prop("primvars:arnold:shadow_color", (0.0, 0.0, 0.0))[1]
    )

    shadow_density: bpy.props.FloatProperty(
        name="Shadow Density",
        default=1.0, min=0.0, soft_max=10.0,
        get=make_id_prop("primvars:arnold:shadow_density", 1.0)[0],
        set=make_id_prop("primvars:arnold:shadow_density", 1.0)[1]
    )

    soft_edge: bpy.props.FloatProperty(
        name="Soft Edge",
        default=0.0, min=0.0, soft_max=10.0,
        get=make_id_prop("primvars:arnold:soft_edge", 0.0)[0],
        set=make_id_prop("primvars:arnold:soft_edge", 0.0)[1]
    )

    specular: bpy.props.FloatProperty(
        name="Specular",
        default=1.0, min=0.0, soft_max=10.0,
        get=make_id_prop("primvars:arnold:specular", 1.0)[0],
        set=make_id_prop("primvars:arnold:specular", 1.0)[1]
    )

    spread: bpy.props.FloatProperty(
        name="Spread",
        default=1.0, min=0.0, soft_max=10.0,
        get=make_id_prop("primvars:arnold:spread", 1.0)[0],
        set=make_id_prop("primvars:arnold:spread", 1.0)[1]
    )

    sss: bpy.props.FloatProperty(
        name="Subsurface Scattering",
        default=1.0, min=0.0, soft_max=10.0,
        get=make_id_prop("primvars:arnold:sss", 1.0)[0],
        set=make_id_prop("primvars:arnold:sss", 1.0)[1]
    )

    transmission: bpy.props.FloatProperty(
        name="Transmission",
        default=1.0, min=0.0, soft_max=10.0,
        get=make_id_prop("primvars:arnold:transmission", 1.0)[0],
        set=make_id_prop("primvars:arnold:transmission", 1.0)[1]
    )

    volume: bpy.props.FloatProperty(
        name="Volume",
        default=1.0, min=0.0, soft_max=10.0,
        get=make_id_prop("primvars:arnold:volume", 1.0)[0],
        set=make_id_prop("primvars:arnold:volume", 1.0)[1]
    )

    volume_samples: bpy.props.IntProperty(
        name="Volume Samples",
        default=2, min=0, soft_max=100,
        get=make_id_prop("primvars:arnold:volume_samples", 2)[0],
        set=make_id_prop("primvars:arnold:volume_samples", 2)[1]
    )


def register():
    bpy.utils.register_class(ArnoldLightProperties)

    if not hasattr(bpy.types.Light, "arnold"):
        bpy.types.Light.arnold = bpy.props.PointerProperty(
            name="Arnold",
            description="Arnold light properties",
            type=ArnoldLightProperties,
        )


def unregister():
    if hasattr(bpy.types.Light, "arnold"):
        del bpy.types.Light.arnold

    bpy.utils.unregister_class(ArnoldLightProperties)
