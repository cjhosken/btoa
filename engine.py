import bpy
from .props.aov import build_aov_settings, register_aov_passes
from .props.render import build_global_settings
from .usd import register_plugin, configure_hydra


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
        register_aov_passes(scene, render_layer)


register, unregister = bpy.utils.register_classes_factory((
   ArnoldHydraRenderEngine,
))
