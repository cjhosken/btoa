import bpy
import json
from bpy_extras.io_utils import ImportHelper, ExportHelper

from ..engine import ArnoldHydraRenderEngine


class ARNOLD_UL_custom_render_vars(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.label(text="", icon='RENDER_STILL')
        row.prop(item, "name", text="", emboss=False)


class ARNOLD_OT_custom_render_var_add(bpy.types.Operator):
    bl_idname = "arnold.custom_render_var_add"
    bl_label = "Add Custom Render Var"

    def execute(self, context):
        r = getattr(context.scene.arnold, "global")
        item = r.custom_render_vars.add()
        item.name = f"custom_pass_{len(r.custom_render_vars)}"
        r.custom_active_index = len(r.custom_render_vars) - 1
        context.scene.update_tag()
        return {'FINISHED'}


class ARNOLD_OT_custom_render_var_remove(bpy.types.Operator):
    bl_idname = "arnold.custom_render_var_remove"
    bl_label = "Remove Custom Render Var"

    def execute(self, context):
        r = getattr(context.scene.arnold, "global")
        if len(r.custom_render_vars) > 0:
            r.custom_render_vars.remove(r.custom_active_index)
            r.custom_active_index = min(r.custom_active_index, len(r.custom_render_vars) - 1)
            context.scene.update_tag()
        return {'FINISHED'}


def draw_aov_row(layout, r, name, label):
    row = layout.row(align=True)
    row.prop(r, f"aov_{name}_enabled", text=label)
    sub = row.row(align=True)
    sub.active = getattr(r, f"aov_{name}_enabled")
    sub.prop(r, f"aov_{name}_filter", text="")
    sub.prop(r, f"aov_{name}_format", text="")


class ARNOLD_HYDRA_RENDER_PT_aovs(bpy.types.Panel):
    bl_label = "Arnold AOVs"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'view_layer'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        r = getattr(context.scene.arnold, "global")
        if not r:
            return

        layout.use_property_split = True
        layout.use_property_decorate = False

        # Tab selector
        layout.prop(r, "aov_active_tab", expand=True)
        layout.separator()

        tab = r.aov_active_tab

        if tab == "STANDARD":
            col = layout.column(align=True)
            draw_aov_row(col, r, "RGBA", "RGBA")
            draw_aov_row(col, r, "A", "A")
            col.separator()
            draw_aov_row(col, r, "P", "P")
            draw_aov_row(col, r, "Pref", "Pref")
            col.separator()
            draw_aov_row(col, r, "N", "N")
            draw_aov_row(col, r, "N_Denoise", "N (Denoise)")
            col.separator()
            draw_aov_row(col, r, "Opacity", "Opacity")
            col.separator()
            draw_aov_row(col, r, "Z", "Z")
            draw_aov_row(col, r, "Z_Back", "Z (Back)")

        elif tab == "LIGHTING":
            col = layout.column(align=True)
            draw_aov_row(col, r, "Direct", "Direct")
            col.separator()
            draw_aov_row(col, r, "Indirect", "Indirect")
            col.separator()
            draw_aov_row(col, r, "Emission", "Emission")
            col.separator()
            draw_aov_row(col, r, "Background", "Background")
            col.separator()
            draw_aov_row(col, r, "Albedo", "Albedo")
            draw_aov_row(col, r, "Denoise_Albedo", "Denoise Albedo")
            col.separator()
            draw_aov_row(col, r, "Specular", "Specular")
            draw_aov_row(col, r, "Specular_Direct", "Specular Direct")
            draw_aov_row(col, r, "Specular_Indirect", "Specular Indirect")
            draw_aov_row(col, r, "Specular_Albedo", "Specular Albedo")
            col.separator()
            draw_aov_row(col, r, "SSS", "SSS")
            draw_aov_row(col, r, "SSS_Albedo", "SSS Albedo")
            draw_aov_row(col, r, "SSS_Direct", "SSS Direct")
            draw_aov_row(col, r, "SSS_Indirect", "SSS Indirect")
            col.separator()
            draw_aov_row(col, r, "Transmission", "Transmission")
            draw_aov_row(col, r, "Transmission_Direct", "Transmission Direct")
            draw_aov_row(col, r, "Transmission_Indirect", "Transmission Indirect")
            draw_aov_row(col, r, "Transmission_Albedo", "Transmission Albedo")
            col.separator()
            draw_aov_row(col, r, "Shadow_Matte", "Shadow Matte")
            col.separator()
            draw_aov_row(col, r, "Diffuse", "Diffuse")
            draw_aov_row(col, r, "Diffuse_Direct", "Diffuse Direct")
            draw_aov_row(col, r, "Diffuse_Indirect", "Diffuse Indirect")
            draw_aov_row(col, r, "Diffuse_Albedo", "Diffuse Albedo")
            col.separator()
            draw_aov_row(col, r, "Coat", "Coat")
            draw_aov_row(col, r, "Coat_Direct", "Coat Direct")
            draw_aov_row(col, r, "Coat_Indirect", "Coat Indirect")
            draw_aov_row(col, r, "Coat_Albedo", "Coat Albedo")
            col.separator()
            draw_aov_row(col, r, "Sheen", "Sheen")
            draw_aov_row(col, r, "Sheen_Direct", "Sheen Direct")
            draw_aov_row(col, r, "Sheen_Indirect", "Sheen Indirect")
            draw_aov_row(col, r, "Sheen_Albedo", "Sheen Albedo")

        elif tab == "VOLUME":
            col = layout.column(align=True)
            draw_aov_row(col, r, "Volume", "Volume")
            col.separator()
            draw_aov_row(col, r, "Volume_Z", "Volume Z")
            draw_aov_row(col, r, "Volume_Albedo", "Volume Albedo")
            draw_aov_row(col, r, "Volume_Direct", "Volume Direct")
            draw_aov_row(col, r, "Volume_Indirect", "Volume Indirect")
            draw_aov_row(col, r, "Volume_Opacity", "Volume Opacity")

        elif tab == "UTILITY":
            col = layout.column(align=True)
            draw_aov_row(col, r, "ID", "ID")
            col.separator()
            draw_aov_row(col, r, "Object", "Object")
            col.separator()
            draw_aov_row(col, r, "Shader", "Shader")
            col.separator()
            draw_aov_row(col, r, "Motion_Vector", "Motion Vector")

        elif tab == "DIAGNOSTIC":
            col = layout.column(align=True)
            draw_aov_row(col, r, "CPU_Time", "CPU Time")
            draw_aov_row(col, r, "Ray_Count", "Ray Count")
            draw_aov_row(col, r, "AA_Inv_Density", "AA Inv Density")

        elif tab == "CUSTOM":
            layout.label(text="Custom Render Vars")
            row = layout.row()
            col = row.column()
            col.template_list("ARNOLD_UL_custom_render_vars", "", r, "custom_render_vars", r, "custom_active_index")

            col_ops = row.column(align=True)
            col_ops.operator("arnold.custom_render_var_add", icon='ADD', text="")
            col_ops.operator("arnold.custom_render_var_remove", icon='REMOVE', text="")

            if len(r.custom_render_vars) > 0 and r.custom_active_index < len(r.custom_render_vars):
                item = r.custom_render_vars[r.custom_active_index]
                box = layout.box()
                box.label(text="Render Var Settings")
                col_settings = box.column(align=True)
                col_settings.prop(item, "name")
                col_settings.prop(item, "format")
                col_settings.prop(item, "data_type")
                col_settings.prop(item, "source_name")
                col_settings.prop(item, "source_type")
                col_settings.prop(item, "filter")


class Panel(bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

def draw_device(self, context):
    scene = context.scene
    layout = self.layout
    layout.use_property_split = True
    layout.use_property_decorate = False

    if context.engine == ArnoldHydraRenderEngine.bl_idname:
        r = getattr(scene.arnold, "global")
        layout.prop(r, "render_device", text="Device")
        

class ARNOLD_HYDRA_RENDER_PT_sampling(Panel):
    bl_label = "Sampling"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "AA_samples")
        col.prop(r, "GI_diffuse_samples")
        col.prop(r, "GI_specular_samples")
        col.prop(r, "GI_transmission_samples")
        col.prop(r, "GI_sss_samples")
        col.prop(r, "GI_volume_samples")
        col.separator()
        col.prop(r, "enable_progressive_render")


class ARNOLD_HYDRA_RENDER_PT_sampling_adaptive(bpy.types.Panel):
    bl_label = "Adaptive Sampling"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_sampling"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        layout.prop(r, "enable_adaptive_sampling")

        col = layout.column(align=True)
        col.enabled = r.enable_adaptive_sampling
        col.prop(r, "AA_samples_max")
        col.prop(r, "AA_adaptive_threshold")


class ARNOLD_HYDRA_RENDER_PT_sampling_clamping(bpy.types.Panel):
    bl_label = "Clamping"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_sampling"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        layout.prop(r, "enable_aa_sample_clamp")
        
        col = layout.column(align=True)
        col.enabled = r.enable_aa_sample_clamp
        col.prop(r, "AA_sample_clamp_affects_aovs")
        col.prop(r, "AA_sample_clamp")
        
        layout.separator()
        layout.prop(r, "indirect_sample_clamp")


class ARNOLD_HYDRA_RENDER_PT_sampling_advanced(bpy.types.Panel):
    bl_label = "Advanced"
    bl_parent_id = "ARNOLD_HYDRA_RENDER_PT_sampling"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'render'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {ArnoldHydraRenderEngine.bl_idname}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        layout.prop(r, "dialectric_priorities", text="Nested Dialectrics")
        layout.prop(r, "stochastic_volume_interpolation")
        layout.prop(r, "indirect_specular_blur")



class ARNOLD_HYDRA_RENDER_PT_ray_depth(Panel):
    bl_label = "Ray Depth"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "GI_total_depth")
        col.prop(r, "GI_diffuse_depth")
        col.prop(r, "GI_specular_depth")
        col.prop(r, "GI_transmission_depth")
        col.prop(r, "GI_volume_depth")
        col.prop(r, "auto_transparency_depth")


