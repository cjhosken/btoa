import bpy
from .props.aov import build_aov_settings, BUILTIN_AOVS, get_usd_aov_types
from .props.render import build_global_settings
from .usd import register_plugin, configure_hydra

_viewports_to_restore = []


@bpy.app.handlers.persistent
def on_render_init(scene, *args):
    global _viewports_to_restore
    _viewports_to_restore.clear()

    # Defer switching viewport shading to SOLID to avoid interrupting active view_update or view_draw cycles
    def pause_viewports():
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D' and space.shading.type == 'RENDERED':
                            try:
                                space.shading.type = 'SOLID'
                                _viewports_to_restore.append(space)
                            except Exception:
                                pass
                    area.tag_redraw()
        return None

    bpy.app.timers.register(pause_viewports, first_interval=0.01)


@bpy.app.handlers.persistent
def on_render_end(scene, *args):
    global _viewports_to_restore

    def restore():
        for space in _viewports_to_restore:
            try:
                space.shading.type = 'RENDERED'
            except Exception:
                pass
        _viewports_to_restore.clear()

        # Force redrawing of View3D areas
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == 'VIEW_3D':
                    area.tag_redraw()
        return None

    # Defer restoration slightly to allow the final render session to fully release resources first
    bpy.app.timers.register(restore, first_interval=0.1)


def setup_hydra_export():
    bpy.app.timers.register(configure_hydra, first_interval=0.1)


class ArnoldHydraRenderEngine(bpy.types.HydraRenderEngine):
    bl_idname = "ARNOLD"
    bl_label = "HdArnold"
    bl_info = "Autodesk's Arnold Production Renderer integration"

    bl_use_preview = True
    bl_use_gpu_context = False
    bl_use_materialx = False

    bl_delegate_id = "HdArnoldRendererPlugin"

    @classmethod
    def register(cls):
        register_plugin()
        setup_hydra_export()

        # Register render handlers to manage concurrent viewport rendering
        if on_render_init not in bpy.app.handlers.render_init:
            bpy.app.handlers.render_init.append(on_render_init)
        if on_render_end not in bpy.app.handlers.render_complete:
            bpy.app.handlers.render_complete.append(on_render_end)
        if on_render_end not in bpy.app.handlers.render_cancel:
            bpy.app.handlers.render_cancel.append(on_render_end)

    @classmethod
    def unregister(cls):
        # Remove render handlers
        if on_render_init in bpy.app.handlers.render_init:
            bpy.app.handlers.render_init.remove(on_render_init)
        if on_render_end in bpy.app.handlers.render_complete:
            bpy.app.handlers.render_complete.remove(on_render_end)
        if on_render_end in bpy.app.handlers.render_cancel:
            bpy.app.handlers.render_cancel.remove(on_render_end)

    def get_settings(self, engine_type):
        arnold = bpy.context.scene.arnold
        settings = arnold.viewport if engine_type == "VIEWPORT" else getattr(arnold, "global")
        return settings

    def get_render_settings(self, engine_type):
        settings = self.get_settings(engine_type)

        result = build_global_settings(
            settings,
            engine_type == "VIEWPORT"
        )

        result.update(
            build_aov_settings(
                settings,
                engine_type
            )
        )

        return result

    def update_render_passes(self, scene, render_layer):
        # scene.arnold.global contains the settings
        settings = getattr(scene.arnold, "global", None)
        if not settings:
            return

        def get_register_params(name, data_type):
            """
            Maps Hydra buffer typings to Blender's API specifications.
            """


            if "color" in data_type:
                # Check if Hydra specified an alpha channel (color4f)
                if "4" in data_type:
                    return 4, "RGBA", "COLOR"
                return 3, "RGB", "COLOR"
                
            if "float" in data_type or "int" in data_type or "half" in data_type:
                if "Z" in name:
                    return 1, "Z", "VALUE"
                
                if "3" in data_type: 
                    return 3, "XYZ", "VECTOR"
                
                # return 1, "X", "VALUE"

            # General production safe-fallback
            return 3, "RGB", "COLOR"

        # Register built-in AOVs if enabled
        for cat, aovs in BUILTIN_AOVS.items():
            for name, label, def_filt, def_fmt in aovs:
                if name == "RGBA" or getattr(settings, f"aov_{name}_enabled", False):
                    bl_name = 'Combined' if name == 'RGBA' else ('Depth' if name == 'Z' else label)
                    dataType, fmt = get_usd_aov_types(name, getattr(settings, f"aov_{name}_format"))
                    channels, channel_name, pass_type = get_register_params(name, dataType)
                    self.register_pass(scene, render_layer, bl_name, channels, channel_name, pass_type)


register_cls, unregister_cls = bpy.utils.register_classes_factory((
    ArnoldHydraRenderEngine,
))

def register():
    register_cls()
    ArnoldHydraRenderEngine.register()

def unregister():
    ArnoldHydraRenderEngine.unregister()
    unregister_cls()
