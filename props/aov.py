import bpy
from .render import ArnoldGlobalRenderProperties

BUILTIN_AOVS = {
    "STANDARD": [
        ("RGBA", "RGBA", "box_filter", "float"),
        ("A", "A", "box_filter", "float"),
        ("P", "P", "box_filter", "float"),
        ("Pref", "Pref", "box_filter", "float"),
        ("N", "N", "box_filter", "float"),
        ("N_Denoise", "N (Denoise)", "box_filter", "float"),
        ("Opacity", "Opacity", "box_filter", "float"),
        ("Z", "Z", "closest_filter", "float"),
        ("Z_Back", "Z (Back)", "closest_filter", "float"),
    ],
    "LIGHTING": [
        ("Direct", "Direct", "box_filter", "float"),
        ("Indirect", "Indirect", "box_filter", "float"),
        ("Emission", "Emission", "box_filter", "float"),
        ("Background", "Background", "box_filter", "float"),
        ("Albedo", "Albedo", "box_filter", "float"),
        ("Denoise_Albedo", "Denoise Albedo", "box_filter", "float"),
        ("Specular", "Specular", "box_filter", "float"),
        ("Specular_Direct", "Specular Direct", "box_filter", "float"),
        ("Specular_Indirect", "Specular Indirect", "box_filter", "float"),
        ("Specular_Albedo", "Specular Albedo", "box_filter", "float"),
        ("SSS", "SSS", "box_filter", "float"),
        ("SSS_Albedo", "SSS Albedo", "box_filter", "float"),
        ("SSS_Direct", "SSS Direct", "box_filter", "float"),
        ("SSS_Indirect", "SSS Indirect", "box_filter", "float"),
        ("Transmission", "Transmission", "box_filter", "float"),
        ("Transmission_Direct", "Transmission Direct", "box_filter", "float"),
        ("Transmission_Indirect", "Transmission Indirect", "box_filter", "float"),
        ("Transmission_Albedo", "Transmission Albedo", "box_filter", "float"),
        ("Shadow_Matte", "Shadow Matte", "box_filter", "float"),
        ("Diffuse", "Diffuse", "box_filter", "float"),
        ("Diffuse_Direct", "Diffuse Direct", "box_filter", "float"),
        ("Diffuse_Indirect", "Diffuse Indirect", "box_filter", "float"),
        ("Diffuse_Albedo", "Diffuse Albedo", "box_filter", "float"),
        ("Coat", "Coat", "box_filter", "float"),
        ("Coat_Direct", "Coat Direct", "box_filter", "float"),
        ("Coat_Indirect", "Coat Indirect", "box_filter", "float"),
        ("Coat_Albedo", "Coat Albedo", "box_filter", "float"),
        ("Sheen", "Sheen", "box_filter", "float"),
        ("Sheen_Direct", "Sheen Direct", "box_filter", "float"),
        ("Sheen_Indirect", "Sheen Indirect", "box_filter", "float"),
        ("Sheen_Albedo", "Sheen Albedo", "box_filter", "float"),
    ],
    "VOLUME": [
        ("Volume", "Volume", "box_filter", "float"),
        ("Volume_Z", "Volume Z", "box_filter", "float"),
        ("Volume_Albedo", "Volume Albedo", "box_filter", "float"),
        ("Volume_Direct", "Volume Direct", "box_filter", "float"),
        ("Volume_Indirect", "Volume Indirect", "box_filter", "float"),
        ("Volume_Opacity", "Volume Opacity", "box_filter", "float"),
    ],
    "UTILITY": [
        ("ID", "ID", "box_filter", "half"),
        ("Object", "Object", "box_filter", "half"),
        ("Shader", "Shader", "box_filter", "half"),
        ("Motion_Vector", "Motion Vector", "closest_filter", "float"),
    ],
    "DIAGNOSTIC": [
        ("CPU_Time", "CPU Time", "box_filter", "float"),
        ("Ray_Count", "Ray Count", "box_filter", "float"),
        ("AA_Inv_Density", "AA Inv Density", "box_filter", "float"),
    ],
}

