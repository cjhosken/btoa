import bpy
from .render import ArnoldGlobalRenderProperties

# ---------------------------------------------------------------------------
# Filter type constants
# ---------------------------------------------------------------------------

FILTER_ITEMS = [
    ("blackman_harris_filter", "Blackman-Harris", ""),
    ("box_filter",             "Box",             ""),
    ("catmullrom_filter",      "Catrom",          ""),
    ("closest_filter",         "Closest",         ""),
    ("contour_filter",         "Contour",         ""),
    ("cryptomatte_filter",     "Cryptomatte",     ""),
    ("diff_filter",            "Diff",            ""),
    ("farthest_filter",        "Farthest",        ""),
    ("gaussian_filter",        "Gaussian",        ""),
    ("heatmap_filter",         "Heatmap",         ""),
    ("mitchell_filter",        "Mitnet",          ""),
    ("sinc_filter",            "Sinc",            ""),
    ("triangle_filter",        "Triangle",        ""),
    ("variance_filter",        "Variance",        ""),
]


BUILTIN_AOVS = {
    "Beauty": [
        ("RGBA",  "RGBA",           "box_filter",     "float"),
    ],
}


# ---------------------------------------------------------------------------
# ArnoldAovFilter — reusable filter property group
# ---------------------------------------------------------------------------

class ArnoldAovFilter(bpy.types.PropertyGroup):
    type: bpy.props.EnumProperty(
        name="Filter",
        description="Reconstruction filter type used to combine samples into the final pixel color",
        items=FILTER_ITEMS,
        default="box_filter",
    )




# ---------------------------------------------------------------------------
# ArnoldCustomRenderVar — user-defined AOV
# ---------------------------------------------------------------------------




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
    return items


# Dynamically add viewport_update_trigger for viewport updates
ArnoldGlobalRenderProperties.__annotations__["viewport_update_trigger"] = bpy.props.BoolProperty(
    description="Internal trigger property used to force viewport render session re-initialization on changes",
    default=False
)


_FORMAT_ITEMS = [
    ("float", "Full (32-bit)", ""),
    ("half",  "Half (16-bit)", ""),
]

# Dynamically register built-in AOV properties on ArnoldGlobalRenderProperties
for cat, aovs in BUILTIN_AOVS.items():
    for name, label, def_filt, def_fmt in aovs:
        _default_enabled = (name == "RGBA")
        ArnoldGlobalRenderProperties.__annotations__[f"aov_{name}_enabled"] = bpy.props.BoolProperty(
            name=label,
            description="Enable this built-in Arbitrary Output Variable (AOV) for output",
            default=_default_enabled
        )
        ArnoldGlobalRenderProperties.__annotations__[f"aov_{name}_format"] = bpy.props.EnumProperty(
            name="Format",
            description="Precision format of the output AOV (e.g. 16-bit half-float or 32-bit full-float)",
            items=_FORMAT_ITEMS,
            default=def_fmt if def_fmt in {"float", "half", "int"} else "float"
        )
        ArnoldGlobalRenderProperties.__annotations__[f"aov_{name}_filter_type"] = bpy.props.EnumProperty(
            name="Filter",
            description="Reconstruction filter type used to combine samples into the final pixel color",
            items=FILTER_ITEMS,
            default=def_filt
        )




class ArnoldViewportShadingProperties(bpy.types.PropertyGroup):
    viewport_aov: bpy.props.EnumProperty(
        name="Render Pass",
        description="Active Render Pass / AOV to display in the viewport",
        items=get_viewport_aov_items,
        default=0,
        update=update_viewport_aov
    )


def register():
    bpy.utils.register_class(ArnoldAovFilter)
    bpy.utils.register_class(ArnoldViewportShadingProperties)

    if not hasattr(bpy.types.View3DShading, "arnold"):
        bpy.types.View3DShading.arnold = bpy.props.PointerProperty(
            type=ArnoldViewportShadingProperties
        )


def unregister():
    if hasattr(bpy.types.View3DShading, "arnold"):
        del bpy.types.View3DShading.arnold

    bpy.utils.unregister_class(ArnoldViewportShadingProperties)
    bpy.utils.unregister_class(ArnoldAovFilter)