class ARNOLD_HYDRA_RENDER_PT_environment(Panel):
    bl_label = "Environment"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(context.scene.render, "film_transparent", text="Transparent Background")
        col.separator()
        col.prop(r, "background")
        col.prop(r, "atmosphere")


class ARNOLD_HYDRA_RENDER_PT_lights(Panel):
    bl_label = "Lights"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "enable_light_samples")
        
        sub = col.column()
        sub.enabled = r.enable_light_samples
        sub.prop(r, "light_samples")
        
        col.prop(r, "low_light_threshold")


class ARNOLD_HYDRA_RENDER_PT_textures(Panel):
    bl_label = "Textures"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "texture_auto_generate_tx")

        col = layout.column(align=True)
        col.enabled = r.texture_auto_generate_tx
        col.prop(r, "texture_auto_tx_path")

        col = layout.column(align=True)
        col.enabled = not r.texture_auto_generate_tx
        col.prop(r, "texture_use_existing_tx")

        col = layout.column(align=True)
        col.prop(r, "texture_accept_unmipped")
        col.prop(r, "texture_autotile")

        col.prop(r, "texture_accept_untiled")

        col.prop(r, "textre_max_memory_MB")
        col.prop(r, "texture_max_open_files")


class ARNOLD_HYDRA_RENDER_PT_subdivision(Panel):
    bl_label = "Subdivision"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        r = getattr(context.scene.arnold, "global")

        col = layout.column(align=True)
        col.prop(r, "max_subdivisions")
        col.prop(r, "subdiv_frustum_culling")

        col = layout.column(align=True)
        col.enabled = r.subdiv_frustum_culling
        col.prop(r, "subdiv_frustum_padding")

        col = layout.column(align=True)
        col.prop(r, "subdiv_dicing_camera")


