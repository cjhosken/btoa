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
        bpy.app.timers.register(cls.load_plugin, first_interval=0.01)

    def load_plugin():
        arnold = bpy.context.scene.arnold
        usd_path = arnold.arnoldUSDPath
        plugin_path = os.path.join(usd_path, "plugin")

        os.environ["ARNOLD_PLUGIN_PATH"] = os.path.join(usd_path, "procedural")
        os.environ["PYTHONPATH"] = os.path.join(usd_path, "lib", "python")
        os.environ["PXR_PLUGINPATH_NAME"] = os.path.join(plugin_path) + ":" + os.path.join(usd_path, "lib", "usd") + ":" + os.environ.get("PXR_PLUGINPATH_NAME")
        os.environ["LD_LIBRARY_PATH"] = os.path.join(usd_path, "lib") + ":" + os.environ.get("LD_LIBRARY_PATH")

        print(f"Loading Plugin from: {plugin_path}...")
        import pxr.Plug
        pxr.Plug.Registry().RegisterPlugins(plugin_path)

    def get_render_settings(self, engine_type):
        # Explicitly define AOV bindings for Arnold
        return {
            'arnold:aov:beauty': True
        }
    
    def update_render_passes(self, scene, render_layer):
        # Register standard AOVs for rendering
        self.register_pass(scene, render_layer, 'Combined', 4, 'RGBA', 'COLOR')
        
    def update(self, data, depsgraph):
        super().update(data, depsgraph)

def register():
    bpy.utils.register_class(ArnoldRenderEngine)

def unregister():
    bpy.utils.unregister_class(ArnoldRenderEngine)