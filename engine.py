import bpy, os

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
        import pxr.Plug
        arnold = bpy.context.scene.arnold
        usd_path = arnold.arnoldUSDPath
        plugin_path = os.path.join(usd_path, "plugin")
        usd_path = os.path.join(arnold.arnoldUSDPath, "plugin")
        sdk_path = os.path.join(os.path.expanduser("~"), ".btoa", "arnoldSDK")

        os.environ["ARNOLD_PLUGIN_PATH"] = os.path.join(usd_path, "procedural")
        os.environ["PXR_PLUGINPATH_NAME"] = os.path.join(plugin_path) + ":" + os.environ.get("PXR_PLUGINPATH_NAME")
        os.environ["LD_LIBRARY_PATH"] = os.path.join(sdk_path, "bin") + ":" + os.environ.get("LD_LIBRARY_PATH")

        print(f"Loading Plugin from: {plugin_path}...")
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