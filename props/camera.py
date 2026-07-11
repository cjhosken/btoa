import bpy


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

    # Camera Type
    camera_type: bpy.props.EnumProperty(
        name="Camera Type",
        items=CameraType.items,
        default="persp_camera",
    )

    # Exposure
    exposure: bpy.props.FloatProperty(
        name="Exposure",
        default=0.0,
    )

    # Lens Distortion
    radial_distortion: bpy.props.FloatProperty(
        name="Radial Distortion",
        default=0.0,
    )
    lens_tilt: bpy.props.FloatVectorProperty(
        name="Lens Tilt",
        default=(0.0, 0.0, 0.0),
    )
    lens_shift: bpy.props.FloatVectorProperty(
        name="Lens Shift",
        default=(0.0, 0.0, 0.0),
    )

    # Shaders
    filtermap: bpy.props.StringProperty(
        name="Filtermap",
        description="Filtermap shader node path",
        default="",
    )
    uv_remap: bpy.props.StringProperty(
        name="UV Remap",
        description="UV remap shader node path",
        default="",
    )

    # Shutter / Motion Blur
    shutter_filter: bpy.props.EnumProperty(
        name="Shutter Filter",
        items=ShutterFilter.items,
        default="box",
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
        default="OFF",
    )
    rolling_shutter_duration: bpy.props.FloatProperty(
        name="Rolling Shutter Duration",
        default=0.0, min=0.0, max=1.0,
        subtype='FACTOR',
    )

    # Depth of Field / Aperture
    aperture_blades: bpy.props.IntProperty(
        name="Aperture Blades",
        default=0, min=0,
    )
    aperture_rotation: bpy.props.FloatProperty(
        name="Aperture Rotation",
        default=0.0,
        subtype='ANGLE',
    )
    aperture_blade_curvature: bpy.props.FloatProperty(
        name="Aperture Blade Curvature",
        default=0.0, min=0.0, max=1.0,
        subtype='FACTOR',
    )
    aperture_aspect_ratio: bpy.props.FloatProperty(
        name="Aperture Aspect Ratio",
        default=1.0, min=0.0, soft_max=2.0,
    )

    # Other
    flat_field_focus: bpy.props.BoolProperty(
        name="Flat Field Focus",
        default=False,
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