class ARNOLD_UL_imagers(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        row.prop(item, "enabled", text="")
        row.label(text=item.name)


class ARNOLD_OT_imager_add(bpy.types.Operator):
    bl_idname = "arnold.imager_add"
    bl_label = "Add Imager"
    bl_options = {'REGISTER', 'UNDO'}

    imager_type: bpy.props.EnumProperty(
        name="Type",
        items=[
            ("defaultArnoldDenoiser", "Arnold Denoiser", ""),
            ("aiImagerColorCorrect", "Color Correct", ""),
            ("aiImagerColorCurves", "Color Curves", ""),
            ("aiImagerDenoiserNoise", "Denoiser Noise", ""),
            ("aiImagerDenoiserOidn", "Denoiser Oidn", ""),
            ("aiImagerDenoiserOptix", "Denoiser Optix", ""),
            ("aiImagerExposure", "Exposure", ""),
            ("aiImagerLensEffects", "Lens Effects", ""),
            ("aiImagerOverlay", "Overlay", ""),
            ("aiImagerTonemap", "Tonemap", ""),
            ("aiImagerWhiteBalance", "WhiteBalance", ""),
        ],
        default="defaultArnoldDenoiser"
    )

    def execute(self, context):
        r = getattr(context.scene.arnold, "global")
        item = r.imagers.add()
        item.imager_type = self.imager_type

        names_map = {
            "defaultArnoldDenoiser": "Arnold Denoiser",
            "aiImagerColorCorrect": "Color Correct",
            "aiImagerColorCurves": "Color Curves",
            "aiImagerDenoiserNoise": "Denoiser Noise",
            "aiImagerDenoiserOidn": "Denoiser Oidn",
            "aiImagerDenoiserOptix": "Denoiser Optix",
            "aiImagerExposure": "Exposure",
            "aiImagerLensEffects": "Lens Effects",
            "aiImagerOverlay": "Overlay",
            "aiImagerTonemap": "Tonemap",
            "aiImagerWhiteBalance": "WhiteBalance",
        }
        item.name = names_map.get(self.imager_type, self.imager_type)

        r.imager_active_index = len(r.imagers) - 1
        context.scene.update_tag()
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class ARNOLD_OT_imager_remove(bpy.types.Operator):
    bl_idname = "arnold.imager_remove"
    bl_label = "Remove Imager"

    def execute(self, context):
        r = getattr(context.scene.arnold, "global")
        if len(r.imagers) > 0:
            r.imagers.remove(r.imager_active_index)
            r.imager_active_index = min(r.imager_active_index, len(r.imagers) - 1)
            context.scene.update_tag()
        return {'FINISHED'}


class ARNOLD_OT_imager_move(bpy.types.Operator):
    bl_idname = "arnold.imager_move"
    bl_label = "Move Imager"

    direction: bpy.props.EnumProperty(
        items=[
            ('UP', 'Up', ''),
            ('DOWN', 'Down', '')
        ]
    )

    def execute(self, context):
        r = getattr(context.scene.arnold, "global")
        index = r.imager_active_index
        if self.direction == 'UP' and index > 0:
            r.imagers.move(index, index - 1)
            r.imager_active_index -= 1
        elif self.direction == 'DOWN' and index < len(r.imagers) - 1:
            r.imagers.move(index, index + 1)
            r.imager_active_index += 1
        context.scene.update_tag()
        return {'FINISHED'}


class ARNOLD_OT_imager_import(bpy.types.Operator, ImportHelper):
    bl_idname = "arnold.imager_import"
    bl_label = "Import Imagers"
    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'}, maxlen=255)

    def execute(self, context):
        r = getattr(context.scene.arnold, "global")
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
            
            for item_data in data:
                item = r.imagers.add()
                item.name = item_data.get("name", "Imager")
                item.enabled = item_data.get("enabled", True)
                item.imager_type = item_data.get("imager_type", "defaultArnoldDenoiser")
            
            context.scene.update_tag()
            self.report({'INFO'}, f"Imported {len(data)} imagers")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to import: {str(e)}")
            return {'CANCELLED'}
        return {'FINISHED'}


class ARNOLD_OT_imager_export(bpy.types.Operator, ExportHelper):
    bl_idname = "arnold.imager_export"
    bl_label = "Export Imagers"
    filename_ext = ".json"
    filter_glob: bpy.props.StringProperty(default="*.json", options={'HIDDEN'}, maxlen=255)

    def execute(self, context):
        r = getattr(context.scene.arnold, "global")
        data = []
        for imager in r.imagers:
            data.append({
                "name": imager.name,
                "enabled": imager.enabled,
                "imager_type": imager.imager_type
            })
        
        try:
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=4)
            self.report({'INFO'}, f"Exported {len(data)} imagers")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export: {str(e)}")
            return {'CANCELLED'}
        return {'FINISHED'}


