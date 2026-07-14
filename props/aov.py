import bpy
from .render import ArnoldGlobalRenderProperties

ARNOLD_AOV_NAMES = {
    "RGBA": "RGBA",
    "A": "A",
    "P": "P",
    "Pref": "Pref",
    "N": "N",
    "N_Denoise": "N",
    "Opacity": "opacity",
    "Z": "Z",
    "Z_Back": "Z",
    "Denoise_Albedo": "denoise_albedo",
    "Specular_Direct": "specular_direct",
    "Specular_Indirect": "specular_indirect",
    "Specular_Albedo": "specular_albedo",
    "SSS_Albedo": "sss_albedo",
    "SSS_Direct": "sss_direct",
    "SSS_Indirect": "sss_indirect",
    "Transmission_Direct": "transmission_direct",
    "Transmission_Indirect": "transmission_indirect",
    "Transmission_Albedo": "transmission_albedo",
    "Shadow_Matte": "shadow_matte",
    "Diffuse_Direct": "diffuse_direct",
    "Diffuse_Indirect": "diffuse_indirect",
    "Diffuse_Albedo": "diffuse_albedo",
    "Coat_Direct": "coat_direct",
    "Coat_Indirect": "coat_indirect",
    "Coat_Albedo": "coat_albedo",
    "Sheen_Direct": "sheen_direct",
    "Sheen_Indirect": "sheen_indirect",
    "Sheen_Albedo": "sheen_albedo",
    "Volume_Z": "volume_z",
    "Volume_Albedo": "volume_albedo",
    "Volume_Direct": "volume_direct",
    "Volume_Indirect": "volume_indirect",
    "Volume_Opacity": "volume_opacity",
    "ID": "id",
    "Object": "object",
    "Shader": "shader",
    "Motion_Vector": "motionvector",
    "CPU_Time": "cpu_time",
    "Ray_Count": "ray_count",
    "AA_Inv_Density": "aa_inv_density",
}

AOV_TYPES = {
    "RGBA": "color4f",

    "A": "float",
    "Z": "float",
    "Z_Back": "float",
    "Volume_Z": "float",
    "CPU_Time": "float",
    "Ray_Count": "float",
    "AA_Inv_Density": "float",

    "P": "float3",
    "Pref": "float3",
    "N": "float3",
    "N_Denoise": "float3",
    "Motion_Vector": "float3",

    "ID": "int",
    "Object": "int",
    "Shader": "int",
}


FILTER_ITEMS = [
    ("blackman_harris_filter", "Blackman-Harris", ""),
    ("box_filter", "Box", ""),
    ("catmullrom_filter", "Catrom", ""),
    ("closest_filter", "Closest", ""),
    ("contour_filter", "Contour", ""),
    ("cryptomatte_filter", "Cryptomatte", ""),
    ("diff_filter", "Diff", ""),
    ("farthest_filter", "Farthest", ""),
    ("gaussian_filter", "Gaussian", ""),
    ("heatmap_filter", "Heatmap", ""),
    ("mitchell_filter", "Mitnet", ""),
    ("sinc_filter", "Sinc", ""),
    ("triangle_filter", "Triangle", ""),
    ("variance_filter", "Variance", ""),
]


FORMAT_ITEMS = [
    ("float", "32-bit", ""),
    ("half", "16-bit", ""),
]


BUILTIN_AOVS = {
    "Beauty": [
        ("RGBA", "RGBA", "box_filter", "float"),
    ],
}


PASS_TYPES = {
    "color4f": (4, "RGBA", "COLOR"),
    "color3f": (3, "RGB", "COLOR"),
    "float3": (3, "XYZ", "VECTOR"),
    "int": (1, "X", "VALUE"),
}


DEFAULT_VIEWPORT_AOV = "RGBA"


annotations = ArnoldGlobalRenderProperties.__annotations__


def recreate_hydra_sessions(context):
    """Force Blender to recreate Hydra viewport render sessions."""
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type != 'VIEW_3D':
                continue

            for space in area.spaces:
                if space.type == 'VIEW_3D' and space.shading.type == 'RENDERED':
                    space.shading.type = 'SOLID'
                    space.shading.type = 'RENDERED'
            area.tag_redraw()


