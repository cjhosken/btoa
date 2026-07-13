import bpy, os


def _set_usd_export_method():
    scene = bpy.context.scene
    if scene is not None:
        scene.hydra.export_method = 'USD'
    return None  # Don't repeat


class ArnoldHydraRenderEngine(bpy.types.HydraRenderEngine):
    bl_idname = "ARNOLD"
    bl_label = "HdArnold"
    bl_info = "Autodesk's Arnold Production Renderer integration"

    bl_use_preview = True
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

        bpy.app.timers.register(_set_usd_export_method, first_interval=0.1)

    def get_render_settings(self, engine_type):
        arnold = bpy.context.scene.arnold
        settings = arnold.viewport if engine_type == "VIEWPORT" else getattr(arnold, "global")
        final = getattr(arnold, "global")

        result = {}

        # Viewport always needs the beauty pass; final renders respect the checkbox
        if engine_type == "VIEWPORT" or (final and final.aov_combined):
            result["aovToken:Combined"] = "color"

        if settings is not None:
            result |= {
                "arnold:global:enable_progressive_render": settings.enable_progressive_render,
                "arnold:global:enable_adaptive_sampling": settings.enable_adaptive_sampling,
                "arnold:global:threads": -1 if settings.autodetect_threads else settings.threads,
                "arnold:global:dialectric_priorities": settings.dialectric_priorities,
                "arnold:global:enable_aa_sample_clamp": settings.enable_aa_sample_clamp,
                "arnold:global:AA_sample_clamp": settings.AA_sample_clamp,
                "arnold:global:AA_sample_clamp_affects_aovs": settings.AA_sample_clamp_affects_aovs,
                "arnold:global:indirect_sample_clamp": settings.indirect_sample_clamp,
                "arnold:global:light_samples": settings.light_samples if settings.enable_light_samples else 0,
                "arnold:global:AA_samples": settings.AA_samples,
                "arnold:global:AA_samples_max": settings.AA_samples_max,
                "arnold:global:GI_diffuse_samples": settings.GI_diffuse_samples,
                "arnold:global:GI_specular_samples": settings.GI_specular_samples,
                "arnold:global:GI_transmission_samples": settings.GI_transmission_samples,
                "arnold:global:GI_sss_samples": settings.GI_sss_samples,
                "arnold:global:GI_volume_samples": settings.GI_volume_samples,
                "arnold:global:auto_transparency_depth": settings.auto_transparency_depth,
                "arnold:global:GI_diffuse_depth": settings.GI_diffuse_depth,
                "arnold:global:GI_specular_depth": settings.GI_specular_depth,
                "arnold:global:GI_transmission_depth": settings.GI_transmission_depth,
                "arnold:global:GI_volume_depth": settings.GI_volume_depth,
                "arnold:global:GI_total_depth": settings.GI_total_depth,
                "arnold:global:abort_on_error": settings.abort_on_error,
                "arnold:global:ignore_textures": settings.ignore_textures,
                "arnold:global:ignore_shaders": settings.ignore_shaders,
                "arnold:global:ignore_atmosphere": settings.ignore_atmosphere,
                "arnold:global:ignore_lights": settings.ignore_lights,
                "arnold:global:ignore_shadows": settings.ignore_shadows,
                "arnold:global:ignore_subdivision": settings.ignore_subdivision,
                "arnold:global:ignore_displacement": settings.ignore_displacement,
                "arnold:global:ignore_bump": settings.ignore_bump,
                "arnold:global:ignore_motion_blur": settings.ignore_motion_blur,
                "arnold:global:ignore_dof": settings.ignore_dof,
                "arnold:global:ignore_smoothing": settings.ignore_smoothing,
                "arnold:global:ignore_sss": settings.ignore_sss,
                "arnold:global:plugin_searchpath": settings.plugin_searchpath,
                "arnold:global:asset_searchpath": settings.asset_searchpath,
                "arnold:global:osl_includepath": settings.osl_includepath,
                "arnold:global:subdiv_dicing_camera": settings.subdiv_dicing_camera.name if settings.subdiv_dicing_camera else "",
                "arnold:global:subdiv_frustum_culling": settings.subdiv_frustum_culling,
                "arnold:global:enable_gpu_rendering": (settings.render_device == "GPU"),
                "arnold:global:render_device": settings.render_device,
                "arnold:global:render_device_fallback": settings.render_device_fallback,
                "arnold:global:log_verbosity": {"error": 0, "warning": 1, "info": 2, "debug": 3}.get(settings.log_verbosity, 2),
                "arnold:global:log_file": settings.log_file,
                "arnold:global:profile_file": settings.profile_file,
                "arnold:global:report_file": settings.report_file,
                "arnold:global:stats_file": settings.stats_file,
            }

        # AOV descriptors tell HdArnold which Arnold internal AOV name to bind
        # to each Blender render pass. Without these, Arnold renders the AOV
        # internally but never writes data to Blender's render buffer.
        # Only meaningful for final renders, not viewport.
        if engine_type != "VIEWPORT" and final is not None:
            if final.aov_combined:
                result["aovDescriptor:Combined"] = {
                    "sourceName": "RGBA",
                    "sourceType": "raw",
                    "dataType": "color4f",
                    "driver:parameters:aov:name": "RGBA",
                    "driver:parameters:aov:format": "color4f",
                    "driver:parameters:aov:clearValue": 0,
                    "driver:parameters:aov:multiSampled": False,
                    "arnold:filter": "box_filter",
                }
            if final.aov_depth:
                result["aovToken:Depth"] = "depth"
                result["aovDescriptor:Depth"] = {
                    "sourceName": "Z",
                    "sourceType": "raw",
                    "dataType": "float",
                    "driver:parameters:aov:name": "Z",
                    "driver:parameters:aov:format": "float",
                    "driver:parameters:aov:clearValue": 1e30,
                    "driver:parameters:aov:multiSampled": False,
                    "arnold:filter": "closest_filter",
                }
            if final.aov_position:
                result["aovToken:P"] = "P"
                result["aovDescriptor:P"] = {
                    "sourceName": "P",
                    "sourceType": "raw",
                    "dataType": "color3f",
                    "driver:parameters:aov:name": "P",
                    "driver:parameters:aov:format": "color3f",
                    "driver:parameters:aov:clearValue": 0,
                    "driver:parameters:aov:multiSampled": False,
                    "arnold:filter": "closest_filter",
                }
            if final.aov_normal:
                result["aovToken:N"] = "N"
                result["aovDescriptor:N"] = {
                    "sourceName": "N",
                    "sourceType": "raw",
                    "dataType": "color3f",
                    "driver:parameters:aov:name": "N",
                    "driver:parameters:aov:format": "color3f",
                    "driver:parameters:aov:clearValue": 0,
                    "driver:parameters:aov:multiSampled": False,
                    "arnold:filter": "closest_filter",
                }
            for aov in final.aov_shaders:
                if aov.name:
                    result[f"aovToken:{aov.name}"] = "color"
                    result[f"aovDescriptor:{aov.name}"] = {
                        "sourceName": aov.name,
                        "sourceType": "raw",
                        "dataType": "color4f",
                        "driver:parameters:aov:name": aov.name,
                        "driver:parameters:aov:format": "color4f",
                        "driver:parameters:aov:clearValue": 0,
                        "driver:parameters:aov:multiSampled": False,
                        "arnold:filter": "box_filter",
                    }

        return result



    def update_render_passes(self, scene, render_layer):
        arnold = scene.arnold
        settings = getattr(arnold, "global")
        if settings:
            if settings.aov_combined:
                self.register_pass(scene, render_layer, 'Combined', 4, 'RGBA', 'COLOR')
            if settings.aov_depth:
                self.register_pass(scene, render_layer, 'Depth', 1, 'Z', 'VALUE')
            if settings.aov_position:
                self.register_pass(scene, render_layer, 'P', 3, 'XYZ', 'VECTOR')
            if settings.aov_normal:
                self.register_pass(scene, render_layer, 'N', 3, 'XYZ', 'VECTOR')
            for aov in settings.aov_shaders:
                if aov.name:
                    self.register_pass(scene, render_layer, aov.name, 4, 'RGBA', 'COLOR')

register, unregister = bpy.utils.register_classes_factory((
   ArnoldHydraRenderEngine,
))
