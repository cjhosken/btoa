import bpy


class RenderProperties(bpy.types.PropertyGroup):
    aa_samples: bpy.props.IntProperty(
        name="AA Samples",
        default=3, min=0,
    )
    aa_samples_max: bpy.props.IntProperty(
        name="AA Samples Max",
        default=20, min=0,
    )
    gi_diffuse_samples: bpy.props.IntProperty(
        name="Diffuse Samples",
        default=2, min=0,
    )
    gi_specular_samples: bpy.props.IntProperty(
        name="Specular Samples",
        default=2, min=0,
    )
    gi_transmission_samples: bpy.props.IntProperty(
        name="Transmission Samples",
        default=2, min=0,
    )
    gi_sss_samples: bpy.props.IntProperty(
        name="SSS Samples",
        default=2, min=0,
    )
    gi_volume_samples: bpy.props.IntProperty(
        name="Volume Samples",
        default=2, min=0,
    )
    gi_diffuse_depth: bpy.props.IntProperty(
        name="Diffuse Depth",
        default=1, min=0,
    )
    gi_specular_depth: bpy.props.IntProperty(
        name="Specular Depth",
        default=1, min=0,
    )
    gi_transmission_depth: bpy.props.IntProperty(
        name="Transmission Depth",
        default=8, min=0,
    )
    gi_volume_depth: bpy.props.IntProperty(
        name="Volume Depth",
        default=0, min=0,
    )
    gi_total_depth: bpy.props.IntProperty(
        name="Total Depth",
        default=10, min=0,
    )
    progressive_min_aa_samples: bpy.props.IntProperty(
        name="Progressive Min AA Samples",
        default=-4,
    )
    max_lights: bpy.props.IntProperty(
        name="Max Lights",
        default=16, min=0, max=16,
    )
    use_tiny_prim_culling: bpy.props.BoolProperty(
        name="Tiny Prim Culling",
        default=False,
    )
    volume_raymarching_step_size: bpy.props.FloatProperty(
        name="Volume Raymarching Step Size",
        default=1.0,
    )
    volume_raymarching_step_size_lighting: bpy.props.FloatProperty(
        name="Volume Raymarching Step Size Lighting",
        default=10.0,
    )
    volume_max_texture_memory_per_field: bpy.props.FloatProperty(
        name="Max Texture Memory Per Field",
        default=128.0,
    )


class SceneRenderProperties(bpy.types.PropertyGroup):
    final: bpy.props.PointerProperty(type=RenderProperties)
    viewport: bpy.props.PointerProperty(type=RenderProperties)


def register():
    bpy.utils.register_class(RenderProperties)
    bpy.utils.register_class(SceneRenderProperties)

    if not hasattr(bpy.types.Scene, "arnold"):
        bpy.types.Scene.arnold = bpy.props.PointerProperty(
            type=SceneRenderProperties
        )


def unregister():
    if hasattr(bpy.types.Scene, "arnold"):
        del bpy.types.Scene.arnold

    bpy.utils.unregister_class(SceneRenderProperties)
    bpy.utils.unregister_class(RenderProperties)
