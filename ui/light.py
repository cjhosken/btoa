import bpy

from ..engine import ArnoldRenderEngine

class ARNOLD_PT_light(bpy.types.Panel):
    bl_label = "Arnold Light"
    bl_idname = "ARNOLD_PT_light"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    COMPAT_ENGINES = {ArnoldRenderEngine.bl_idname}
    
    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

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
    ARNOLD_PT_light
))
