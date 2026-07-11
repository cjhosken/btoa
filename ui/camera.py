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

        layout.separator()
        layout.label(text="Lens")
        layout.prop(arnold, "radial_distortion")
        layout.prop(arnold, "lens_tilt")
        layout.prop(arnold, "lens_shift")

        layout.separator()
        layout.label(text="Shaders")
        layout.prop(arnold, "filtermap")
        layout.prop(arnold, "uv_remap")

        layout.separator()
        layout.label(text="Shutter / Motion Blur")
        layout.prop(arnold, "shutter_filter")
        layout.prop(arnold, "rolling_shutter")
        layout.prop(arnold, "rolling_shutter_duration")

        layout.separator()
        layout.label(text="Depth of Field")
        layout.prop(arnold, "aperture_blades")
        layout.prop(arnold, "aperture_rotation")
        layout.prop(arnold, "aperture_blade_curvature")
        layout.prop(arnold, "aperture_aspect_ratio")

        layout.separator()
        layout.prop(arnold, "flat_field_focus")


def register():
    bpy.utils.register_class(ARNOLD_HYDRA_CAMERA_PT_arnold)


def unregister():
    bpy.utils.unregister_class(ARNOLD_HYDRA_CAMERA_PT_arnold)
