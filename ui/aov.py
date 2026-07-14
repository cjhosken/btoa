import bpy
from ..engine import ArnoldHydraRenderEngine

class ARNOLD_HYDRA_RENDER_PT_aovs(bpy.types.Panel):
    bl_label = "Render Vars"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'view_layer'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        from ..props.aov import BUILTIN_AOVS

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        r = getattr(context.scene.arnold, "global")
        if not r:
            return

        for cat, aovs in BUILTIN_AOVS.items():
            for name, label, def_filt, def_fmt in aovs:
                p           = f"aov_{name}"
                enabled_prop = f"{p}_enabled"
                ftype_prop   = f"{p}_filter_type"
                format_prop  = f"{p}_format"

                row = layout.row(align=True)
                row.prop(r, enabled_prop, text=label)

                enabled = getattr(r, enabled_prop, False)
                sub = row.row(align=True)
                sub.enabled = enabled
                sub.prop(r, ftype_prop, text="")
                sub.prop(r, format_prop, text="")


class ARNOLD_VIEW3D_PT_shading_render_pass(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = "Render Pass"
    bl_parent_id = "VIEW3D_PT_shading"
    COMPAT_ENGINES = {'ARNOLD'}

    @classmethod
    def poll(cls, context):
        return (
            context.space_data.shading.type == 'RENDERED' and
            context.engine == 'ARNOLD' and
            hasattr(context.space_data.shading, 'arnold')
        )

    def draw(self, context):
        shading = context.space_data.shading
        layout = self.layout
        layout.prop(shading.arnold, "viewport_aov", text="")


register_classes, unregister_classes = bpy.utils.register_classes_factory((
    ARNOLD_HYDRA_RENDER_PT_aovs,
    ARNOLD_VIEW3D_PT_shading_render_pass
))


def register():
    register_classes()


def unregister():
    unregister_classes()