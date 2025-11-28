from pathlib import Path
import bpy, os, sys, ctypes

class ArnoldRenderEngine(bpy.types.HydraRenderEngine):
    bl_idname = "ARNOLD"
    bl_label = "HdArnold"
    bl_info = "Autodesk's Arnold Production Renderer integration"

    bl_use_preview = True
    bl_use_gpu_context = False
    bl_use_materialx = True

    bl_delegate_id = "HdArnoldRendererPlugin"

    @classmethod
    def register(cls):        
        import pxr.Plug
        plugin_path = os.path.join(os.environ.get("BTOA_ROOT", ""), "plugin")
        print(plugin_path)
        pxr.Plug.Registry().RegisterPlugins(plugin_path)

    def update(self, data, depsgraph):
        super().update(data, depsgraph)

    def get_render_settings(self, engine_type):
        settings = {
            "aovToken:RGBA":"color",
            "aovToken:depth":"depth"
        }
        
        return settings

    def update_render_passes(self, scene, render_layer):
        self.register_pass(scene, render_layer, 'RGBA', 4, 'RGBA', 'COLOR')
        self.register_pass(scene, render_layer, 'depth', 1, 'Z', 'VALUE')
    
register, unregister = bpy.utils.register_classes_factory((
    ArnoldRenderEngine,
))