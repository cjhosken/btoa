import bpy, os

class ArnoldHydraRenderEngine(bpy.types.HydraRenderEngine):
    bl_idname = "ARNOLD"
    bl_label = "HdArnold"
    bl_info = "Autodesk's Arnold Production Renderer integration"

    bl_use_preview = False
    bl_use_gpu_context = False
    bl_use_materialx = False

    bl_delegate_id = "HdArnoldRendererPlugin"

    @classmethod
    def register(cls):        
        import pxr.Plug
        plugin_path = os.path.join(os.environ.get("BTOA_ROOT", ""), "plugin")
        pxr.Plug.Registry().RegisterPlugins(plugin_path)

    def get_render_settings(self, engine_type):
        settings = {
                "aovToken:Combined": "RGBA",
            }
        return settings

    def update_render_passes(self, scene, render_layer):
        self.register_pass(scene, render_layer, 'Combined', 4, 'RGBA', 'COLOR')

register, unregister = bpy.utils.register_classes_factory((
   ArnoldHydraRenderEngine,
))