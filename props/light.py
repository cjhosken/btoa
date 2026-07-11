import bpy


class ArnoldLightProperties(bpy.types.PropertyGroup):
    samples: bpy.props.IntProperty(
        name="Samples",
        default=1, min=0, soft_max=100,
    )
    sampling_mode: bpy.props.EnumProperty(
        name="Sampling Mode",
        items=[
            ("IMPORTANCE", "Importance", ""),
            ("SHADE", "Shade All", ""),
        ],
        default="IMPORTANCE",
    )
    volume_samples: bpy.props.IntProperty(
        name="Volume Samples",
        default=1, min=0, soft_max=100,
    )
    roundness: bpy.props.FloatProperty(
        name="Roundness",
        default=0.0, min=0.0, max=1.0,
    )
    spread: bpy.props.FloatProperty(
        name="Spread",
        default=1.0, min=0.0, max=1.0,
    )
    soft_edge: bpy.props.FloatProperty(
        name="Soft Edge",
        default=0.0, min=0.0, max=1.0,
        subtype='FACTOR',
    )
    resolution: bpy.props.IntProperty(
        name="Resolution",
        default=0, min=0,
    )
    aspect_ratio: bpy.props.FloatProperty(
        name="Aspect Ratio",
        default=1.0, min=0.0, soft_max=10.0,
    )
    lens_radius: bpy.props.FloatProperty(
        name="Lens Radius",
        default=0.0, min=0.0,
        subtype='DISTANCE',
    )
    shadow_density: bpy.props.FloatProperty(
        name="Shadow Density",
        default=1.0, min=0.0, soft_max=10.0,
    )
    cast_volumetric_shadows: bpy.props.BoolProperty(
        name="Cast Volumetric Shadows",
        default=True,
    )
    max_bounces: bpy.props.IntProperty(
        name="Max Bounces",
        default=-1, min=-1, soft_max=100,
    )
    camera_contribution: bpy.props.FloatProperty(
        name="Camera",
        default=1.0, min=0.0, soft_max=10.0,
    )
    diffuse_contribution: bpy.props.FloatProperty(
        name="Diffuse",
        default=1.0, min=0.0, soft_max=10.0,
    )
    specular_contribution: bpy.props.FloatProperty(
        name="Specular",
        default=1.0, min=0.0, soft_max=10.0,
    )
    transmission_contribution: bpy.props.FloatProperty(
        name="Transmission",
        default=1.0, min=0.0, soft_max=10.0,
    )
    subsurface_contribution: bpy.props.FloatProperty(
        name="Subsurface",
        default=1.0, min=0.0, soft_max=10.0,
    )
    volume_contribution: bpy.props.FloatProperty(
        name="Volume",
        default=1.0, min=0.0, soft_max=10.0,
    )
    indirect_contribution: bpy.props.FloatProperty(
        name="Indirect",
        default=1.0, min=0.0, soft_max=10.0,
    )
    aov_light_group: bpy.props.StringProperty(
        name="AOV Light Group",
        default="",
    )
    dome_light: bpy.props.BoolProperty(
        name="Dome Light",
        description="Treat this light as a dome/environment light",
        default=False,
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
