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

        layout.prop(arnold, "camera_type")
        layout.prop(arnold, "exposure")


class ARNOLD_HYDRA_CAMERA_PT_lens(bpy.types.Panel):
    bl_label = "Lens"
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

        layout.prop(arnold, "radial_distortion")
        layout.prop(arnold, "radial_distortion_type")
        layout.prop(arnold, "lens_tilt")
        layout.prop(arnold, "lens_shift")


class ARNOLD_HYDRA_CAMERA_PT_shaders(bpy.types.Panel):
    bl_label = "Shaders"
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

        layout.prop(arnold, "filtermap")
        layout.prop(arnold, "uv_remap")


class ARNOLD_HYDRA_CAMERA_PT_shutter(bpy.types.Panel):
    bl_label = "Shutter / Motion Blur"
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


register_classes, unregister_classes = bpy.utils.register_classes_factory((
    ARNOLD_HYDRA_CAMERA_PT_arnold,
    ARNOLD_HYDRA_CAMERA_PT_lens,
    ARNOLD_HYDRA_CAMERA_PT_shaders,
    ARNOLD_HYDRA_CAMERA_PT_shutter,
    ARNOLD_HYDRA_CAMERA_PT_dof,
))


def register():
    register_classes()


def unregister():
    unregister_classes()
