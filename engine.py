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
        plugin_path = arnold.hdArnoldPluginPath

        print(f"Loading Plugin from: {plugin_path}...")
        pxr.Plug.Registry().RegisterPlugins(plugin_path)

    def get_render_settings(self, engine_type):
        # Explicitly define AOV bindings for Arnold
        return {
            'aovToken:color': "color",
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