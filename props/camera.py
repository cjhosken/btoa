import bpy

from .utils import make_id_prop, make_vector_id_prop, make_enum_id_prop


class CameraType:
    items = (
        ("persp_camera", "Perspective", "Standard perspective camera"),
        ("ortho_camera", "Orthographic", "Orthographic camera"),
        ("uv_camera", "UV", "UV camera"),
        ("cyl_camera", "Cylindrical", "Cylindrical camera"),
        ("fisheye_camera", "Fisheye", "Fisheye camera"),
    )


class ShutterFilter:
    items = (
        ("box", "Box", ""),
        ("triangle", "Triangle", ""),
        ("gaussian", "Gaussian", ""),
        ("blackman_harris", "Blackman-Harris", ""),
        ("sinc", "Sinc", ""),
    )


class ArnoldCameraProperties(bpy.types.PropertyGroup):

    aperture_aspect_ratio: bpy.props.FloatProperty(
        name="Aperture Aspect Ratio",
        default=1.0, min=0.0, soft_max=2.0,
        get=make_id_prop("primvars:arnold:aperture_aspect_ratio", 1.0)[0],
        set=make_id_prop("primvars:arnold:aperture_aspect_ratio", 1.0)[1]
    )

    aperture_blade_curvature: bpy.props.FloatProperty(
        name="Aperture Blade Curvature",
        default=0.0, min=0.0, max=1.0,
        subtype='FACTOR',
        get=make_id_prop("primvars:arnold:aperture_blade_curvature", 0.0)[0],
        set=make_id_prop("primvars:arnold:aperture_blade_curvature", 0.0)[1]
    )

    aperture_blades: bpy.props.IntProperty(
        name="Aperture Blades",
        default=0, min=0,
        get=make_id_prop("primvars:arnold:aperture_blades", 0)[0],
        set=make_id_prop("primvars:arnold:aperture_blades", 0)[1]
    )

    aperture_rotation: bpy.props.FloatProperty(
        name="Aperture Rotation",
        default=0.0,
        subtype='ANGLE',
        get=make_id_prop("primvars:arnold:aperture_rotation", 0.0)[0],
        set=make_id_prop("primvars:arnold:aperture_rotation", 0.0)[1]
    )

    # Camera Type
    camera_type: bpy.props.EnumProperty(
        name="Camera Type",
        items=CameraType.items,
        get=make_enum_id_prop("primvars:arnold:camera_type", CameraType.items, "persp_camera")[0],
        set=make_enum_id_prop("primvars:arnold:camera_type", CameraType.items, "persp_camera")[1]
    )

    # Exposure
    exposure: bpy.props.FloatProperty(
        name="Exposure",
        default=0.0,
        get=make_id_prop("primvars:arnold:exposure", 0.0)[0],
        set=make_id_prop("primvars:arnold:exposure", 0.0)[1]
    )

    filtermap: bpy.props.StringProperty(
        name="Filtermap",
        description="Filtermap shader node path",
        default="",
        get=make_id_prop("primvars:arnold:filtermap", "")[0],
        set=make_id_prop("primvars:arnold:filtermap", "")[1]
    )

    flat_field_focus: bpy.props.BoolProperty(
        name="Flat Field Focus",
        default=False,
        get=make_id_prop("primvars:arnold:flat_field_focus", False)[0],
        set=make_id_prop("primvars:arnold:flat_field_focus", False)[1]
    )

    # Lens Distortion
    
    lens_shift: bpy.props.FloatVectorProperty(
        name="Lens Shift",
        default=(0.0, 0.0, 0.0),
        get=make_vector_id_prop("primvars:arnold:lens_shift", (0.0, 0.0, 0.0))[0],
        set=make_vector_id_prop("primvars:arnold:lens_shift", (0.0, 0.0, 0.0))[1]
    )

    lens_tilt: bpy.props.FloatVectorProperty(
        name="Lens Tilt",
        default=(0.0, 0.0, 0.0),
        get=make_vector_id_prop("primvars:arnold:lens_tilt", (0.0, 0.0, 0.0))[0],
        set=make_vector_id_prop("primvars:arnold:lens_tilt", (0.0, 0.0, 0.0))[1]
    )

    radial_distortion: bpy.props.FloatProperty(
        name="Radial Distortion",
        default=0.0,
        get=make_id_prop("primvars:arnold:radial_distortion", 0.0)[0],
        set=make_id_prop("primvars:arnold:radial_distortion", 0.0)[1]
    )

    radial_distortion_type: bpy.props.EnumProperty(
        name="Radial Distortion Type",
        items=[
            ("cubic", "Cubic", ""),
            ("quadratic", "Quadratic", ""),
        ],
        get=make_enum_id_prop("primvars:arnold:radial_distortion_type", [("cubic", "Cubic", ""), ("quadratic", "Quadratic", "")], "cubic")[0],
        set=make_enum_id_prop("primvars:arnold:radial_distortion_type", [("cubic", "Cubic", ""), ("quadratic", "Quadratic", "")], "cubic")[1]
    )

    rolling_shutter: bpy.props.EnumProperty(
        name="Rolling Shutter",
        items=[
            ("OFF", "Off", ""),
            ("TOP", "Top", ""),
            ("BOTTOM", "Bottom", ""),
            ("LEFT", "Left", ""),
            ("RIGHT", "Right", ""),
        ],
        get=make_enum_id_prop("primvars:arnold:rolling_shutter", [("OFF", "Off", ""), ("TOP", "Top", ""), ("BOTTOM", "Bottom", ""), ("LEFT", "Left", ""), ("RIGHT", "Right", "")], "OFF")[0],
        set=make_enum_id_prop("primvars:arnold:rolling_shutter", [("OFF", "Off", ""), ("TOP", "Top", ""), ("BOTTOM", "Bottom", ""), ("LEFT", "Left", ""), ("RIGHT", "Right", "")], "OFF")[1]
    )

    rolling_shutter_duration: bpy.props.FloatProperty(
        name="Rolling Shutter Duration",
        default=0.0, min=0.0, max=1.0,
        subtype='FACTOR',
        get=make_id_prop("primvars:arnold:rolling_shutter_duration", 0.0)[0],
        set=make_id_prop("primvars:arnold:rolling_shutter_duration", 0.0)[1]
    )

    # Shutter / Motion Blur
    shutter_filter: bpy.props.EnumProperty(
        name="Shutter Filter",
        items=ShutterFilter.items,
        get=make_enum_id_prop("primvars:arnold:shutter_filter", ShutterFilter.items, "box")[0],
        set=make_enum_id_prop("primvars:arnold:shutter_filter", ShutterFilter.items, "box")[1]
    )
    
    uv_remap: bpy.props.StringProperty(
        name="UV Remap",
        description="UV remap shader node path",
        default="",
        get=make_id_prop("primvars:arnold:uv_remap", "")[0],
        set=make_id_prop("primvars:arnold:uv_remap", "")[1]
    )


def register():
    bpy.utils.register_class(ArnoldCameraProperties)

    if not hasattr(bpy.types.Camera, "arnold"):
        bpy.types.Camera.arnold = bpy.props.PointerProperty(
            name="Arnold",
            description="Arnold camera properties",
            type=ArnoldCameraProperties,
        )


def unregister():
    if hasattr(bpy.types.Camera, "arnold"):
        del bpy.types.Camera.arnold

    bpy.utils.unregister_class(ArnoldCameraProperties)
