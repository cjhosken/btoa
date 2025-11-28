from pathlib import Path
import bpy, os, sys, ctypes

class ArnoldRenderEngine(bpy.types.HydraRenderEngine):
    bl_idname = "ARNOLD"
    bl_label = "HdArnold"
    bl_info = "Autodesk's Arnold Production Renderer integration"

    bl_use_preview = True
    bl_use_gpu_context = True
    bl_use_materialx = True

    bl_delegate_id = "HdArnoldRendererPlugin"

    @classmethod
    def register(cls):        
        import pxr.Plug
        plugin_path = os.path.join(os.environ.get("BTOA_ROOT", ""), "plugin")
        print(plugin_path)
        pxr.Plug.Registry().RegisterPlugins(plugin_path)

    def update(self, data, depsgraph):
        super().update(data, depsgraph)

    def get_render_settings(self, engine_type):
        settings = {
            "disableDepthOfField": False,
            "includedPurposes": ["default"],
            "materialBindingPurposes":["full", "allPurpose"],
            "resolution":(1920, 1080),
            "productType":"raster",
            "productName":"",
            "instantaneousShutter":0,
            "driver:parameters:artist":"",
            "driver:parameters:comment":"",
            "driver:parameters:hostname":"",
            "driver:parameters:OpenEXR:compression":"zips",
            "pixelAspectRatio":1,
            "aspectRatioConfirmPolicy":"expandAperture",
            "dataWindowNDC":(0, 0, 1, 1),
            "orderedVars": [
                "</Render/Products/Vars/Beauty>"
            ],
            "aovBindings": [
                {
                    "sourceName": "RGBA",
                    "sourceType":"raw",
                    "dataType":"color4f",
                    "driver:parameters:aov:name": "Beauty",
                    "driver:parameters:aov:multiSampled": False,
                    "driver:parameters:aov:format":"float4",
                    "driver:parameters:aov:clearValue": 0,
                    "driver:parameters:aov:channel_prefix":"",
                    "arnold:width":2,
                    "arnold:filter":"gaussian_filter"
                }
            ]
        }

        return settings

    def update_render_passes(self, scene, render_layer):
        self.register_pass(scene, render_layer, "RGBA", 4, "RGBA", "COLOR")
    

register, unregister = bpy.utils.register_classes_factory((
    ArnoldRenderEngine,
))