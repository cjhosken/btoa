import bpy

from ..engine import ArnoldHydraRenderEngine


class ArnoldCameraPanel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.camera
    
    def setup(self, context):
        layout = self.layout
        layout.use_property_split = True
        settings = context.camera.arnold
        return layout, settings


class ARNOLD_HYDRA_CAMERA_PT_arnold(ArnoldCameraPanel):
    bl_label = "Arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        pass


class ARNOLD_HYDRA_CAMERA_PT_camera(ArnoldCameraPanel):
    bl_label = "Camera"
    bl_parent_id = "ARNOLD_HYDRA_CAMERA_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "exposure")
        layout.prop(settings, "radial_distortion")
        layout.prop(settings, "radial_distortion_type")
        layout.prop(settings, "lens_tilt")
        layout.prop(settings, "lens_shift")
        #layout.prop(arnold, "filtermap")
        #layout.prop(arnold, "uv_remap")


class ARNOLD_HYDRA_CAMERA_PT_motion_blur(ArnoldCameraPanel):
    bl_label = "Motion Blur"
    bl_parent_id = "ARNOLD_HYDRA_CAMERA_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "shutter_filter")
        layout.prop(settings, "rolling_shutter")
        layout.prop(settings, "rolling_shutter_duration")


class ARNOLD_HYDRA_CAMERA_PT_depth_of_field(ArnoldCameraPanel):
    bl_label = "Depth of Field"
    bl_parent_id = "ARNOLD_HYDRA_CAMERA_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "aperture_blades")
        layout.prop(settings, "aperture_rotation")
        layout.prop(settings, "aperture_blade_curvature")
        layout.prop(settings, "aperture_aspect_ratio")
        layout.prop(settings, "flat_field_focus")


class ARNOLD_HYDRA_CAMERA_PT_override(ArnoldCameraPanel):
    bl_label = "Override Camera"
    bl_parent_id = "ARNOLD_HYDRA_CAMERA_PT_arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout, settings = self.setup(context)

        layout.prop(settings, "camera")

        if settings.camera == "cyl_camera":
            layout.prop(settings, "cyl_camera_horizontal_fov")
            layout.prop(settings, "cyl_camera_vertical_fov")
            layout.prop(settings, "cyl_camera_projective")

        elif settings.camera == "vr_camera":
            layout.prop(settings, "vr_camera_mode")
            layout.prop(settings, "vr_camera_projection")
            layout.prop(settings, "vr_camera_eye_separation")
            layout.prop(settings, "vr_camera_eye_to_neck")
            layout.prop(settings, "vr_camera_top_merge_mode")
            layout.prop(settings, "vr_camera_top_merge_angle")
            layout.prop(settings, "vr_camera_bottom_merge_mode")
            layout.prop(settings, "vr_camera_bottom_merge_angle")
            layout.prop(settings, "vr_camera_merge_shader")

        elif settings.camera == "uv_camera":
            #layout.prop(arnold, "uv_camera_mesh")
            layout.prop(settings, "uv_camera_offset")
            layout.prop(settings, "uv_camera_u_offset")
            layout.prop(settings, "uv_camera_v_offset")
            #layout.prop(arnold, "uv_camera_uv_set")
            layout.prop(settings, "uv_camera_u_scale")
            layout.prop(settings, "uv_camera_v_scale")
            layout.prop(settings, "uv_camera_extend_edges")


register, unregister = bpy.utils.register_classes_factory((
    ARNOLD_HYDRA_CAMERA_PT_arnold,
    ARNOLD_HYDRA_CAMERA_PT_camera,
    ARNOLD_HYDRA_CAMERA_PT_motion_blur,
    ARNOLD_HYDRA_CAMERA_PT_depth_of_field,
    ARNOLD_HYDRA_CAMERA_PT_override,
))
