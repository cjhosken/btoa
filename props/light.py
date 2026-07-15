import bpy
from ..usd import USDProperty


class ArnoldLightProperties(bpy.types.PropertyGroup):

    ### Light

    samples: USDProperty(
        name="Samples",
        description="Number of samples used to resolve soft shadows and direct lighting noise",
        usd="primvars:arnold:samples",
        type=bpy.props.IntProperty,
        default=1, soft_min=0, soft_max=8,
    )

    sampling_mode: USDProperty(
        name="Sampling Mode",
        description="Light sampling strategy (Auto or Local)",
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
        description="Number of samples used for direct lighting in volumes",
        usd="primvars:arnold:volume_samples",
        type=bpy.props.IntProperty,
        default=2, soft_min=0, soft_max=8,
    )

    roundness: USDProperty(
        name="Roundness",
        description="Controls the roundness of disc lights",
        usd="primvars:arnold:roundness",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=1.0,
    )

    angle: USDProperty(
        name="Angle",
        description="Angular diameter of the sun/distant light source (in degrees)",
        usd="primvars:arnold:angle",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=90.0,
    )

    spread: USDProperty(
        name="Spread",
        description="Emission angle spread (focus/concentration of light direction)",
        usd="primvars:arnold:spread",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1,
    )

    soft_edge: USDProperty(
        name="Soft Edge",
        description="Smoothness of the spotlight outer cone edge boundary",
        usd="primvars:arnold:soft_edge",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=1.0,
    )

    portal: USDProperty(
        name="Potal",
        description="Designate the light as a portal to guide indirect rays",
        usd="primvars:arnold:portal",
        type=bpy.props.BoolProperty,
        default=False,
    )

    portal_mode: USDProperty(
        name="Portal Mode",
        description="Portal evaluation strategy",
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
        description="Texture resolution used for dome light environment mapping",
        usd="primvars:arnold:resolution",
        type=bpy.props.IntProperty,
        default=512, soft_min=0, soft_max=1024,
    )

    aspect_ratio: USDProperty(
        name="Aspect Ratio",
        description="Aspect ratio of quad lights",
        usd="primvars:arnold:aspect_ratio",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=20.0,
    )

    lens_radius: USDProperty(
        name="Lens Radius",
        description="Lens radius for cylindrical light shapes",
        usd="primvars:arnold:lens_radius",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=10.0,
        subtype='DISTANCE',
    )

    aov_indirect: USDProperty(
        name="AOV Indirect",
        description="Whether indirect lighting from this light writes to separate light path expressions",
        usd="primvars:arnold:aov_indirect",
        type=bpy.props.BoolProperty,
        default=False,
    )

    ### Shadows

    shadow_color: USDProperty(
        name="Shadow Color",
        description="Tint color applied to shadows cast by this light",
        usd="primvars:arnold:shadow_color",
        type=bpy.props.FloatVectorProperty,
        subtype='COLOR', default=(0.0, 0.0, 0.0), soft_min=0.0, soft_max=1.0,
    )

    shadow_density: USDProperty(
        name="Shadow Density",
        description="Strength of the shadows cast by this light",
        usd="primvars:arnold:shadow_density",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0,
    )

    cast_shadows: USDProperty(
        name="Cast Shadows",
        description="Cast shadows from this light",
        usd="primvars:arnold:cast_shadows",
        type=bpy.props.BoolProperty,
        default=True,
    )

    cast_volumetric_shadows: USDProperty(
        name="Cast Volumetric Shadows",
        description="Cast volumetric shadows from this light",
        usd="primvars:arnold:cast_volumetric_shadows",
        type=bpy.props.BoolProperty,
        default=True,
    )

    ### Contribution

    camera: USDProperty(
        name="Camera",
        description="Luminance contribution scale factor for camera/beauty ray paths",
        usd="primvars:arnold:camera",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0,
    )

    diffuse: USDProperty(
        name="Diffuse",
        description="Luminance contribution scale factor for diffuse reflections",
        usd="primvars:arnold:diffuse",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0,
    )

    specular: USDProperty(
        name="Specular",
        description="Luminance contribution scale factor for specular/glossy reflections",
        usd="primvars:arnold:specular",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0,
    )

    transmission: USDProperty(
        name="Transmission",
        description="Luminance contribution scale factor for transmission/glass refraction paths",
        usd="primvars:arnold:transmission",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0,
    )

    sss: USDProperty(
        name="Subsurface",
        description="Luminance contribution scale factor for subsurface scattering paths",
        usd="primvars:arnold:sss",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0,
    )

    volume: USDProperty(
        name="Volume",
        description="Luminance contribution scale factor for volume scattering",
        usd="primvars:arnold:volume",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0,
    )

    indirect: USDProperty(
        name="Indirect",
        description="Luminance contribution scale factor for indirect lighting bounces",
        usd="primvars:arnold:indirect",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0,
    )

    max_bounces: USDProperty(
        name="Max Bounces",
        description="Maximum path bounce depth this light's rays will travel",
        usd="primvars:arnold:max_bounces",
        type=bpy.props.IntProperty,
        default=999, soft_min=0, soft_max=1000,
    )

    aov: USDProperty(
        name="AOV Light Group",
        description="",
        usd="primvars:arnold:aov",
        type=bpy.props.StringProperty,
        default=""
    )

    ### Contribution

    shaders: USDProperty(
        name="Shaders",
        description="",
        usd="primvars:arnold:shaders",
        type=bpy.props.StringProperty,
        default=""
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
