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
    "ZBack": "Z",
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
    "ZBack": "float",
    "volume_Z": "float",
    "cputime": "float",
    "raycount": "float",
    "aa_inv_density": "float",

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
        ("RGBA", "RGBA", "box_filter", "float"),
        ("A", "A", "box_filter", "float"),
        ("P", "P", "box_filter", "float"),
        ("Pref", "Pref", "box_filter", "float"),
        ("N", "N", "box_filter", "float"),
        ("N_Denoise", "N (Denoise)", "box_filter", "float"),
        ("opacity", "Opacity", "box_filter", "float"),
        ("Z", "Z", "box_filter", "float"),
        ("ZBack", "Z (Back)", "box_filter", "float"),
    ],
    "Lighting": [
        ("direct", "Direct", "box_filter", "float"),
        ("indirect", "Indirect", "box_filter", "float"),
        ("emission", "Emission", "box_filter", "float"),
        ("background", "Background", "box_filter", "float"),
        ("albedo", "Albedo", "box_filter", "float"),
        ("denoise_albedo", "Denoise Albedo", "box_filter", "float"),
        ("specular", "Specular", "box_filter", "float"),
        ("specular_direct", "Specular Direct", "box_filter", "float"),
        ("specular_indirect", "Specular Indirect", "box_filter", "float"),
        ("specular_albedo", "Specular", "box_filter", "float"),
        ("sss", "SSS", "box_filter", "float"),
        ("sss_direct", "SSS Direct", "box_filter", "float"),
        ("sss_indirect", "SSS Indirect", "box_filter", "float"),
        ("sss_albedo", "SSS Albedo", "box_filter", "float"),
        ("transmission", "Transmission", "box_filter", "float"),
        ("transmission_direct", "Transmission Direct", "box_filter", "float"),
        ("transmission_indirect", "Transmission Indirect", "box_filter", "float"),
        ("transmission_albedo", "Transmission Albedo", "box_filter", "float"),
        ("shadow_matte", "Shadow Matte", "box_filter", "float"),
        ("diffuse", "Diffuse", "box_filter", "float"),
        ("diffuse_direct", "Diffuse Direct", "box_filter", "float"),
        ("diffuse_indirect", "Diffuse Indirect", "box_filter", "float"),
        ("diffuse_albedo", "Diffuse Albedo", "box_filter", "float"),
        ("coat", "Coat", "box_filter", "float"),
        ("coat_direct", "Coat Direct", "box_filter", "float"),
        ("coat_indirect", "Coat Indirect", "box_filter", "float"),
        ("coat_albedo", "Coat Albedo", "box_filter", "float"),
        ("sheen", "Sheen", "box_filter", "float"),
        ("sheen_direct", "Sheen Direct", "box_filter", "float"),
        ("sheen_indirect", "Sheen Indirect", "box_filter", "float"),
        ("sheen_albedo", "Sheen Albedo", "box_filter", "float")
    ],
    "Volume": [
        ("volume", "Volume", "box_filter", "float"),
        ("volume_direct", "Volume Direct", "box_filter", "float"),
        ("volume_indirect", "Volume Indirect", "box_filter", "float"),
        ("volume_albedo", "Volume Albedo", "box_filter", "float"),
        ("volume_opacity", "Volume Opacity", "box_filter", "float"),
        ("volume_Z", "Volume Z", "box_filter", "float")
    ],
    "Utility": [
        ("ID", "ID", "box_filter", "half"),
        ("object", "Object", "box_filter", "half"),
        ("shader", "Shader", "box_filter", "half"),
        ("motionvector", "Motion Vector", "box_filter", "float")
    ],
    "Diagnostic": [
        ("cputime", "CPU Time", "box_filter", "float"),
        ("raycount", "Ray Count", "box_filter", "float"),
        ("AA_inv_density", "AA Inv Density", "box_filter", "float")
    ]
}


PASS_TYPES = {
    "color4f": (4, "RGBA", "COLOR"),
    "color3f": (3, "RGB", "COLOR"),
    "float2": (2, "XY", "VECTOR"),
    "float3": (3, "XYZ", "VECTOR"),
    "int": (1, "X", "VALUE"),
    "uint": (1, "X", "VALUE"),
    "int64": (1, "X", "VALUE"),
}


DEFAULT_VIEWPORT_AOV = "RGBA"


annotations = ArnoldGlobalRenderProperties.__annotations__




def get_usd_aov_types(name, user_fmt):
    datatype = AOV_TYPES.get(name, "color3f")

    half = user_fmt == "half"

    formats = {
        "color4f": "color4h" if half else "color4f",
        "color3f": "color3h" if half else "color3f",
        "float3": "half3" if half else "float3",
        "float2": "half2" if half else "float2",
        "float": "half" if half else "float",
        "int": "int",
        "uint": "uint",
        "int64": "int",
    }

    return datatype, formats[datatype]



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