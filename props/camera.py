import bpy

from ..usd import USDProperty

class ArnoldCameraProperties(bpy.types.PropertyGroup):

    ### Camera
    exposure: USDProperty(
        name="Exposure",
        usd="primvars:arnold:exposure",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=-100.0, soft_max=100.0
    )

    radial_distortion: USDProperty(
        name="Radial Distortion",
        usd="primvars:arnold:radial_distortion",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=-0.2, soft_max=2.0
    )

    radial_distortion_type: USDProperty(
        name="Radial Distortion Type",
        usd="primvars:arnold:radial_distortion_type",
        type=bpy.props.EnumProperty,
        items=[
            ("cubic", "Cubic", ""),
            ("cubic_inverse", "Cubic Inverse", ""),
        ],
        default="cubic",
    )

    ### Motion Blur

    shutter_filter: USDProperty(
        name="Shutter Filter",
        usd="primvars:arnold:shutter_filter",
        type=bpy.props.EnumProperty,
        items=[
            ("box", "Box", ""),
            ("triangle", "Triangle", ""),
            ("curve", "Curve", ""),
        ],
        default="box",
    )

    rolling_shutter: USDProperty(
        name="Rolling Shutter",
        usd="primvars:arnold:rolling_shutter",
        type=bpy.props.EnumProperty,
        items=[
            ("off", "Off", ""),
            ("top", "Top", ""),
            ("bottom", "Bottom", ""),
            ("left", "Left", ""),
            ("right", "Right", ""),
        ],
        default="off",
    )

    rolling_shutter_duration: USDProperty(
        name="Rolling Shutter Duration",
        usd="primvars:arnold:rolling_shutter_duration",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, max=1.0,
        subtype='FACTOR',
    )


    ### Depth of Field

    aperture_blades: USDProperty(
        name="Aperture Blades",
        usd="primvars:arnold:aperture_blades",
        type=bpy.props.IntProperty,
        default=0, min=0, soft_max=40
    )

    aperture_rotation: USDProperty(
        name="Aperture Rotation",
        usd="primvars:arnold:aperture_rotation",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, max=360.0,
        subtype='ANGLE',
    )

    aperture_blade_curvature: USDProperty(
        name="Aperture Blade Curvature",
        usd="primvars:arnold:aperture_blade_curvature",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=-20.0, soft_max=20.0,
        subtype='FACTOR',
    )

    aperture_aspect_ratio: USDProperty(
        name="Aperture Aspect Ratio",
        usd="primvars:arnold:aperture_aspect_ratio",
        type=bpy.props.FloatProperty,
        default=1.0, min=0.0, soft_max=1.0,
    )

    flat_field_focus: USDProperty(
        name="Flat Field Focus",
        usd="primvars:arnold:flat_field_focus",
        type=bpy.props.BoolProperty,
        default=True,
    )

    lens_tilt: USDProperty(
        name="Lens Tilt",
        usd="primvars:arnold:lens_tilt",
        type=bpy.props.FloatVectorProperty,
        default=(0.0, 0.0, 0.0),
    )

    lens_shift: USDProperty(
        name="Lens Shift",
        usd="primvars:arnold:lens_shift",
        type=bpy.props.FloatVectorProperty,
        default=(0.0, 0.0, 0.0),
    )

    ### Override Camera

    camera: USDProperty(
        name="Camera Type",
        usd="primvars:arnold:camera",
        type=bpy.props.EnumProperty,
        items=[
            ("persp_camera", "Perspective", "Standard perspective camera"),
            ("ortho_camera", "Orthographic", "Orthographic camera"),
            ("fisheye_camera", "Fisheye", "Fisheye camera"),
            ("cyl_camera", "Cylindrical", "Cylindrical camera"),
            ("spherical_camera", "Spherical", "Spherical camera"),
            ("vr_camera", "VR", "VR camera"),
            ("uv_camera", "UV", "UV camera"),
        ],
        default="persp_camera",
    )

    cyl_camera_horizontal_fov: USDProperty(
        name="Horizontal FOV",
        usd="primvars:arnold:horizontal_fov",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=1e+09
    )

    cyl_camera_vertical_fov: USDProperty(
        name="Vertical FOV",
        usd="primvars:arnold:vertical_fov",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=1e+09
    )

    cyl_camera_projective: USDProperty(
        name="Projective",
        usd="primvars:arnold:projective",
        type=bpy.props.BoolProperty,
        default=True
    )

    vr_camera_mode : USDProperty(
        name="Mode",
        usd="primvars:arnold:mode",
        type=bpy.props.EnumProperty,
        items=[
            ("side_by_side", "Side by Side", ""),
            ("over_under", "Over Under", ""),
            ("left_eye", "Left Eye", ""),
            ("right_eye", "Right Eye", ""),
        ],
        default="side_by_side",
    )

    vr_camera_projection : USDProperty(
        name="Projection",
        usd="primvars:arnold:projection",
        type=bpy.props.EnumProperty,
        items=[
            ("latlong", "Latlong", ""),
            ("cubemap_6x1", "Cubemap 6x1", ""),
            ("cubemap_3x2", "Cubemap 3x2", ""),
        ],
        default="latlong",
    )

    vr_camera_eye_separation : USDProperty(
        name="Eye Separation",
        usd="primvars:arnold:eye_separation",
        type=bpy.props.FloatProperty,
        default=0.65, min=0.0, soft_max=1.0
    )

    vr_camera_eye_to_neck : USDProperty(
        name="Eye To Neck",
        usd="primvars:arnold:eye_to_neck",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=1.0
    )

    vr_camera_top_merge_mode : USDProperty(
        name="Camera Type",
        usd="primvars:arnold:top_merge_mode",
        type=bpy.props.EnumProperty,
        items=[
            ("none", "None", ""),
            ("cosine", "Cosine", ""),
            ("shader", "Shader", ""),
        ],
        default="cosine",
    )

    vr_camera_top_merge_angle : USDProperty(
        name="Top Merge Angle",
        usd="primvars:arnold:top_merge_angle",
        type=bpy.props.FloatProperty,
        default=90.0, min=0.0, max=180.0
    )

    vr_camera_bottom_merge_mode : USDProperty(
        name="Camera Type",
        usd="primvars:arnold:bottom_merge_mode",
        type=bpy.props.EnumProperty,
        items=[
            ("none", "None", ""),
            ("cosine", "Cosine", ""),
            ("shader", "Shader", ""),
        ],
        default="cosine",
    )

    vr_camera_bottom_merge_angle : USDProperty(
        name="Bottom Merge Angle",
        usd="primvars:arnold:bottom_merge_angle",
        type=bpy.props.FloatProperty,
        default=90.0, min=0.0, max=180.0
    )

    vr_camera_merge_shader : USDProperty(
        name="Merge Shader",
        usd="primvars:arnold:merge_shader",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, max=10.0
    )

    uv_camera_offset : USDProperty(
        name="Offset",
        usd="primvars:arnold:offset",
        type=bpy.props.FloatProperty,
        default=0.1, min=0.0, soft_max=10.0
    )

    uv_camera_u_offset : USDProperty(
        name="U Offset",
        usd="primvars:arnold:u_offset",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=10.0
    )

    uv_camera_v_offset : USDProperty(
        name="V Offset",
        usd="primvars:arnold:v_offset",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=10.0
    )

    uv_camera_u_scale : USDProperty(
        name="U Scale",
        usd="primvars:arnold:u_scale",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=10.0
    )

    uv_camera_v_scale : USDProperty(
        name="V Scale",
        usd="primvars:arnold:v_scale",
        type=bpy.props.FloatProperty,
        default=0.0, min=0.0, soft_max=10.0
    )

    uv_camera_extend_edges : USDProperty(
        name="Extend Edges",
        usd="primvars:arnold:extend_edges",
        type=bpy.props.BoolProperty,
        default=True
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
