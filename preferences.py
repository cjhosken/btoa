import bpy

from .engine import ArnoldHydraRenderEngine


class BTOA_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = "btoa"

    blender_version: bpy.props.StringProperty(
        name="Blender Version",
        description="Version of Blender libraries to build against",
        default=f"{bpy.app.version[0]}.{bpy.app.version[1]}"
    )
    arnold_version: bpy.props.StringProperty(
        name="Arnold Version",
        description="Arnold SDK version to use",
        default="7.4.4.0"
    )
    arnold_sdk_url: bpy.props.StringProperty(
        name="Arnold SDK URL (Optional)",
        description="Override download URL for Arnold SDK",
        default=""
    )
    arnold_sdk_local: bpy.props.StringProperty(
        name="Local Arnold SDK / Archive",
        description="Use a local directory or tarball (.tgz) instead of downloading",
        default="",
        subtype='FILE_PATH'
    )
    install_dir: bpy.props.StringProperty(
        name="Install Directory",
        description="Destination path for installation (defaults to ~/.btoa)",
        default="",
        subtype='DIR_PATH'
    )
    build_status: bpy.props.StringProperty(
        name="Status",
        default="Idle"
    )
    is_building: bpy.props.BoolProperty(
        name="Is Building",
        default=False
    )
    
    # Main Tabs
    preferences_tab: bpy.props.EnumProperty(
        name="Tab",
        items=[
            ("BUILD", "Build", "Build Settings"),
            ("SYSTEM", "System", "System, Device, Paths & Licensing Settings"),
            ("DIAGNOSTICS", "Diagnostics", "Log and Overrides Settings"),
        ],
        default="BUILD"
    )

    # Collapse state trackers for subpanels
    show_device_settings: bpy.props.BoolProperty(
        name="Show Device Settings",
        default=True
    )
    show_render_settings: bpy.props.BoolProperty(
        name="Show Render Settings",
        default=True
    )
    show_search_paths: bpy.props.BoolProperty(
        name="Show Search Paths",
        default=True
    )
    show_licensing: bpy.props.BoolProperty(
        name="Show Licensing",
        default=True
    )
    show_log: bpy.props.BoolProperty(
        name="Show Log",
        default=True
    )
    show_error_handling: bpy.props.BoolProperty(
        name="Show Error Handling",
        default=True
    )
    show_overrides_settings: bpy.props.BoolProperty(
        name="Show Feature Overrides",
        default=True
    )

    def draw(self, context):
        layout = self.layout
        
        # Horizontal Main Tabs at the top
        row = layout.row(align=True)
        row.prop(self, "preferences_tab", expand=True)
        layout.separator()

        # Robust scene resolution in preferences window
        scene = getattr(context, "scene", None)
        if not scene:
            scene = bpy.context.scene
        if not scene and bpy.data.scenes:
            scene = bpy.data.scenes[0]

        r = None
        if scene and hasattr(scene, "arnold"):
            r = getattr(scene.arnold, "global")

        if self.preferences_tab == 'BUILD':
            layout.label(text="Build USD Render Delegate Settings", icon='SETTINGS')

            box = layout.box()
            box.prop(self, "blender_version")
            box.prop(self, "arnold_version")
            box.prop(self, "arnold_sdk_url")
            box.prop(self, "arnold_sdk_local")
            box.prop(self, "install_dir")

            row = layout.row()
            if self.is_building:
                row.active = False
                row.operator("btoa.build_delegate", text="Building... See terminal for details", icon='FILE_REFRESH')
            else:
                row.operator("btoa.build_delegate", text="Build USD Render Delegate", icon='SYSTEM')

            layout.label(text=f"Status: {self.build_status}")

        elif self.preferences_tab == 'SYSTEM':
            if r:
                # 1. Device Settings (put at the top of System)
                row = layout.row(align=True)
                icon = 'TRIA_DOWN' if self.show_device_settings else 'TRIA_RIGHT'
                row.prop(self, "show_device_settings", icon=icon, text="", emboss=False)
                row.label(text="Device Settings")
                
                if self.show_device_settings:
                    box = layout.box()
                    box.use_property_split = True
                    box.use_property_decorate = False
                    box.prop(r, "render_device_fallback")

                    # Automatic Device Selection subpanel/folder
                    subbox = box.box()
                    subbox.label(text="Automatic Device Selection")
                    subbox.prop(r, "gpu_default_names")
                    subbox.prop(r, "gpu_default_min_memory_MB")

                    # Manual Device Selection subpanel/folder
                    subbox = box.box()
                    subbox.label(text="Manual Device Selection (Local Render)")
                    subbox.prop(r, "manual_device_selection", text="Enable Manual Device Selection")
                    sub = subbox.column()
                    sub.enabled = r.manual_device_selection
                    sub.prop(r, "gpu_default_names", text="GPU Names")
                    sub.prop(r, "gpu_max_texture_resolution")
                
                layout.separator()

                # 2. Render Settings
                row = layout.row(align=True)
                icon = 'TRIA_DOWN' if self.show_render_settings else 'TRIA_RIGHT'
                row.prop(self, "show_render_settings", icon=icon, text="", emboss=False)
                row.label(text="Render Settings")
                
                if self.show_render_settings:
                    box = layout.box()
                    box.use_property_split = True
                    box.use_property_decorate = False
                    box.prop(r, "bucket_scanning")
                    box.prop(r, "bucket_size")
                    box.prop(r, "autodetect_threads")
                    
                    sub = box.column()
                    sub.enabled = not r.autodetect_threads
                    sub.prop(r, "threads")

                layout.separator()

                # 3. Search Paths
                row = layout.row(align=True)
                icon = 'TRIA_DOWN' if self.show_search_paths else 'TRIA_RIGHT'
                row.prop(self, "show_search_paths", icon=icon, text="", emboss=False)
                row.label(text="Search Paths")
                
                if self.show_search_paths:
                    box = layout.box()
                    box.use_property_split = True
                    box.use_property_decorate = False
                    box.prop(r, "absolute_texture_paths")
                    box.prop(r, "absolute_procedural_paths")
                    box.prop(r, "procedural_searchpath")
                    box.prop(r, "plugin_searchpath")
                    box.prop(r, "texture_searchpath")
                
                layout.separator()

                # 4. Licensing
                row = layout.row(align=True)
                icon = 'TRIA_DOWN' if self.show_licensing else 'TRIA_RIGHT'
                row.prop(self, "show_licensing", icon=icon, text="", emboss=False)
                row.label(text="Licensing")
                
                if self.show_licensing:
                    box = layout.box()
                    box.use_property_split = True
                    box.use_property_decorate = False
                    box.prop(r, "abort_on_license_fail")
                    box.prop(r, "skip_license_check")

            else:
                layout.label(text="No active Arnold scene settings found.", icon='ERROR')

        elif self.preferences_tab == 'DIAGNOSTICS':
            if r:
                # 1. Log Collapsible Panel (formerly Diagnostics & Paths)
                row = layout.row(align=True)
                icon = 'TRIA_DOWN' if self.show_log else 'TRIA_RIGHT'
                row.prop(self, "show_log", icon=icon, text="", emboss=False)
                row.label(text="Log")
                
                if self.show_log:
                    box = layout.box()
                    box.use_property_split = True
                    box.use_property_decorate = False
                    box.prop(r, "log_verbosity")
                    box.prop(r, "log_to_console")
                    
                    # Log File + Tickbox to enable it
                    row_file = box.row()
                    row_file.prop(r, "log_to_file")
                    sub = box.column()
                    sub.enabled = r.log_to_file
                    sub.prop(r, "log_file", text="Log File Path")
                    
                    # Statistics File + Tickbox to enable it
                    row_stats = box.row()
                    row_stats.prop(r, "stats_to_file")
                    sub = box.column()
                    sub.enabled = r.stats_to_file
                    sub.prop(r, "stats_file", text="Stats File Path")
                    
                    # Profile file + Tickbox to enable it
                    row_profile = box.row()
                    row_profile.prop(r, "profile_to_file")
                    sub = box.column()
                    sub.enabled = r.profile_to_file
                    sub.prop(r, "profile_file", text="Profile File Path")
                
                layout.separator()

                # 2. Error Handling Collapsible Panel
                row = layout.row(align=True)
                icon = 'TRIA_DOWN' if self.show_error_handling else 'TRIA_RIGHT'
                row.prop(self, "show_error_handling", icon=icon, text="", emboss=False)
                row.label(text="Error Handling")
                
                if self.show_error_handling:
                    box = layout.box()
                    box.use_property_split = True
                    box.use_property_decorate = False
                    box.prop(r, "abort_on_error")
                
                layout.separator()

                # 3. Feature Overrides (Diagnostics subpanel)
                row = layout.row(align=True)
                icon = 'TRIA_DOWN' if self.show_overrides_settings else 'TRIA_RIGHT'
                row.prop(self, "show_overrides_settings", icon=icon, text="", emboss=False)
                row.label(text="Feature Overrides")
                
                if self.show_overrides_settings:
                    box = layout.box()
                    box.use_property_split = True
                    box.use_property_decorate = False
                    box.prop(r, "ignore_textures")
                    box.prop(r, "ignore_shaders")
                    box.prop(r, "ignore_lights")
                    box.prop(r, "ignore_shadows")
                    box.prop(r, "ignore_subdivision")
                    box.prop(r, "ignore_displacement")
                    box.prop(r, "ignore_bump")
                    box.prop(r, "ignore_motion_blur")
                    box.prop(r, "ignore_dof")
                    box.prop(r, "ignore_smoothing")
                    box.prop(r, "ignore_sss")
                    box.prop(r, "ignore_atmosphere")
                    box.prop(r, "ignore_imagers")
            else:
                layout.label(text="No active Arnold scene settings found.", icon='ERROR')


register_classes, unregister_classes = bpy.utils.register_classes_factory((
    BTOA_AddonPreferences,
))


def register():
    register_classes()


def unregister():
    unregister_classes()
