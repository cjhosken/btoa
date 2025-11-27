from pathlib import Path
import bpy, os, sys, ctypes

class ArnoldRenderEngine(bpy.types.HydraRenderEngine):
    bl_idname = "ARNOLD"
    bl_label = "Arnold"
    bl_info = "Autodesk's Arnold Production Renderer integration"

    bl_use_preview = True
    bl_use_gpu_context = True
    bl_use_materialx = True

    bl_delegate_id = "HdArnoldRendererPlugin"

    @classmethod
    def register(cls):
        bpy.utils.expose_bundled_python_modules()

        delegate_root = os.path.join(Path.home(), ".arnold", "install", "arnoldusd")
        plugin_dir = os.path.join(delegate_root, "plugin")

        import pxr.Plug
        pxr.Plug.Registry().RegisterPlugins(plugin_dir)

    def update(self, data, depsgraph):
        super().update(data, depsgraph)

    def get_render_settings(self, engine_type):
        if (engine_type == "VIEWPORT"):
            pass
        else:
            pass
        
        settings = {
            "disableDepthOfField": False,
            "includedPurposes": ["default"],
            "materialBindingPurposes":["full", "allPurpose"],
            "resolution":(1920, 1080),
            "aovToken:RGBA":"color",
        }

        return settings

    def update_render_passes(self, scene, render_layer):
        self.register_pass(scene, render_layer, "RGBA", 4, "RGBA", "COLOR")
    

register, unregister = bpy.utils.register_classes_factory((
    ArnoldRenderEngine,
))