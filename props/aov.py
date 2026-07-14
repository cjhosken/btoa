import bpy
from .render import ArnoldGlobalRenderProperties

# ---------------------------------------------------------------------------
# Filter type constants
# ---------------------------------------------------------------------------

_FILTERS_WIDTH = [
    ("blackman_harris_filter", "Blackman-Harris", ""),
    ("gaussian_filter",        "Gaussian",        ""),
    ("contour_filter",         "Contour",         ""),
    ("sinc_filter",            "Sinc",            ""),
    ("triangle_filter",        "Triangle",        ""),
]

_FILTERS_SIMPLE = [
    ("box_filter",      "Box",      ""),
    ("catmullrom_filter", "Catrom", ""),
    ("closest_filter",  "Closest",  ""),
    ("farthest_filter", "Farthest", ""),
    ("heatmap_filter",  "Heatmap",  ""),
    ("mitchell_filter", "Mitnet",   ""),
]

FILTER_ITEMS = _FILTERS_WIDTH + _FILTERS_SIMPLE
FILTERS_WITH_WIDTH = {f[0] for f in _FILTERS_WIDTH}


BUILTIN_AOVS = {
    "Beauty": [
        ("RGBA",  "Combined",           "box_filter",     "float"),
    ],
}


# ---------------------------------------------------------------------------
# ArnoldAovFilter — reusable filter property group
# ---------------------------------------------------------------------------

class ArnoldAovFilter(bpy.types.PropertyGroup):
    type: bpy.props.EnumProperty(
        name="Filter",
        items=FILTER_ITEMS,
        default="box_filter",
    )

    width: bpy.props.FloatProperty(
        name="Width",
        description="Filter kernel width",
        default=2.0, min=0.01, soft_max=10.0,
    )


# ---------------------------------------------------------------------------
# ArnoldCustomRenderVar — user-defined AOV
# ---------------------------------------------------------------------------

class ArnoldCustomRenderVar(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", default="custom_pass")

    source_name: bpy.props.StringProperty(
        name="Source",
        description="Arnold AOV source name",
        default="",
    )

    source_type: bpy.props.EnumProperty(
        name="Source Type",
        items=[
            ("raw",     "Raw",     ""),
            ("lpe",     "LPE",     ""),
            ("primvar", "Primvar", ""),
        ],
        default="raw",
    )

    data_type: bpy.props.EnumProperty(
        name="Data Type",
        items=[
            ("color4f", "RGBA (color4f)", ""),
            ("color3f", "RGB (color3f)",  ""),
            ("float3",  "Vector (float3)",""),
            ("float",   "Float",          ""),
            ("int",     "Int",            ""),
        ],
        default="color3f",
    )

    format: bpy.props.EnumProperty(
        name="Precision",
        items=[
            ("float", "Full (32-bit)",  ""),
            ("half",  "Half (16-bit)",  ""),
        ],
        default="float",
    )

    filter: bpy.props.PointerProperty(type=ArnoldAovFilter)


# ---------------------------------------------------------------------------
# Viewport shading properties & updates
# ---------------------------------------------------------------------------

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
    
    # Toggle shading mode to force Blender to recreate the Hydra session
    # and reload the updated AOV/RenderVar settings.
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D' and space.shading.type == 'RENDERED':
                        space.shading.type = 'SOLID'
                        space.shading.type = 'RENDERED'
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
    name="Output Variable AOVs",
    default=True
)


_FORMAT_ITEMS = [
    ("float", "Full (32-bit)", ""),
    ("half",  "Half (16-bit)", ""),
    ("int",   "Integer",       ""),
]

# Dynamically register built-in AOV properties on ArnoldGlobalRenderProperties
for cat, aovs in BUILTIN_AOVS.items():
    for name, label, def_filt, def_fmt in aovs:
        _default_enabled = (name == "RGBA")
        ArnoldGlobalRenderProperties.__annotations__[f"aov_{name}_enabled"] = bpy.props.BoolProperty(
            name=label,
            default=_default_enabled
        )
        ArnoldGlobalRenderProperties.__annotations__[f"aov_{name}_format"] = bpy.props.EnumProperty(
            name="Format",
            items=_FORMAT_ITEMS,
            default=def_fmt if def_fmt in {"float", "half", "int"} else "float"
        )
        ArnoldGlobalRenderProperties.__annotations__[f"aov_{name}_filter_type"] = bpy.props.EnumProperty(
            name="Filter",
            items=FILTER_ITEMS,
            default=def_filt
        )
        ArnoldGlobalRenderProperties.__annotations__[f"aov_{name}_filter_width"] = bpy.props.FloatProperty(
            name="Width",
            default=2.0,
            min=0.01,
            soft_max=10.0
        )



class ArnoldViewportShadingProperties(bpy.types.PropertyGroup):
    viewport_aov: bpy.props.EnumProperty(
        name="Render Pass",
        items=get_viewport_aov_items,
        default=0,
        update=update_viewport_aov
    )


def register():
    bpy.utils.register_class(ArnoldAovFilter)
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
    bpy.utils.unregister_class(ArnoldAovFilter)