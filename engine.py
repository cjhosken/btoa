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
        delegate_root = os.path.join(Path(__file__).parent, "btoa", "arnoldusd")
        plugin_dir = os.path.join(delegate_root, "plugin")
        os.environ["ARNOLD_PLUGIN_PATH"] = os.path.join(delegate_root, "procedural") + os.pathsep + os.environ.get("ARNOLD_PLUGIN_PATH", "")
        os.environ["PYTHONPATH"] = os.path.join(delegate_root, "lib", "python") + os.pathsep + os.environ.get("PYTHONPATH", "")
        os.environ["PXR_PLUGINPATH_NAME"] = plugin_dir + os.pathsep + os.path.join(delegate_root, "lib", "usd") + os.pathsep + os.environ.get("PXR_PLUGINPATH_NAME", "")

        platform = sys.platform

        # Check the platform and set the environment variable accordingly
        if platform == "win32":  # Windows
            os.environ["PATH"] = os.path.join(delegate_root, "lib") + os.pathsep + os.environ.get("PATH", "")
        elif platform == "darwin":  # macOS
            os.environ["DYLD_LIBRARY_PATH"] = os.path.join(delegate_root, "lib") + os.pathsep + os.environ.get("DYLD_LIBRARY_PATH", "")
        else:  # Linux or other *nix-like systems
            os.environ["LD_LIBRARY_PATH"] = os.path.join(delegate_root, "lib") + os.pathsep + os.environ.get("LD_LIBRARY_PATH", "")


        print(f"Loading Plugin from: {plugin_dir}...")
        import pxr.Plug
        pxr.Plug.Registry().RegisterPlugins(plugin_dir)

    def get_render_settings(self, engine_type):
        if (engine_type == "VIEWPORT"):
            pass
        else:
            pass
        
        settings = {
            "disableDepthOfField": False,
            "includedPurposes": ["default"],
            "materialBindingPurposes":["full", "allPurpose"],
            "resultion":(1920, 1080),
        }

        return settings

    def update_render_passes(self, scene, render_layer):
        print(f"RENDER LAYER: {render_layer}")
        self.register_pass(
            scene, render_layer,
            name="RGBA",          # Display name
            channels=4,           # RGBA
            type='COLOR',         # Color pass
            aov_settings={
                'arnold:filter': 'box_filter',
                'dataType': 'color4f',
                'driver:parameters:aov:clearValue': 0,
                'driver:parameters:aov:format': 'color4f',
                'driver:parameters:aov:multiSampled': False,
                "driver:parameters:aov:name": "RGBA",
                'sourceName': 'RGBA',
                'sourceType': 'raw',
                'arnold:driver': 'driver_exr'
            }
        )

        print(scene)
    

register, unregister = bpy.utils.register_classes_factory((
    ArnoldRenderEngine,
))