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
        import pxr.Plug
        btoa = os.path.join(os.path.expanduser("~"), ".btoa")
        arnoldsdk = os.path.join(btoa, "arnoldsdk", "Arnold-7.3.4.1-linux")
        arnoldusd = os.path.join(btoa, "arnold-usd")
        
        os.environ["ARNOLD_PLUGIN_PATH"] = os.path.join(arnoldusd, "procedural")

        os.environ["PYTHONPATH"] = os.environ.get("PYTHONPATH", "") + ":" + os.path.join(arnoldsdk, "python")
        os.environ["PXR_PLUGINPATH_NAME"] = os.environ.get("PXR_PLUGINPATH_NAME", "") + ":" + os.path.join(arnoldusd, "plugin") + ":" + os.path.join(arnoldsdk, "plugins", "usd")
        os.environ["LD_LIBRARY_PATH"] = os.environ.get("LD_LIBRARY_PATH", "") + ":" + os.path.join(arnoldsdk, "bin")

        print(os.environ.get("PXR_PLUGINPATH_NAME"))
        print(os.environ.get("LD_LIBRARY_PATH"))

        pxr.Plug.Registry().RegisterPlugins([os.path.join(arnoldusd, "plugin")])


    def get_render_settings(self, engine_type):
        return {
            'myBoolean': True,
            'myValue': 8,
            'aovToken:Depth': "depth",
        }
    
    def update_render_passes(self, scene, render_layer):
        if render_layer.use_pass_z:
            self.register_pass(scene, render_layer, 'Depth', 1, 'Z', 'VALUE')

    def update(self, data, depsgraph):
        super().update(data, depsgraph)


def register():
    bpy.utils.register_class(ArnoldRenderEngine)

def unregister():
    bpy.utils.unregister_class(ArnoldRenderEngine)