class ARNOLD_HYDRA_RENDER_PT_imagers(Panel):
    bl_label = "Imagers"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        r = getattr(context.scene.arnold, "global")
        if not r:
            return

        layout.use_property_split = True
        layout.use_property_decorate = False

        row = layout.row()
        row.template_list("ARNOLD_UL_imagers", "", r, "imagers", r, "imager_active_index")

        col = row.column(align=True)
        col.operator("arnold.imager_add", icon='ADD', text="")
        col.operator("arnold.imager_remove", icon='REMOVE', text="")
        col.separator()
        col.operator("arnold.imager_move", icon='TRIA_UP', text="").direction = 'UP'
        col.operator("arnold.imager_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

        layout.separator()
        row = layout.row(align=True)
        row.operator("arnold.imager_import", icon='IMPORT', text="Import")
        row.operator("arnold.imager_export", icon='EXPORT', text="Export")


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
    ARNOLD_UL_custom_render_vars,
    ARNOLD_OT_custom_render_var_add,
    ARNOLD_OT_custom_render_var_remove,
    ARNOLD_HYDRA_RENDER_PT_aovs,
    ARNOLD_HYDRA_RENDER_PT_sampling,
    ARNOLD_HYDRA_RENDER_PT_sampling_adaptive,
    ARNOLD_HYDRA_RENDER_PT_sampling_clamping,
    ARNOLD_HYDRA_RENDER_PT_sampling_advanced,
    ARNOLD_HYDRA_RENDER_PT_ray_depth,
    ARNOLD_HYDRA_RENDER_PT_environment,
    ARNOLD_HYDRA_RENDER_PT_lights,
    ARNOLD_HYDRA_RENDER_PT_textures,
    ARNOLD_HYDRA_RENDER_PT_subdivision,
    ARNOLD_UL_imagers,
    ARNOLD_OT_imager_add,
    ARNOLD_OT_imager_remove,
    ARNOLD_OT_imager_move,
    ARNOLD_OT_imager_import,
    ARNOLD_OT_imager_export,
    ARNOLD_HYDRA_RENDER_PT_imagers,
    ARNOLD_VIEW3D_PT_shading_render_pass,
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
    bpy.types.RENDER_PT_context.append(draw_device)

    for panel_cls in get_panels():
        panel_cls.COMPAT_ENGINES.add(ArnoldHydraRenderEngine.bl_idname)

    register_classes()


def unregister():

    bpy.types.RENDER_PT_context.remove(draw_device)

    for panel_cls in get_panels():
        if ArnoldHydraRenderEngine.bl_idname in panel_cls.COMPAT_ENGINES:
            panel_cls.COMPAT_ENGINES.remove(ArnoldHydraRenderEngine.bl_idname)

    unregister_classes()