def refresh_scene(context):
    """Trigger dependency graph updates."""
    arnold = getattr(context.scene.arnold, "global", None)
    if arnold:
        arnold.viewport_update_trigger ^= True

    viewport = getattr(context.scene.arnold, "viewport", None)
    if viewport:
        viewport.viewport_update_trigger ^= True

    context.view_layer.update()

    if context.scene.world:
        context.scene.world.update_tag()


def update_viewport_aov(self, context):
    if context is None:
        return

    refresh_scene(context)
    recreate_hydra_sessions(context)


def get_viewport_aov_items(self, context):
    items = [
        (DEFAULT_VIEWPORT_AOV, "Combined (RGBA)", ""),
    ]

    if not context or not context.scene:
        return items

    arnold = getattr(context.scene.arnold, "global", None)
    if not arnold:
        return items

    for aovs in BUILTIN_AOVS.values():
        for name, label, *_ in aovs:
            if (
                name != DEFAULT_VIEWPORT_AOV
                and getattr(arnold, f"aov_{name}_enabled", False)
            ):
                items.append((name, label, ""))

    return items

def get_active_viewport_aov():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type != "VIEW_3D":
                continue

            space = area.spaces.active

            if space.shading.type == "RENDERED":
                return space.shading.arnold.viewport_aov

    return DEFAULT_VIEWPORT_AOV


def get_usd_aov_types(name, user_fmt):
    datatype = AOV_TYPES.get(name, "color3f")

    half = user_fmt == "half"

    formats = {
        "color4f": "color4h" if half else "color4f",
        "color3f": "color3h" if half else "color3f",
        "float3": "half3" if half else "float3",
        "float": "float16" if half else "float",
        "int": "int",
    }

    return datatype, formats[datatype]


def register_aov_passes(scene, render_layer):
    """
    Hydra delegates create the actual AOV buffers.
    Blender only needs the pass names registered.
    """

    for group_name, aovs in BUILTIN_AOVS.items():

        for name, label, *_ in aovs:

            if name == "RGBA":
                continue

            if name not in render_layer.passes:
                render_layer.passes.new(
                    name,
                    name,
                    "RGBA"
                )


def build_aov_settings(settings, engine_type):
    """
    Build Hydra render settings for Arnold AOV outputs.

    Returns a dictionary consumed by HydraRenderEngine.
    """

    result = {}

    if settings is None:
        return result

    is_viewport = (engine_type == "VIEWPORT")

    # Resolve which AOV is routed to viewport display buffer
    active_aov = "RGBA"
    if is_viewport:
        try:
            found = False
            for window in bpy.context.window_manager.windows:
                for area in window.screen.areas:
                    if area.type == 'VIEW_3D':
                        space = area.spaces.active
                        if space and space.type == 'VIEW_3D' and space.shading.type == 'RENDERED':
                            active_aov = space.shading.arnold.viewport_aov
                            found = True
                            break
                if found:
                    break
        except Exception:
            pass

    # Loop over BUILTIN_AOVS to build viewport and final AOV configurations
    for group_name, aovs in BUILTIN_AOVS.items():
        for name, label, default_filter, default_format in aovs:
            if is_viewport:
                if name == "RGBA":
                    # Map beauty Combined pass onto the active viewport AOV
                    arnold_name = get_arnold_source_name(active_aov)
                    result["aovToken:Combined"] = "color"
                    if active_aov == "Z":
                        filt = getattr(settings, "aov_Z_filter_type", "closest_filter")
                    elif active_aov == "A":
                        filt = getattr(settings, "aov_A_filter_type", "box_filter")
                    else:
                        filt = getattr(settings, f"aov_{active_aov}_filter_type", "box_filter")

                    result["aovDescriptor:Combined"] = create_aov_descriptor(
                        source=arnold_name,
                        name="RGBA",
                        datatype="color4f",
                        fmt="color4f",
                        clear=1e30 if active_aov == "Z" else 0.0,
                        filt=filter_to_arnold_string(filt)
                    )
                elif name == "Z" and active_aov != "Z":
                    result["aovToken:Depth"] = "depth"
                    result["aovDescriptor:Depth"] = create_aov_descriptor(
                        source="Z",
                        name="Z",
                        datatype="float",
                        fmt="float",
                        clear=1e30,
                        filt="closest_filter"
                    )
            else:
                enabled = getattr(settings, f"aov_{name}_enabled", False)
                if name == "RGBA":
                    enabled = True

                if not enabled:
                    continue

                user_format = getattr(settings, f"aov_{name}_format", default_format)
                filter_type = getattr(settings, f"aov_{name}_filter_type", default_filter)
                arnold_name = get_arnold_source_name(name)
                datatype, fmt = get_usd_aov_types(name, user_format)

                bl_name = 'Combined' if name == 'RGBA' else ('Depth' if name == 'Z' else label)
                token_val = 'color' if name == 'RGBA' else ('depth' if name == 'Z' else arnold_name)

                result[f"aovToken:{bl_name}"] = token_val
                result[f"aovDescriptor:{bl_name}"] = create_aov_descriptor(
                    source=arnold_name,
                    name=bl_name,
                    datatype=datatype,
                    fmt=fmt,
                    clear=1e30 if name == "Z" else 0.0,
                    filt=filter_to_arnold_string(filter_type)
                )

    return result


