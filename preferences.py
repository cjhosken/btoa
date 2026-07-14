import bpy


class BTOA_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = "btoa"

    blender_version: bpy.props.StringProperty(
        name="Blender Version",
        description="Version of Blender libraries to build against",
        default=".".join(map(str, bpy.app.version[:2]))
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

    def draw(self, context):
        layout = self.layout
    
        layout.label(text="Build USD Render Delegate Settings", icon='SETTINGS')

        box = layout.box()
        box.prop(self, "blender_version")
        box.prop(self, "arnold_version")
        box.prop(self, "arnold_sdk_url")
        box.prop(self, "arnold_sdk_local")
        box.prop(self, "install_dir")

        row = layout.row()
        row.active = not self.is_building
        row.operator(
            "btoa.build_delegate",
            text=(
                "Building... See terminal for details"
                if self.is_building
                else "Build USD Render Delegate"
            ),
            icon="FILE_REFRESH" if self.is_building else "SYSTEM",
        )

        layout.label(text=f"Status: {self.build_status}")


register, unregister = bpy.utils.register_classes_factory((
    BTOA_AddonPreferences,
))