import bpy, os


def _set_usd_export_method():
    scene = bpy.context.scene
    if scene is not None:
        scene.hydra.export_method = 'USD'
    return None  # Don't repeat


def get_usd_aov_types(name, user_fmt):
    is_half = (user_fmt == "half")
    if name == "RGBA":
        dataType = "color4f"
    elif name in {"A", "Z", "Z_Back", "Volume_Z", "CPU_Time", "Ray_Count", "AA_Inv_Density"}:
        dataType = "float"
    elif name in {"P", "Pref", "N", "N_Denoise", "Motion_Vector"}:
        dataType = "half3" if is_half else "float3"
    elif name in {"ID", "Object", "Shader"}:
        dataType = "int"
    else:
        dataType = "color3f"

    is_int = (user_fmt == "int")

    if dataType == "color4f":
        fmt = "color4h" if is_half else "color4f"
    elif dataType == "color3f":
        fmt = "color3h" if is_half else "color3f"
    elif dataType in {"vector3f", "point3f", "normal3f", "float3", "half3"}:
        fmt = "half3" if is_half else "float3"
    elif dataType == "float":
        fmt = "float16" if is_half else "float"
    elif dataType == "int":
        fmt = "int"
    else:
        fmt = dataType

    return dataType, fmt


def get_arnold_source_name(name):
    mapping = {
        "RGBA": "RGBA",
        "A": "A",
        "P": "P",
        "Pref": "Pref",
        "N": "N",
        "N_Denoise": "N",
        "Opacity": "opacity",
        "Z": "Z",
        "Z_Back": "Z",
        "Denoise_Albedo": "denoise_albedo",
        "Specular_Direct": "specular_direct",
        "Specular_Indirect": "specular_indirect",
        "Specular_Albedo": "specular_albedo",
        "SSS_Albedo": "sss_albedo",
        "SSS_Direct": "sss_direct",
        "SSS_Indirect": "sss_indirect",
        "Transmission_Direct": "transmission_direct",
        "Transmission_Indirect": "transmission_indirect",
        "Transmission_Albedo": "transmission_albedo",
        "Shadow_Matte": "shadow_matte",
        "Diffuse_Direct": "diffuse_direct",
        "Diffuse_Indirect": "diffuse_indirect",
        "Diffuse_Albedo": "diffuse_albedo",
        "Coat_Direct": "coat_direct",
        "Coat_Indirect": "coat_indirect",
        "Coat_Albedo": "coat_albedo",
        "Sheen_Direct": "sheen_direct",
        "Sheen_Indirect": "sheen_indirect",
        "Sheen_Albedo": "sheen_albedo",
        "Volume_Z": "volume_z",
        "Volume_Albedo": "volume_albedo",
        "Volume_Direct": "volume_direct",
        "Volume_Indirect": "volume_indirect",
        "Volume_Opacity": "volume_opacity",
        "ID": "id",
        "Object": "object",
        "Shader": "shader",
        "Motion_Vector": "motionvector",
        "CPU_Time": "cpu_time",
        "Ray_Count": "ray_count",
        "AA_Inv_Density": "aa_inv_density",
    }
    return mapping.get(name, name.lower())


def filter_to_arnold_string(filt):
    """Convert an ArnoldAovFilter PropertyGroup instance to the Arnold
    filter node-type string expected by aovDescriptor's 'arnold:filter' key.
    Also returns a dict of extra filter params to merge into the descriptor."""
    if filt is None:
        return "box_filter", {}

    ftype = filt.type
    extras = {}

    return ftype, extras