class ArnoldCustomRenderVar(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="custom_pass")
    format: bpy.props.EnumProperty(
        name="Format",
        items=[
            ("float", "float", ""),
            ("color2f", "color2f", ""),
            ("color3f", "color3f", ""),
            ("color4f", "color4f", ""),
            ("float2", "float2", ""),
            ("float3", "float3", ""),
            ("float4", "float4", ""),
            ("half", "half", ""),
            ("float16", "float16", ""),
            ("color2h", "color2h", ""),
            ("color3h", "color3h", ""),
            ("half2", "half2", ""),
            ("half3", "half3", ""),
            ("half4", "half4", ""),
            ("u8", "u8", ""),
            ("uint8", "uint8", ""),
            ("color2u8", "color2u8", ""),
            ("color3u8", "color3u8", ""),
            ("color4u8", "color4u8", ""),
            ("i8", "i8", ""),
            ("int8", "int8", ""),
            ("color2i8", "color2i8", ""),
            ("color3i8", "color3i8", ""),
            ("color4i8", "color4i8", ""),
            ("int", "int", ""),
            ("int2", "int2", ""),
            ("int3", "int3", ""),
            ("int4", "int4", ""),
            ("uint", "uint", ""),
            ("uint2", "uint2", ""),
            ("uint3", "uint3", ""),
            ("uint4", "uint4", ""),
        ],
        default="float"
    )
    data_type: bpy.props.EnumProperty(
        name="Data Type",
        items=[
            ("auto", "Auto", ""),
            ("bool", "bool", ""),
            ("int", "int", ""),
            ("int64", "int64", ""),
            ("float", "float", ""),
            ("double", "double", ""),
            ("string", "string", ""),
            ("token", "token", ""),
            ("asset", "asset", ""),
            ("half2", "half2", ""),
            ("float2", "float2", ""),
            ("double2", "double2", ""),
            ("int3", "int3", ""),
            ("half3", "half3", ""),
            ("float3", "float3", ""),
            ("double3", "double3", ""),
            ("point3f", "point3f", ""),
            ("point3d", "point3d", ""),
            ("normal3f", "normal3f", ""),
            ("normal3d", "normal3d", ""),
            ("vector3f", "vector3f", ""),
            ("vector3d", "vector3d", ""),
            ("color3f", "color3f", ""),
            ("color3d", "color3d", ""),
            ("color4f", "color4f", ""),
            ("color4d", "color4d", ""),
            ("texCoord2f", "texCoord2f", ""),
            ("texCoord3f", "texCoord3f", ""),
            ("int4", "int4", ""),
            ("half4", "half4", ""),
            ("float4", "float4", ""),
            ("double4", "double4", ""),
            ("quath", "quath", ""),
            ("quatf", "quatf", ""),
            ("quatd", "quatd", ""),
        ],
        default="color3f"
    )
    source_name: bpy.props.StringProperty(name="Source Name", default="")
    source_type: bpy.props.EnumProperty(
        name="Source Type",
        items=[
            ("raw", "Raw", ""),
            ("primvar", "Primvar", ""),
            ("lpe", "LPE", ""),
            ("intrinsic", "Intrinsic", "")
        ],
        default="raw"
    )
    filter: bpy.props.EnumProperty(
        name="Filter",
        items=[
            ("blackman_harris_filter", "Blackman Harris", ""),
            ("box_filter", "Box", ""),
            ("catrom_filter", "Catrom", ""),
            ("closest_filter", "Closest", ""),
            ("contour_filter", "Contour", ""),
            ("cryptomatte_filter", "Cryptommatte", ""),
            ("diff_filter", "Diff", ""),
            ("farthest_filter", "Farthest", ""),
            ("gaussian_filter", "Gaussian", ""),
            ("heatmap_filter", "Heatmap", ""),
            ("mitnet_filter", "Mitnet", ""),
            ("sync_filter", "Sync", ""),
            ("triangle_filter", "Triangle", ""),
            ("variance_filter", "Variance", ""),
        ],
        default="box_filter"
    )

def update_viewport_aov(self, context):
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