def get_arnold_source_name(name):
    return ARNOLD_AOV_NAMES.get(name, name.lower())


def filter_to_arnold_string(filter_type):
    return filter_type or "box_filter"


def create_aov_descriptor(
    source,
    name,
    datatype,
    fmt,
    clear,
    filt,
):
    return {
        "sourceName": source,
        "sourceType": "raw",
        "dataType": datatype,
        "driver:parameters:aov:name": name,
        "driver:parameters:aov:format": fmt,
        "driver:parameters:aov:clearValue": clear,
        "driver:parameters:aov:multiSampled": False,
        "arnold:filter": filt,
    }


def register_builtin_aovs():
    annotations["viewport_update_trigger"] = bpy.props.BoolProperty(
        description="Internal trigger property used to force viewport updates",
        default=False,
    )

    for aovs in BUILTIN_AOVS.values():
        for name, label, default_filter, default_format in aovs:
            annotations[f"aov_{name}_enabled"] = bpy.props.BoolProperty(
                name=label,
                description="Enable this built-in Arbitrary Output Variable (AOV) for output",
                default=(name == DEFAULT_VIEWPORT_AOV)
            )

            annotations[f"aov_{name}_format"] = bpy.props.EnumProperty(
                name="Format",
                description="Precision format of the output AOV (e.g. 16-bit half-float or 32-bit full-float)",
                items=FORMAT_ITEMS,
                default=default_format
            )

            annotations[f"aov_{name}_filter_type"] = bpy.props.EnumProperty(
                name="Filter",
                description="Reconstruction filter type used to combine samples into the final pixel color",
                items=FILTER_ITEMS,
                default=default_filter
            )


register_builtin_aovs()


class ArnoldAovFilter(bpy.types.PropertyGroup):
    type: bpy.props.EnumProperty(
        name="Filter",
        description="Reconstruction filter type used to combine samples into the final pixel color",
        items=FILTER_ITEMS,
        default="box_filter",
    )


class ArnoldViewportShadingProperties(bpy.types.PropertyGroup):
    viewport_aov: bpy.props.EnumProperty(
        name="Render Pass",
        description="Active Render Pass / AOV to display in the viewport",
        items=get_viewport_aov_items,
        default=0,
        update=update_viewport_aov
    )


register_classes, unregister_classes = bpy.utils.register_classes_factory([ArnoldAovFilter, ArnoldViewportShadingProperties,])


def register():
    register_classes()

    if not hasattr(bpy.types.View3DShading, "arnold"):
        bpy.types.View3DShading.arnold = bpy.props.PointerProperty(
            type=ArnoldViewportShadingProperties
        )


def unregister():
    if hasattr(bpy.types.View3DShading, "arnold"):
        del bpy.types.View3DShading.arnold

    unregister_classes()