class _BuiltinFilterProxy:
    """Read flat per-AOV filter properties from ArnoldGlobalRenderProperties
    and present the same interface as ArnoldAovFilter so filter_to_arnold_string
    can process them without requiring a PointerProperty."""
    __slots__ = ("type",)

    def __init__(self, r, name):
        p = f"aov_{name}_filter"
        self.type          = getattr(r, f"{p}_type",          "box_filter")


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
                "arnold:global:ignore_sss": settings.ignore_sss,
                "arnold:global:plugin_searchpath": settings.plugin_searchpath,
                "arnold:global:asset_searchpath": settings.asset_searchpath,
                "arnold:global:subdiv_dicing_camera": settings.subdiv_dicing_camera.name if settings.subdiv_dicing_camera else "",
                "arnold:global:subdiv_frustum_culling": settings.subdiv_frustum_culling,
                "arnold:global:enable_gpu_rendering": (settings.render_device == "GPU"),
                "arnold:global:render_device": settings.render_device,
                "arnold:global:render_device_fallback": settings.render_device_fallback,
                "arnold:global:log_verbosity": settings.log_verbosity,
                "arnold:global:log_file": settings.log_file,
                "arnold:global:profile_file": settings.profile_file,
                "arnold:global:report_file": settings.report_file,
                "arnold:global:stats_file": settings.stats_file,
                # Newly added properties mapping:
                "arnold:global:stochastic_volume_interpolation": settings.stochastic_volume_interpolation,
                "arnold:global:procedural_instancing_optimization": settings.procedural_instancing_optimization,
                "arnold:global:indirect_specular_blur": settings.indirect_specular_blur,
                "arnold:global:low_light_threshold": settings.low_light_threshold,
                "arnold:global:nits_per_unit": settings.nits_per_unit,
                "arnold:global:subdiv_frustum_padding": settings.subdiv_frustum_padding,
                "arnold:global:texture_max_memory_MB": settings.texture_max_memory_MB,
                "arnold:global:texture_max_open_files": settings.texture_max_open_files,
                "arnold:global:texture_automip": settings.texture_automip,
                "arnold:global:texture_accept_untiled": settings.texture_accept_untiled,
                "arnold:global:texture_autotile": settings.texture_autotile,
                "arnold:global:texture_accept_unmipped": settings.texture_accept_unmipped,
                "arnold:global:texture_auto_generate_tx": settings.texture_auto_generate_tx,
                "arnold:global:texture_use_existing_tx": settings.texture_use_existing_tx,
                "arnold:global:texture_auto_tx_path": settings.texture_auto_tx_path,
                "arnold:global:gpu_default_names": settings.gpu_default_names,
                "arnold:global:gpu_default_min_memory_MB": settings.gpu_default_min_memory_MB,
                "arnold:global:manual_device_selection": settings.manual_device_selection,
                "arnold:global:device_selection": settings.device_selection,
                "arnold:global:bucket_size": settings.bucket_size,
                "arnold:global:bucket_scanning": settings.bucket_scanning,
                "arnold:global:parallel_node_init": settings.parallel_node_init,
                "arnold:global:abort_on_license_fail": settings.abort_on_license_fail,
                "arnold:global:skip_license_check": settings.skip_license_check,
                "arnold:global:enable_report": settings.enable_report,
                "arnold:global:enable_stats": settings.enable_stats,
                "arnold:global:enable_profile": settings.enable_profile,
                "arnold:global:ignore_operators": settings.ignore_operators,
                "arnold:global:ignore_imagers": settings.ignore_imagers,
            }

        # AOV descriptors tell HdArnold which Arnold internal AOV name to bind
        # to each Blender render pass. Without these, Arnold renders the AOV
        # internally but never writes data to Blender's render buffer.
        # Only meaningful for final renders, not viewport.


        # Combined pass (beauty RGBA)
        if True:
            filt = settings.aov_RGBA_filter_type if settings else "box_filter"
            if is_viewport:
                result["aovToken:Combined"] = "color"
                source_name = get_arnold_source_name(active_aov)
                if active_aov == "Z":
                    filt = getattr(settings, "aov_Z_filter_type", "closest_filter") if settings else "closest_filter"
                elif active_aov == "A":
                    filt = getattr(settings, "aov_A_filter_type", "box_filter") if settings else "box_filter"
                else:
                    filt = getattr(settings, f"aov_{active_aov}_filter_type", "box_filter") if settings else "box_filter"

                result["aovDescriptor:Combined"] = {
                    "sourceName": source_name,
                    "sourceType": "raw",
                    "dataType": "color4f",
                    "driver:parameters:aov:name": "RGBA",
                    "driver:parameters:aov:format": "color4f",
                    "driver:parameters:aov:clearValue": 1e30 if active_aov == "Z" else 0.0,
                    "driver:parameters:aov:multiSampled": False,
                    "arnold:filter": filt,
                }
            else:
                result["aovToken:Combined"] = "color"
                filt_str, filt_extras = filter_to_arnold_string(
                    _BuiltinFilterProxy(final, "RGBA") if final else None
                )
                desc = {
                    "sourceName": "RGBA",
                    "sourceType": "raw",
                    "dataType": "color4f",
                    "driver:parameters:aov:name": "RGBA",
                    "driver:parameters:aov:format": "color4f",
                    "driver:parameters:aov:clearValue": 0.0,
                    "driver:parameters:aov:multiSampled": False,
                    "arnold:filter": filt_str,
                }
                desc.update(filt_extras)
                result["aovDescriptor:Combined"] = desc

        # Depth pass
        if (is_viewport and active_aov != "Z") or (final and getattr(final, "aov_Z_enabled", False)):
            filt_str = "closest_filter"
            filt_extras = {}
            fmt = "float"
            if final:
                filt_str, filt_extras = filter_to_arnold_string(_BuiltinFilterProxy(final, "Z"))
                dataType, fmt = get_usd_aov_types("Z", getattr(final, "aov_Z_format", "float"))

            result["aovToken:Depth"] = "depth"
            desc = {
                "sourceName": "Z",
                "sourceType": "raw",
                "dataType": "float",
                "driver:parameters:aov:name": "Z",
                "driver:parameters:aov:format": fmt,
                "driver:parameters:aov:clearValue": 1e30,
                "driver:parameters:aov:multiSampled": False,
                "arnold:filter": filt_str,
            }
            desc.update(filt_extras)
            result["aovDescriptor:Depth"] = desc

        # Add all other enabled built-in AOVs
        if not is_viewport:
            from .props.aov import BUILTIN_AOVS
            for cat, aovs in BUILTIN_AOVS.items():
                for name, label, def_filt, def_fmt in aovs:
                    if name in {"RGBA", "Z"}:
                        continue
                    if getattr(final, f"aov_{name}_enabled", False):
                        dataType, fmt = get_usd_aov_types(name, getattr(final, f"aov_{name}_format"))
                        arnold_name = get_arnold_source_name(name)
                        filt_str, filt_extras = filter_to_arnold_string(
                            _BuiltinFilterProxy(final, name)
                        )
                        result[f"aovToken:{label}"] = arnold_name
                        desc = {
                            "sourceName": arnold_name,
                            "sourceType": "raw",
                            "dataType": dataType,
                            "driver:parameters:aov:name": label,
                            "driver:parameters:aov:format": fmt,
                            "driver:parameters:aov:clearValue": 0.0,
                            "driver:parameters:aov:multiSampled": False,
                            "arnold:filter": filt_str,
                        }
                        desc.update(filt_extras)
                        result[f"aovDescriptor:{label}"] = desc

        return result


    def update_render_passes(self, scene, render_layer):
        arnold = scene.arnold
        settings = getattr(arnold, "global")
        if not settings:
            return

        from .props.aov import BUILTIN_AOVS
        
        def get_register_params(name, dataType):
            if dataType == "color4f":
                return 4, "RGBA", "COLOR"
            elif dataType == "color3f":
                return 3, "RGB", "COLOR"
            elif dataType in {"vector3f", "point3f", "normal3f", "float3", "half3"}:
                return 3, "XYZ", "VECTOR"
            elif dataType == "float":
                chan = "Z" if name in {"Z", "Z_Back", "Volume_Z"} else "X"
                return 1, chan, "VALUE"
            elif dataType == "int":
                return 1, "X", "VALUE"
            return 3, "RGB", "COLOR"

        # 1. Register built-in AOVs if enabled
        for cat, aovs in BUILTIN_AOVS.items():
            for name, label, def_filt, def_fmt in aovs:
                if name == "RGBA" or getattr(settings, f"aov_{name}_enabled", False):
                    bl_name = 'Combined' if name == 'RGBA' else ('Depth' if name == 'Z' else label)
                    dataType, fmt = get_usd_aov_types(name, getattr(settings, f"aov_{name}_format"))
                    channels, channel_name, pass_type = get_register_params(name, dataType)
                    self.register_pass(scene, render_layer, bl_name, channels, channel_name, pass_type)



register, unregister = bpy.utils.register_classes_factory((
   ArnoldHydraRenderEngine,
))
