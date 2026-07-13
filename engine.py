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

        is_viewport = (engine_type == "VIEWPORT")

        # Resolve which AOV is routed to viewport display buffer
        active_aov = "RGBA"
        if is_viewport:
            try:
                found = False
                # Retrieve active shading properties by scanning view 3D spaces
                for window in bpy.context.window_manager.windows:
                    for area in window.screen.areas:
                        if area.type == 'VIEW_3D':
                            space = area.spaces.active
                            if space and space.type == 'VIEW_3D' and space.shading.type == 'RENDERED':
                                active_aov = space.shading.arnold.viewport_aov
                                found = True
                                break
                    if found:
                        break
            except Exception:
                pass

        if is_viewport:
            print(f"[BtoA] Active Viewport AOV: {active_aov}")

        # Viewport always needs the beauty/active pass; final renders respect the checkbox
        if is_viewport or (final and final.aov_combined):
            if is_viewport:
                result["aovToken:Combined"] = "color" if active_aov == "RGBA" else active_aov
            else:
                result["aovToken:Combined"] = "color"

        if settings is not None:
            result |= {
                "arnold:global:viewport_update_trigger": settings.viewport_update_trigger,
                "arnold:global:enable_progressive_render": True if is_viewport else settings.enable_progressive_render,
                "arnold:global:enable_adaptive_sampling": settings.enable_adaptive_sampling,
                "arnold:global:threads": 0 if settings.autodetect_threads else settings.threads,
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
                "arnold:global:enable_gpu_rendering": (final.render_device == "GPU") if final else False,
                "arnold:global:render_device": final.render_device if final else "CPU",
                "arnold:global:render_device_fallback": final.render_device_fallback if final else "cpu",
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


        if is_viewport or (final and final.aov_combined):
            if active_aov == "depth":
                result["aovDescriptor:Combined"] = {
                    "sourceName": "Z",
                    "sourceType": "raw",
                    "dataType": "color4f" if is_viewport else "float",
                    "driver:parameters:aov:name": "RGBA",
                    "driver:parameters:aov:format": "color4f" if is_viewport else "float",
                    "driver:parameters:aov:clearValue": 1e30,
                    "driver:parameters:aov:multiSampled": False,
                    "arnold:filter": "closest_filter",
                }
            elif active_aov == "A":
                result["aovDescriptor:Combined"] = {
                    "sourceName": "A",
                    "sourceType": "raw",
                    "dataType": "color4f" if is_viewport else "float",
                    "driver:parameters:aov:name": "RGBA",
                    "driver:parameters:aov:format": "color4f" if is_viewport else "float",
                    "driver:parameters:aov:clearValue": 0.0,
                    "driver:parameters:aov:multiSampled": False,
                    "arnold:filter": "box_filter",
                }
            else:
                filt = "closest_filter" if active_aov in {"P", "N", "motionvector"} else "box_filter"
                result["aovDescriptor:Combined"] = {
                    "sourceName": active_aov,
                    "sourceType": "raw",
                    "dataType": "color4f" if is_viewport else ("color3f" if active_aov != "RGBA" else "color4f"),
                    "driver:parameters:aov:name": "RGBA",
                    "driver:parameters:aov:format": "color4f" if is_viewport else ("color3f" if active_aov != "RGBA" else "color4f"),
                    "driver:parameters:aov:clearValue": 0,
                    "driver:parameters:aov:multiSampled": False,
                    "arnold:filter": filt,
                }
        if (is_viewport and active_aov != "depth") or (final and final.aov_depth):
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
        if (not is_viewport) and (final and final.aov_position):
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
        if (not is_viewport) and (final and final.aov_normal):
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
        for prop, arnold_name, pass_name, data_type, fmt, filt in [
            ("diffuse", "diffuse", "Diffuse", "color3f", "color3f", "box_filter"),
            ("specular", "specular", "Specular", "color3f", "color3f", "box_filter"),
            ("transmission", "transmission", "Transmission", "color3f", "color3f", "box_filter"),
            ("sss", "sss", "SSS", "color3f", "color3f", "box_filter"),
            ("volume", "volume", "Volume", "color3f", "color3f", "box_filter"),
            ("direct", "direct", "Direct", "color3f", "color3f", "box_filter"),
            ("indirect", "indirect", "Indirect", "color3f", "color3f", "box_filter"),
            ("coat", "coat", "Coat", "color3f", "color3f", "box_filter"),
            ("sheen", "sheen", "Sheen", "color3f", "color3f", "box_filter"),
            ("emission", "emission", "Emission", "color3f", "color3f", "box_filter"),
            ("albedo", "albedo", "Albedo", "color3f", "color3f", "box_filter"),
            ("diffuse_direct", "diffuse_direct", "Diffuse Direct", "color3f", "color3f", "box_filter"),
            ("diffuse_indirect", "diffuse_indirect", "Diffuse Indirect", "color3f", "color3f", "box_filter"),
            ("specular_direct", "specular_direct", "Specular Direct", "color3f", "color3f", "box_filter"),
            ("specular_indirect", "specular_indirect", "Specular Indirect", "color3f", "color3f", "box_filter"),
            ("transmission_direct", "transmission_direct", "Transmission Direct", "color3f", "color3f", "box_filter"),
            ("transmission_indirect", "transmission_indirect", "Transmission Indirect", "color3f", "color3f", "box_filter"),
            ("sss_direct", "sss_direct", "SSS Direct", "color3f", "color3f", "box_filter"),
            ("sss_indirect", "sss_indirect", "SSS Indirect", "color3f", "color3f", "box_filter"),
            ("volume_direct", "volume_direct", "Volume Direct", "color3f", "color3f", "box_filter"),
            ("volume_indirect", "volume_indirect", "Volume Indirect", "color3f", "color3f", "box_filter"),
            ("motionvector", "motionvector", "Motion Vector", "color3f", "color3f", "closest_filter"),
            ("alpha", "A", "Alpha", "float", "float", "box_filter")
        ]:
            if (not is_viewport) and final and getattr(final, f"aov_{prop}", False):
                result[f"aovToken:{pass_name}"] = arnold_name
                result[f"aovDescriptor:{pass_name}"] = {
                    "sourceName": arnold_name,
                    "sourceType": "raw",
                    "dataType": data_type,
                    "driver:parameters:aov:name": arnold_name,
                    "driver:parameters:aov:format": fmt,
                    "driver:parameters:aov:clearValue": 0.0,
                    "driver:parameters:aov:multiSampled": False,
                    "arnold:filter": filt,
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
            for prop, arnold_name, pass_name, channels, channel_name, pass_type in [
                ("diffuse", "diffuse", "Diffuse", 3, "RGB", "COLOR"),
                ("specular", "specular", "Specular", 3, "RGB", "COLOR"),
                ("transmission", "transmission", "Transmission", 3, "RGB", "COLOR"),
                ("sss", "sss", "SSS", 3, "RGB", "COLOR"),
                ("volume", "volume", "Volume", 3, "RGB", "COLOR"),
                ("direct", "direct", "Direct", 3, "RGB", "COLOR"),
                ("indirect", "indirect", "Indirect", 3, "RGB", "COLOR"),
                ("coat", "coat", "Coat", 3, "RGB", "COLOR"),
                ("sheen", "sheen", "Sheen", 3, "RGB", "COLOR"),
                ("emission", "emission", "Emission", 3, "RGB", "COLOR"),
                ("albedo", "albedo", "Albedo", 3, "RGB", "COLOR"),
                ("diffuse_direct", "diffuse_direct", "Diffuse Direct", 3, "RGB", "COLOR"),
                ("diffuse_indirect", "diffuse_indirect", "Diffuse Indirect", 3, "RGB", "COLOR"),
                ("specular_direct", "specular_direct", "Specular Direct", 3, "RGB", "COLOR"),
                ("specular_indirect", "specular_indirect", "Specular Indirect", 3, "RGB", "COLOR"),
                ("transmission_direct", "transmission_direct", "Transmission Direct", 3, "RGB", "COLOR"),
                ("transmission_indirect", "transmission_indirect", "Transmission Indirect", 3, "RGB", "COLOR"),
                ("sss_direct", "sss_direct", "SSS Direct", 3, "RGB", "COLOR"),
                ("sss_indirect", "sss_indirect", "SSS Indirect", 3, "RGB", "COLOR"),
                ("volume_direct", "volume_direct", "Volume Direct", 3, "RGB", "COLOR"),
                ("volume_indirect", "volume_indirect", "Volume Indirect", 3, "RGB", "COLOR"),
                ("motionvector", "motionvector", "Motion Vector", 3, "XYZ", "VECTOR"),
                ("alpha", "A", "Alpha", 1, "X", "VALUE")
            ]:
                if getattr(settings, f"aov_{prop}", False):
                    self.register_pass(scene, render_layer, pass_name, channels, channel_name, pass_type)

register, unregister = bpy.utils.register_classes_factory((
   ArnoldHydraRenderEngine,
))
