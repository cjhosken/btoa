import bpy

from ..usd import USDProperty

class ArnoldLightProperties(bpy.types.PropertyGroup):
    ### Light

    samples: USDProperty(
        name="Samples",
        usd="primvars:arnold:samples",
        type=bpy.props.IntProperty,
        default=1, min=0, soft_max=8,
    )

    sampling_mode: USDProperty(
        name="Sampling Mode",
        usd="primvars:arnold:sampling_mode",
        type=bpy.props.EnumProperty,
        items=[
            ("auto", "Auto", ""),
            ("local", "Local", ""),
        ],
        default="auto",
    )

    volume_samples: USDProperty(
        name="Volume Samples",
        usd="primvars:arnold:volume_samples",
        type=bpy.props.IntProperty,
        default=2, min=0, soft_max=8,
    )

    roundness: USDProperty(
        name="Roundness",
        usd="primvars:arnold:roundness",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, max=1.0,
    )

    angle: USDProperty(
        name="Angle",
        usd="primvars:arnold:angle",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=90.0,
    )

    spread: USDProperty(
        name="Spread",
        usd="primvars:arnold:spread",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, max=1,
    )

    soft_edge: USDProperty(
        name="Soft Edge",
        usd="primvars:arnold:soft_edge",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, max=1.0,
    )

    portal: USDProperty(
        name="Potal",
        usd="primvars:arnold:portal",
        type=bpy.props.BoolProperty,
        default=False,
    )

    portal_mode: USDProperty(
        name="Portal Mode",
        usd="primvars:arnold:portal_mode",
        type=bpy.props.EnumProperty,
        items=[
            ("off", "Off", ""),
            ("interior_only", "Interior Only", ""),
            ("interior_exterior", "Interior Exterior", "")
        ],
        default="off",
    )

    resolution: USDProperty(
        name="Resolution",
        usd="primvars:arnold:resolution",
        type=bpy.props.IntProperty,
        default=512, min=0, soft_max=1024,
    )

    aspect_ratio: USDProperty(
        name="Aspect Ratio",
        usd="primvars:arnold:aspect_ratio",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=20.0,
    )

    lens_radius: USDProperty(
        name="Lens Radius",
        usd="primvars:arnold:lens_radius",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=10.0,
        subtype='DISTANCE',
    )

    aov_indirect: USDProperty(
        name="AOV Indirect",
        usd="primvars:arnold:aov_indirect",
        type=bpy.props.BoolProperty,
        default=False,
    )

    ### Shadows

    shadow_color: USDProperty(
        name="Shadow Color",
        usd="primvars:arnold:shadow_color",
        type=bpy.props.FloatVectorProperty,
        subtype='COLOR', default=(0.0, 0.0, 0.0), min=0.0, max=1.0,
    )

    shadow_density: USDProperty(
        name="Shadow Density",
        usd="primvars:arnold:shadow_density",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, max=1.0,
    )

    cast_shadows: USDProperty(
        name="Cast Shadows",
        usd="primvars:arnold:cast_shadows",
        type=bpy.props.BoolProperty,
        default=True,
    )

    cast_volumetric_shadows: USDProperty(
        name="Cast Volumetric Shadows",
        usd="primvars:arnold:cast_volumetric_shadows",
        type=bpy.props.BoolProperty,
        default=True,
    )

    ### Contribution

    camera: USDProperty(
        name="Camera",
        usd="primvars:arnold:camera",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0,
    )

    diffuse: USDProperty(
        name="Diffuse",
        usd="primvars:arnold:diffuse",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0,
    )

    specular: USDProperty(
        name="Specular",
        usd="primvars:arnold:specular",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0,
    )

    transmission: USDProperty(
        name="Transmission",
        usd="primvars:arnold:transmission",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0,
    )

    sss: USDProperty(
        name="Subsurface",
        usd="primvars:arnold:sss",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0,
    )

    volume: USDProperty(
        name="Volume",
        usd="primvars:arnold:volume",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0,
    )

    indirect: USDProperty(
        name="Indirect",
        usd="primvars:arnold:indirect",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0,
    )

    max_bounces: USDProperty(
        name="Max Bounces",
        usd="primvars:arnold:max_bounces",
        type=bpy.props.IntProperty,
        default=999, min=0, soft_max=1000,
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