def get_viewport_aov_items(self, context):
    items = [("RGBA", "Combined (RGBA)", "")]
    if context and context.scene:
        arnold = getattr(context.scene.arnold, "global", None)
        if arnold:
            for cat, aovs in BUILTIN_AOVS.items():
                for name, label, def_filt, def_fmt in aovs:
                    if name == "RGBA":
                        continue
                    if getattr(arnold, f"aov_{name}_enabled", False):
                        items.append((name, label, ""))
            for item in arnold.custom_render_vars:
                if item.name:
                    items.append((item.name, item.name, ""))
    return items

# Dynamically add custom_render_vars and custom_active_index
ArnoldGlobalRenderProperties.__annotations__["custom_render_vars"] = bpy.props.CollectionProperty(
    type=ArnoldCustomRenderVar
)
ArnoldGlobalRenderProperties.__annotations__["custom_active_index"] = bpy.props.IntProperty(
    name="Active Custom Render Var Index",
    default=0
)

# Dynamically add viewport_update_trigger for viewport updates
ArnoldGlobalRenderProperties.__annotations__["viewport_update_trigger"] = bpy.props.BoolProperty(
    default=False
)

# Dynamically add global output_variable_aovs flag
ArnoldGlobalRenderProperties.__annotations__["output_variable_aovs"] = bpy.props.BoolProperty(
    name="Output Variabe AOVs",
    default=True
)

# Dynamically register built-in AOV properties on ArnoldGlobalRenderProperties
for cat, aovs in BUILTIN_AOVS.items():
    for name, label, def_filt, def_fmt in aovs:
        ArnoldGlobalRenderProperties.__annotations__[f"aov_{name}_enabled"] = bpy.props.BoolProperty(
            name=label,
            default=(name == "RGBA" or name == "Z")
        )
        ArnoldGlobalRenderProperties.__annotations__[f"aov_{name}_filter"] = bpy.props.EnumProperty(
            name="Filter",
            items=[
                ("blackman_harris_filter", "Blackman Harris", ""),
                ("box_filter", "Box", ""),
                ("catrom_filter", "Catrom", ""),
                ("closest_filter", "Closest", ""),
                ("contour_filter", "Contour", ""),
                ("cryptomatte_filter", "Cryptommatte", ""),
                ("diff_filter", "Diff", ""),
                ("farthest_filter", "Farthest", ""),
                ("gaussian_filter", "Gaussian", ""),
                ("heatmap_filter", "Heatmap", ""),
                ("mitnet_filter", "Mitnet", ""),
                ("sync_filter", "Sync", ""),
                ("triangle_filter", "Triangle", ""),
                ("variance_filter", "Variance", ""),
            ],
            default=def_filt
        )
        ArnoldGlobalRenderProperties.__annotations__[f"aov_{name}_format"] = bpy.props.EnumProperty(
            name="Format",
            items=[
                ("float", "32-bit", ""),
                ("half", "16-bit", ""),
            ],
            default=def_fmt
        )
        ArnoldGlobalRenderProperties.__annotations__[f"aov_{name}_filter_width"] = bpy.props.FloatProperty(
            name="Filter Width",
            default=2.0,
            min=0.0
        )


class ArnoldViewportShadingProperties(bpy.types.PropertyGroup):
    viewport_aov: bpy.props.EnumProperty(
        name="Render Pass",
        items=get_viewport_aov_items,
        default=0,
        update=update_viewport_aov
    )


def register():
    bpy.utils.register_class(ArnoldCustomRenderVar)
    bpy.utils.register_class(ArnoldViewportShadingProperties)

    if not hasattr(bpy.types.View3DShading, "arnold"):
        bpy.types.View3DShading.arnold = bpy.props.PointerProperty(
            type=ArnoldViewportShadingProperties
        )


def unregister():
    if hasattr(bpy.types.View3DShading, "arnold"):
        del bpy.types.View3DShading.arnold

    bpy.utils.unregister_class(ArnoldViewportShadingProperties)
    bpy.utils.unregister_class(ArnoldCustomRenderVar)