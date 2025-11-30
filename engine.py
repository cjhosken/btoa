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
        print(plugin_path)
        pxr.Plug.Registry().RegisterPlugins(plugin_path)

    def get_render_settings(self, engine_type):
        settings = {}

        if engine_type != 'VIEWPORT':
            settings |= {
                # Beauty
                "aovToken:Combined": "color",
                "aovDescriptor:Combined": {
                    "sourceName": "RGBA",
                    
                    "driver:parameters:aov:clearValue": 0,
                    "driver:parameters:aov:format": "color4f",
                    "driver:parameters:aov:name": "RGBA",
                    "driver:parameters:aov:multiSampled": False,
                    
                    "arnold:filter": "box_filter",
                    "arnold:global:AA_seed": 1129,
                    
                    
                    "sourceType": "raw",
                    "dataType": "color4f",
                }
            }

        return settings

    def update_render_passes(self, scene, render_layer):
        self.register_pass(scene, render_layer, 'Combined', 4, 'RGBA', 'COLOR')

register, unregister = bpy.utils.register_classes_factory((
   ArnoldHydraRenderEngine,
))