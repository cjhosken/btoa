import bpy
import os, subprocess
from bpy.props import *
        
# Define the export operator
class ARNOLD_OT_ExportASS(bpy.types.Operator):
    bl_idname = "arnold.export_ass"
    bl_description="Export Arnold ASS (.ass) file"
    bl_label = "Export Arnold ASS (.ass)"
    
    filepath: StringProperty(subtype="FILE_PATH", default=os.path.join(os.path.expanduser("~"), "scene.ass"))

    keep_usd : BoolProperty(
        name="Export USD",
        description="Export a .usd file alongisde an .ass file.",
        default=True
    )

    export_selection_only: BoolProperty(
        name="Export Selection Only",
        description="Export only the selected objects",
        default=False
    )

    export_visible_only: BoolProperty(
        name="Export Visible Only",
        description="Export only the visible objects",
        default=False
    )

    export_animation: BoolProperty(
        name="Export Animation",
        description="Export the animation",
        default=False
    )

    def execute(self, context):
        print(self.filepath)
        if len(os.path.basename(self.filepath)) < 1:
            return {"FINISHED"}
        
        # Export the current Blender scene to a USD file
        usd_filepath = os.path.splitext(self.filepath)[0] + ".usd"

        bpy.ops.wm.usd_export(filepath=usd_filepath, 
                              selected_objects_only=self.export_selection_only, 
                              visible_objects_only=self.export_visible_only,
                              export_animation=self.export_animation,
                              export_materials=False
                              )
        
        # https://docs.blender.org/api/current/bpy.ops.wm.html

        print(f"Exported USD file to {usd_filepath}")
        
        # Convert the USD file to RDLA/RDLB
        ass_filepath = self.convert_usd_to_ass(usd_filepath)
        if ass_filepath:
            print(f"Converted USD to ASS: {ass_filepath}")
            # Delete the temporary USD file
            try:
                if (not self.keep_usd):
                    os.remove(usd_filepath)
                    print(f"Deleted temporary USD file: {usd_filepath}")
            except OSError as e:
                print(f"Error deleting USD file: {e}")
        else:
            print("Conversion failed.")
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
    def convert_usd_to_ass(self, usd_filepath):
        # Set up paths

        ass_filepath = os.path.splitext(usd_filepath)[0] + ".ass"
        
        # Construct the command to source the setup script and run the conversion

        command = f'{os.path.join(os.path.expanduser("~"), ".btoa/arnoldSDK/bin/kick")} -i {usd_filepath} -resave {ass_filepath}'
        
        try:
            # Run the command in a shell
            subprocess.run(command, shell=True, check=True, executable="/bin/bash")

            texture_path = os.path.join(os.path.dirname(ass_filepath), "textures")
            maketx_path = os.path.join(os.path.expanduser("~"), ".btoa/arnoldSDK/bin/maketx")

            if os.path.exists(texture_path):
                for file in os.listdir(texture_path):
                    file_path = os.path.join(texture_path, file)

                    if not file.lower().endswith(('.jpg', '.png', '.tif', '.tiff', '.exr')):
                        print(f"Skipping non-image file: {file}")
                        continue

                    # Define the command to convert to .tx
                    maketx_command = [maketx_path, file_path]

                    subprocess.run(maketx_command, shell=True, check=True, executable="/bin/bash")

            return ass_filepath
        except subprocess.CalledProcessError as e:
            print(f"Error during USD to ASS conversion: {e}")
            return None
        
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
classes = [ARNOLD_OT_ExportASS]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)