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

    def __init__(self):
        super().__init__()
        self._avos = [ "RGBA" ]

    @classmethod
    def register(cls):
        delegate_root = os.path.join(Path(__file__).parent, "btoa")
        delegate_dir = os.path.join(delegate_root, "arnoldusd")
        os.environ["PATH"] = delegate_dir + os.pathsep + os.environ.get("PATH", "")

        print(f"Loading Plugin from: {delegate_dir}...")
        import pxr.Plug
        pxr.Plug.Registry().RegisterPlugins(str(os.path.join(delegate_dir, "plugin")))

    def get_render_settings(self, engine_type):
        # Return Arnold-specific render settings including required AOVs
        settings = {
            'arnold:aov:RGBA': True,  # Main beauty pass
            'arnold:aov:enable_progressive_render': True,
            'arnold:aov:background': [0, 0, 0, 1],
        }
        return settings
    
    def update_render_passes(self, scene=None, render_layer=None):
        # Register all AOV passes
        self.register_pass(scene, render_layer, "Combined", 4, "RGBA", 'COLOR')
        
    def render(self, depsgraph):
        # Ensure AOVs are properly set before rendering
        self.update_render_passes(depsgraph.scene, depsgraph.view_layer)
        super().render(depsgraph)

    def view_update(self, context, depsgraph):
        self.update_render_passes(depsgraph.scene, depsgraph.view_layer)
        super().view_update(context, depsgraph)

    def view_draw(self, context, depsgraph):
        self.update_render_passes(depsgraph.scene, depsgraph.view_layer)
        super().view_draw(context, depsgraph)

def register():
    bpy.utils.register_class(ArnoldRenderEngine)

def unregister():
    bpy.utils.unregister_class(ArnoldRenderEngine)