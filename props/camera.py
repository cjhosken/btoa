import bpy
from ..usd import USDProperty


class ArnoldCameraProperties(bpy.types.PropertyGroup):

    ### Camera

    exposure: USDProperty(
        name="Exposure",
        description="Exposure value for the camera. Increase to make the image brighter",
        usd="primvars:arnold:exposure",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=-100.0, soft_max=100.0
    )

    radial_distortion: USDProperty(
        name="Radial Distortion",
        description="Radial distortion coefficient",
        usd="primvars:arnold:radial_distortion",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=-0.2, soft_max=2.0
    )

    radial_distortion_type: USDProperty(
        name="Radial Distortion Type",
        description="Type of radial distortion (Cubic or Cubic Inverse)",
        usd="primvars:arnold:radial_distortion_type",
        type=bpy.props.EnumProperty,
        items=[
            ("cubic", "Cubic", ""),
            ("cubic_inverse", "Cubic Inverse", ""),
        ],
        default="cubic",
    )

    lens_tilt: USDProperty(
        name="Lens Tilt",
        description="Tilt angle of the lens in degrees (horizontal, vertical)",
        usd="primvars:arnold:lens_tilt",
        type=bpy.props.FloatVectorProperty,
        default=(0.0, 0.0, 0.0),
    )

    lens_shift: USDProperty(
        name="Lens Shift",
        description="Horizontal and vertical shift of the lens",
        usd="primvars:arnold:lens_shift",
        type=bpy.props.FloatVectorProperty,
        default=(0.0, 0.0, 0.0),
    )

    filtermap: USDProperty(
        name="Filter Map",
        description="",
        usd="primvars:arnold:filtermap",
        type=bpy.props.StringProperty,
        default=0.0, soft_min=-0.2, soft_max=2.0
    )

    uv_remap: USDProperty(
        name="UV Remap",
        description="",
        usd="primvars:arnold:uv_remap",
        type=bpy.props.StringProperty
    )

    ### Motion Blur

    shutter_filter: USDProperty(
        name="Shutter Filter",
        description="Curve defining the shutter opening/closing profile",
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
        description="Rolling shutter direction",
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
        description="Duration of the rolling shutter sweep (fraction of the frame duration)",
        usd="primvars:arnold:rolling_shutter_duration",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=1.0,
        subtype='FACTOR',
    )

    ### Depth of Field

    aperture_blades: USDProperty(
        name="Aperture Blades",
        description="Number of blades in the camera aperture (0 for circular)",
        usd="primvars:arnold:aperture_blades",
        type=bpy.props.IntProperty,
        default=0, soft_min=0, soft_max=40
    )

    aperture_rotation: USDProperty(
        name="Aperture Rotation",
        description="Rotation of the aperture blades",
        usd="primvars:arnold:aperture_rotation",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=360.0,
        subtype='ANGLE',
    )

    aperture_blade_curvature: USDProperty(
        name="Aperture Blade Curvature",
        description="Curvature of the aperture blades",
        usd="primvars:arnold:aperture_blade_curvature",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=-20.0, soft_max=20.0,
        subtype='FACTOR',
    )

    aperture_aspect_ratio: USDProperty(
        name="Aperture Aspect Ratio",
        description="Aspect ratio of the aperture",
        usd="primvars:arnold:aperture_aspect_ratio",
        type=bpy.props.FloatProperty,
        default=1.0, soft_min=0.0, soft_max=1.0,
    )

    flat_field_focus: USDProperty(
        name="Flat Field Focus",
        description="Enable flat field focus instead of spherical",
        usd="primvars:arnold:flat_field_focus",
        type=bpy.props.BoolProperty,
        default=True,
    )

    ### Override Camera

    camera: USDProperty(
        name="Camera Type",
        description="Select Arnold camera type",
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
        description="Horizontal field of view (FOV) for cylindrical camera",
        usd="primvars:arnold:horizontal_fov",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=1e+09
    )

    cyl_camera_vertical_fov: USDProperty(
        name="Vertical FOV",
        description="Vertical field of view (FOV) for cylindrical camera",
        usd="primvars:arnold:vertical_fov",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=1e+09
    )

    cyl_camera_projective: USDProperty(
        name="Projective",
        description="Projective mode for cylindrical camera",
        usd="primvars:arnold:projective",
        type=bpy.props.BoolProperty,
        default=True
    )

    vr_camera_mode : USDProperty(
        name="Mode",
        description="VR stereo rendering mode",
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
        description="VR projection type (Latlong or Cubemap)",
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
        description="Interpupillary distance (eye separation) for VR rendering",
        usd="primvars:arnold:eye_separation",
        type=bpy.props.FloatProperty,
        default=0.65, soft_min=0.0, soft_max=1.0
    )

    vr_camera_eye_to_neck : USDProperty(
        name="Eye To Neck",
        description="Distance from the eyes to the center of neck rotation",
        usd="primvars:arnold:eye_to_neck",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=1.0
    )

    vr_camera_top_merge_mode : USDProperty(
        name="Camera Type",
        description="Merge mode towards the top pole",
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
        description="Start angle for top pole merging",
        usd="primvars:arnold:top_merge_angle",
        type=bpy.props.FloatProperty,
        default=90.0, soft_min=0.0, soft_max=180.0
    )

    vr_camera_bottom_merge_mode : USDProperty(
        name="Camera Type",
        description="Merge mode towards the bottom pole",
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
        description="Start angle for bottom pole merging",
        usd="primvars:arnold:bottom_merge_angle",
        type=bpy.props.FloatProperty,
        default=90.0, soft_min=0.0, soft_max=180.0
    )

    vr_camera_merge_shader : USDProperty(
        name="Merge Shader",
        description="Exponent of the cosine merge shader",
        usd="primvars:arnold:merge_shader",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=10.0
    )

    uv_camera_mesh : USDProperty(
        name="Mesh",
        description="",
        usd="primvars:arnold:mesh",
        type=bpy.props.StringProperty,
        default=""
    )

    uv_camera_offset : USDProperty(
        name="Offset",
        description="Offset of the camera ray along the normal",
        usd="primvars:arnold:offset",
        type=bpy.props.FloatProperty,
        default=0.1, soft_min=0.0, soft_max=10.0
    )

    uv_camera_u_offset : USDProperty(
        name="U Offset",
        description="U texture coordinate offset",
        usd="primvars:arnold:u_offset",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=10.0
    )

    uv_camera_v_offset : USDProperty(
        name="V Offset",
        description="V texture coordinate offset",
        usd="primvars:arnold:v_offset",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=10.0
    )

    uv_camera_uv_set : USDProperty(
        name="UV Set",
        description="",
        usd="primvars:arnold:uv_set",
        type=bpy.props.StringProperty,
        default=""
    )

    uv_camera_u_scale : USDProperty(
        name="U Scale",
        description="U texture coordinate scale",
        usd="primvars:arnold:u_scale",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=10.0
    )

    uv_camera_v_scale : USDProperty(
        name="V Scale",
        description="V texture coordinate scale",
        usd="primvars:arnold:v_scale",
        type=bpy.props.FloatProperty,
        default=0.0, soft_min=0.0, soft_max=10.0
    )

    uv_camera_extend_edges : USDProperty(
        name="Extend Edges",
        description="Extend edges of the UV shell to prevent seam artifacts",
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
