import bpy

from .engine import ArnoldHydraRenderEngine

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

    def draw(self, layout):
        pass

class ARNOLD_HYDRA_LIGHT_PT_light(Panel):
    """Physical light sources"""
    bl_label = "Light"
    bl_context = 'data'

    @classmethod
    def poll(cls, context):
        return super().poll(context) and context.light

    def draw(self, context):
        layout = self.layout

        light = context.light

        layout.prop(light, "type", expand=True)

        layout.use_property_split = True
        layout.use_property_decorate = False

        main_col = layout.column()
        heading = main_col.column(align=True, heading="Temperature")
        row = heading.column(align=True).row(align=True)
        row.prop(light, "use_temperature", text="")
        sub = row.row()
        sub.active = light.use_temperature
        sub.prop(light, "temperature", text="")

        if light.use_temperature:
            main_col.prop(light, "color", text="Tint")
        else:
            main_col.prop(light, "color", text="Color")

        main_col = layout.column()
        main_col.prop(light, "energy")
        main_col.prop(light, "exposure")
        main_col.prop(light, "normalize")
        main_col.separator()

        if light.type == 'POINT':
            row = main_col.row(align=True)
            row.prop(light, "shadow_soft_size", text="Radius")

        elif light.type == 'SPOT':
            col = main_col.column(align=True)
            col.prop(light, 'spot_size', text="Angle", slider=True)
            col.prop(light, 'spot_blend', slider=True)

            main_col.prop(light, 'show_cone')

        elif light.type == 'SUN':
            main_col.prop(light, "angle")

        elif light.type == 'AREA':
            main_col.prop(light, "shape", text="Shape")
            sub = main_col.column(align=True)

            if light.shape in {'SQUARE', 'DISK'}:
                sub.prop(light, "size")
            elif light.shape in {'RECTANGLE', 'ELLIPSE'}:
                sub.prop(light, "size", text="Size X")
                sub.prop(light, "size_y", text="Y")

            else:
                main_col.prop(light, 'size')

register_classes, unregister_classes = bpy.utils.register_classes_factory((
    ARNOLD_HYDRA_RENDER_PT_quality,
    ARNOLD_HYDRA_LIGHT_PT_light,
    
))

def get_panels():
    # Follow the Cycles model of excluding panels we don't want.
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
                'BLENDER_RENDER' in compat_engines and
                panel_cls.__name__ not in exclude_panels
            ) or (
                'BLENDER_EEVEE' in compat_engines and
                panel_cls.__name__ in include_eevee_panels
            )
        ):
            yield panel_cls

def register():
    register_classes()

    for panel_cls in get_panels():
        panel_cls.COMPAT_ENGINES.add(ArnoldHydraRenderEngine.bl_idname)


def unregister():
    unregister_classes()

    for panel_cls in get_panels():
        if ArnoldHydraRenderEngine.bl_idname in panel_cls.COMPAT_ENGINES:
            panel_cls.COMPAT_ENGINES.remove(ArnoldHydraRenderEngine.bl_idname)