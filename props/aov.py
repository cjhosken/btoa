import bpy
from .render import ArnoldGlobalRenderProperties

AOV_TYPES = {
    "RGBA": "color4f",

    "A": "float",
    "Z": "float",
    "ZBack": "float",
    "volume_Z": "float",
    "cputime": "float",
    "raycount": "float",
    "AA_inv_density": "float",  # uppercase: used as the BUILTIN_AOVS key / property name

    "P": "float3",
    "Pref": "float3",
    "N": "float3",
    "N_Denoise": "float3",
    "opacity": "color3f",
    "motionvector": "float2",

    "ID": "int",
    "object": "int",
    "shader": "int",
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
    "Standard": [
        ("RGBA", "RGBA", "gaussian_filter", "float"),
        ("A", "A", "gaussian_filter", "float"),
        ("P", "P", "closest_filter", "float"),
        ("Pref", "Pref", "closest_filter", "float"),
        ("N", "N", "closest_filter", "float"),
        ("N_Denoise", "N (Denoise)", "closest_filter", "float"),
        ("opacity", "Opacity", "gaussian_filter", "float"),
        ("Z", "Z", "closest_filter", "float"),
        ("ZBack", "Z (Back)", "closest_filter", "float"),
    ],
    "Lighting": [
        ("direct", "Direct", "gaussian_filter", "float"),
        ("indirect", "Indirect", "gaussian_filter", "float"),
        ("emission", "Emission", "gaussian_filter", "float"),
        ("background", "Background", "gaussian_filter", "float"),
        ("albedo", "Albedo", "gaussian_filter", "float"),
        ("denoise_albedo", "Denoise Albedo", "gaussian_filter", "float"),
        ("specular", "Specular", "gaussian_filter", "float"),
        ("specular_direct", "Specular Direct", "gaussian_filter", "float"),
        ("specular_indirect", "Specular Indirect", "gaussian_filter", "float"),
        ("specular_albedo", "Specular", "gaussian_filter", "float"),
        ("sss", "SSS", "gaussian_filter", "float"),
        ("sss_direct", "SSS Direct", "gaussian_filter", "float"),
        ("sss_indirect", "SSS Indirect", "gaussian_filter", "float"),
        ("sss_albedo", "SSS Albedo", "gaussian_filter", "float"),
        ("transmission", "Transmission", "gaussian_filter", "float"),
        ("transmission_direct", "Transmission Direct", "gaussian_filter", "float"),
        ("transmission_indirect", "Transmission Indirect", "gaussian_filter", "float"),
        ("transmission_albedo", "Transmission Albedo", "gaussian_filter", "float"),
        ("shadow_matte", "Shadow Matte", "gaussian_filter", "float"),
        ("diffuse", "Diffuse", "gaussian_filter", "float"),
        ("diffuse_direct", "Diffuse Direct", "gaussian_filter", "float"),
        ("diffuse_indirect", "Diffuse Indirect", "gaussian_filter", "float"),
        ("diffuse_albedo", "Diffuse Albedo", "gaussian_filter", "float"),
        ("coat", "Coat", "gaussian_filter", "float"),
        ("coat_direct", "Coat Direct", "gaussian_filter", "float"),
        ("coat_indirect", "Coat Indirect", "gaussian_filter", "float"),
        ("coat_albedo", "Coat Albedo", "gaussian_filter", "float"),
        ("sheen", "Sheen", "gaussian_filter", "float"),
        ("sheen_direct", "Sheen Direct", "gaussian_filter", "float"),
        ("sheen_indirect", "Sheen Indirect", "gaussian_filter", "float"),
        ("sheen_albedo", "Sheen Albedo", "gaussian_filter", "float")
    ],
    "Volume": [
        ("volume", "Volume", "gaussian_filter", "float"),
        ("volume_direct", "Volume Direct", "gaussian_filter", "float"),
        ("volume_indirect", "Volume Indirect", "gaussian_filter", "float"),
        ("volume_albedo", "Volume Albedo", "gaussian_filter", "float"),
        ("volume_opacity", "Volume Opacity", "gaussian_filter", "float"),
        ("volume_Z", "Volume Z", "closest_filter", "float")
    ],
    "Utility": [
        ("ID", "ID", "closest_filter", "half"),
        ("object", "Object", "closest_filter", "half"),
        ("shader", "Shader", "closest_filter", "half"),
        ("motionvector", "Motion Vector", "closest_filter", "float")
    ],
    "Diagnostic": [
        ("cputime", "CPU Time", "closest_filter", "float"),
        ("raycount", "Ray Count", "closest_filter", "float"),
        ("AA_inv_density", "AA Inv Density", "closest_filter", "float")
    ]
}


PASS_TYPES = {
    "color4f": (4, "RGBA", "COLOR"),
    "color3f": (3, "RGB", "COLOR"),
    "float3": (3, "XYZ", "VECTOR"),
    "float": (1, "X", "VALUE"),
    "half": (1, "X", "VALUE"),
    "int": (1, "X", "VALUE"),
    "uint": (1, "X", "VALUE"),
    "int64": (1, "X", "VALUE"),
}


DEFAULT_VIEWPORT_AOV = "RGBA"


annotations = ArnoldGlobalRenderProperties.__annotations__




def get_usd_aov_types(name, user_fmt):
    datatype = AOV_TYPES.get(name, "color3f")

    if datatype in {"float", "half", "int", "uint", "int64"}:
        datatype = "float"

    if user_fmt != "half":
        return datatype, datatype

    return datatype, {
        "color4f": "color4h",
        "color3f": "color3h",
        "float3": "half3",
        "float2": "half2",
        "float": "half",
    }[datatype]

def build_aov_settings(settings, engine_type):
    """
    Build Hydra render settings for Arnold AOV outputs.

    Returns a dictionary consumed by HydraRenderEngine.
    """

    result = {}

    if settings is None:
        return result

    is_viewport = (engine_type == "VIEWPORT")

    if is_viewport:
        result["aovToken:Combined"] = "color"
        result["aovDescriptor:Combined"] = create_aov_descriptor(
            source="RGBA",
            name="RGBA",
            datatype="color4f",
            fmt="color4f",
            clear=0.0,
            filt="box_filter"
        )
        result["aovToken:Depth"] = "depth"
        result["aovDescriptor:Depth"] = create_aov_descriptor(
            source="Z",
            name="Z",
            datatype="float",
            fmt="float",
            clear=1e30,
            filt="closest_filter"
        )
        return result

    # Loop over BUILTIN_AOVS to build final AOV configurations
    for group_name, aovs in BUILTIN_AOVS.items():
        for name, label, default_filter, default_format in aovs:
            enabled = getattr(settings, f"aov_{name}_enabled", False)
            if name == "RGBA":
                enabled = True

            if not enabled:
                continue

            user_format = getattr(settings, f"aov_{name}_format", default_format)
            filter_type = getattr(settings, f"aov_{name}_filter_type", default_filter)
            arnold_name = name
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
                filt=filter_type
            )

    return result


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
                default=(name in {"RGBA", "Z"})
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


register_classes, unregister_classes = bpy.utils.register_classes_factory([ArnoldAovFilter,])


def register():
    register_classes()


def unregister():
    unregister_classes()