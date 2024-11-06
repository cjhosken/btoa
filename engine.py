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
        arnoldsdk = os.path.join(btoa, "dependencies", "arnoldSDK")
        arnoldusd = os.path.join(btoa, "installs", "arnoldusd")
        
        os.environ["ARNOLD_PLUGIN_PATH"] = os.path.join(arnoldusd, "procedural")
        os.environ["PXR_PLUGINPATH_NAME"] = os.environ.get("PXR_PLUGINPATH_NAME", "") + ":" + os.path.join(arnoldusd, "plugin") + ":" + os.path.join(arnoldsdk, "plugins", "usd")

        pxr.Plug.Registry().RegisterPlugins([os.path.join(arnoldusd, "plugin")])


    def get_render_settings(self, engine_type):
        # Explicitly define AOV bindings for Arnold
        return {
            'aovToken:color': "color",
            'aovToken:depth': "depth",
            'aovToken:diffuse': "diffuse",
            'aovToken:specular': "specular",
            'aovToken:emission': "emission",
        }
    
    def update_render_passes(self, scene, render_layer):
        # Register standard AOVs for rendering
        self.register_pass(scene, render_layer, 'Combined', 4, 'RGBA', 'COLOR')
        
        # Register additional passes if needed
        if render_layer.use_pass_z:
            self.register_pass(scene, render_layer, 'Depth', 1, 'Z', 'VALUE')
        if render_layer.use_pass_diffuse_color:
            self.register_pass(scene, render_layer, 'Diffuse', 3, 'RGB', 'COLOR')
        if render_layer.use_pass_glossy_direct:
            self.register_pass(scene, render_layer, 'Specular', 3, 'RGB', 'COLOR')
        # Add more passes as needed

    def update(self, data, depsgraph):
        super().update(data, depsgraph)


def register():
    bpy.utils.register_class(ArnoldRenderEngine)

def unregister():
    bpy.utils.unregister_class(ArnoldRenderEngine)