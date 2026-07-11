import bpy

from ..engine import ArnoldHydraRenderEngine


class Panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES


class ARNOLD_HYDRA_RENDER_PT_quality(Panel):
    bl_label = "Quality"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = context.scene.arnold.final

        col = layout.column(align=True)
        col.label(text="Sampling")
        col.prop(r, "aa_samples")
        col.prop(r, "aa_samples_max")
        col.prop(r, "progressive_min_aa_samples")

        col.separator()
        col.label(text="Ray Depth")
        col.prop(r, "gi_diffuse_depth")
        col.prop(r, "gi_specular_depth")
        col.prop(r, "gi_transmission_depth")
        col.prop(r, "gi_volume_depth")
        col.prop(r, "gi_total_depth")

        col.separator()
        col.label(text="GI Samples")
        col.prop(r, "gi_diffuse_samples")
        col.prop(r, "gi_specular_samples")
        col.prop(r, "gi_transmission_samples")
        col.prop(r, "gi_sss_samples")
        col.prop(r, "gi_volume_samples")

        col.separator()
        col.label(text="Performance")
        col.prop(r, "max_lights")
        col.prop(r, "use_tiny_prim_culling")
        col.prop(r, "volume_raymarching_step_size")
        col.prop(r, "volume_raymarching_step_size_lighting")
        col.prop(r, "volume_max_texture_memory_per_field")


register_classes, unregister_classes = bpy.utils.register_classes_factory((
    ARNOLD_HYDRA_RENDER_PT_quality,
))


def get_panels():
    exclude_panels = {
        'RENDER_PT_stamp',
        'DATA_PT_light',
        'DATA_PT_spot',
        'NODE_DATA_PT_light',
        'DATA_PT_falloff_curve',
        'RENDER_PT_post_processing',
        'RENDER_PT_simplify',
        'SCENE_PT_audio',
        'RENDER_PT_freestyle'
    }
    include_eevee_panels = {
        'MATERIAL_PT_preview',
        'EEVEE_MATERIAL_PT_context_material',
        'EEVEE_MATERIAL_PT_surface',
        'EEVEE_MATERIAL_PT_volume',
        'EEVEE_MATERIAL_PT_settings',
        'EEVEE_WORLD_PT_surface',
    }
    for panel_cls in bpy.types.Panel.__subclasses__():
        if (compat_engines := getattr(panel_cls, 'COMPAT_ENGINES', None)) is None:
            continue
        if (
            (
                'BLENDER_RENDER' in compat_engines
                and panel_cls.__name__ not in exclude_panels
            )
            or (
                'BLENDER_EEVEE' in compat_engines
                and panel_cls.__name__ in include_eevee_panels
            )
        ):
            yield panel_cls


def register():
    register_classes()
    for panel_cls in get_panels():
        panel_cls.COMPAT_ENGINES.add(ArnoldHydraRenderEngine.bl_idname)


def unregister():
    for panel_cls in get_panels():
        if ArnoldHydraRenderEngine.bl_idname in panel_cls.COMPAT_ENGINES:
            panel_cls.COMPAT_ENGINES.remove(ArnoldHydraRenderEngine.bl_idname)
    unregister_classes()
