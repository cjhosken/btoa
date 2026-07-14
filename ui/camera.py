import bpy

from ..engine import ArnoldHydraRenderEngine


class Panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.camera


class ARNOLD_HYDRA_CAMERA_PT_arnold(Panel):
    bl_label = "Arnold"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        cam = context.camera
        arnold = cam.arnold

class ARNOLD_HYDRA_CAMERA_PT_camera(bpy.types.Panel):
    bl_label = "Camera"
    bl_parent_id = "ARNOLD_HYDRA_CAMERA_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.camera

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.camera.arnold

        layout.prop(arnold, "exposure")
        layout.prop(arnold, "radial_distortion")
        layout.prop(arnold, "radial_distortion_type")
        layout.prop(arnold, "lens_tilt")
        layout.prop(arnold, "lens_shift")
        #layout.prop(arnold, "filtermap")
        #layout.prop(arnold, "uv_remap")


class ARNOLD_HYDRA_CAMERA_PT_motionblur(bpy.types.Panel):
    bl_label = "Motion Blur"
    bl_parent_id = "ARNOLD_HYDRA_CAMERA_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.camera

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.camera.arnold

        layout.prop(arnold, "shutter_filter")
        layout.prop(arnold, "rolling_shutter")
        layout.prop(arnold, "rolling_shutter_duration")


class ARNOLD_HYDRA_CAMERA_PT_dof(bpy.types.Panel):
    bl_label = "Depth of Field"
    bl_parent_id = "ARNOLD_HYDRA_CAMERA_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.camera

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.camera.arnold

        layout.prop(arnold, "aperture_blades")
        layout.prop(arnold, "aperture_rotation")
        layout.prop(arnold, "aperture_blade_curvature")
        layout.prop(arnold, "aperture_aspect_ratio")
        layout.prop(arnold, "flat_field_focus")

class ARNOLD_HYDRA_CAMERA_PT_override(bpy.types.Panel):
    bl_label = "Override Camera"
    bl_parent_id = "ARNOLD_HYDRA_CAMERA_PT_arnold"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES and context.camera

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        arnold = context.camera.arnold

        layout.prop(arnold, "camera")

        if arnold.camera == "cyl_camera":
            layout.prop(arnold, "cyl_camera_horizontal_fov")
            layout.prop(arnold, "cyl_camera_vertical_fov")
            layout.prop(arnold, "cyl_camera_projective")

        if arnold.camera == "vr_camera":
            layout.prop(arnold, "vr_camera_mode")
            layout.prop(arnold, "vr_camera_projection")
            layout.prop(arnold, "vr_camera_eye_separation")
            layout.prop(arnold, "vr_camera_eye_to_neck")
            layout.prop(arnold, "vr_camera_top_merge_mode")
            layout.prop(arnold, "vr_camera_top_merge_angle")
            layout.prop(arnold, "vr_camera_bottom_merge_mode")
            layout.prop(arnold, "vr_camera_bottom_merge_angle")
            layout.prop(arnold, "vr_camera_merge_shader")

        if arnold.camera == "uv_camera":
            #layout.prop(arnold, "uv_camera_mesh")
            layout.prop(arnold, "uv_camera_offset")
            layout.prop(arnold, "uv_camera_u_offset")
            layout.prop(arnold, "uv_camera_v_offset")
            #layout.prop(arnold, "uv_camera_uv_set")
            layout.prop(arnold, "uv_camera_u_scale")
            layout.prop(arnold, "uv_camera_v_scale")
            layout.prop(arnold, "uv_camera_extend_edges")


register_classes, unregister_classes = bpy.utils.register_classes_factory((
    ARNOLD_HYDRA_CAMERA_PT_arnold,
    ARNOLD_HYDRA_CAMERA_PT_camera,
    ARNOLD_HYDRA_CAMERA_PT_motionblur,
    ARNOLD_HYDRA_CAMERA_PT_dof,
    ARNOLD_HYDRA_CAMERA_PT_override,
))


def register():
    register_classes()


def unregister():
    unregister_classes()
