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
        bpy.utils.expose_bundled_modules()

        import pxr.Plug
        plugin_path = os.path.abspath(os.path.join(os.environ.get("BTOA_ROOT", ""), "plugin"))
        print(f"[BtoA] Registering USD plugin path: {plugin_path}")
        if os.path.exists(plugin_path):
            pxr.Plug.Registry().RegisterPlugins([plugin_path])
        else:
            print(f"[BtoA] Warning: USD plugin path does not exist. Please build the delegate.")

    def get_render_settings(self, engine_type):
        arnold = bpy.context.scene.arnold
        samples = arnold.samples
        result = {"arnold:samples": samples}
        
        if engine_type != "VIEWPORT":
            result |= {
                "aovToken:Combined": "color",
                "aovToken:Depth": "depth"
            }

        return result

    def update_render_passes(self, scene, render_layer):
        self.register_pass(scene, render_layer, 'Combined', 4, 'RGBA', 'COLOR')
        self.register_pass(scene, render_layer, 'Depth', 1, 'Z', 'VALUE')

register, unregister = bpy.utils.register_classes_factory((
   ArnoldHydraRenderEngine,
))
