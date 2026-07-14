import bpy
import threading
import subprocess
import os
import sys


_build_thread = None
_build_log = []
_build_status = "Idle"


class BTOA_OT_build_delegate(bpy.types.Operator):
    bl_idname = "btoa.build_delegate"
    bl_label = "Build USD Render Delegate"
    bl_description = "Download and compile Arnold USD delegate and SDK libraries"
    
    _timer = None
    
    def modal(self, context, event):
        global _build_thread, _build_status
        
        if event.type == 'TIMER':
            # Check preferences and update status
            try:
                prefs = context.preferences.addons["btoa"].preferences
                prefs.build_status = _build_status
            except KeyError:
                pass
            
            if _build_thread and not _build_thread.is_alive():
                _build_thread = None
                try:
                    prefs = context.preferences.addons["btoa"].preferences
                    prefs.is_building = False
                except KeyError:
                    pass
                context.window_manager.event_timer_remove(self._timer)
                if "success" in _build_status.lower():
                    self.report({'INFO'}, "USD Render Delegate built successfully!")
                else:
                    self.report({'ERROR'}, f"Build failed: {_build_status}")
                return {'FINISHED'}
                
        return {'PASS_THROUGH'}
        
    def execute(self, context):
        global _build_thread, _build_status, _build_log
        
        prefs = context.preferences.addons["btoa"].preferences
        if prefs.is_building:
            self.report({'WARNING'}, "Build already in progress.")
            return {'CANCELLED'}
            
        blender_ver = prefs.blender_version
        arnold_ver = prefs.arnold_version
        sdk_url = prefs.arnold_sdk_url
        sdk_local = prefs.arnold_sdk_local
        install_dir = prefs.install_dir
        
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "build.py")
        cmd = [sys.executable, script_path, "--blender-version", blender_ver, "--arnold-version", arnold_ver]
        
        if sdk_url:
            cmd += ["--arnold-sdk-url", sdk_url]
        if sdk_local:
            cmd += ["--arnold-sdk-local", sdk_local]
        if install_dir:
            cmd += ["--install-dir", install_dir]
            
        prefs.is_building = True
        _build_status = "Starting build..."
        _build_log.clear()
        
        def run_build():
            global _build_status, _build_log
            try:
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                while True:
                    line = process.stdout.readline()
                    if not line:
                        break
                    line_str = line.strip()
                    if line_str.startswith("==> "):
                        _build_status = line_str[4:]
                    _build_log.append(line_str)
                    print(f"[BtoA Build] {line_str}", flush=True)
                process.wait()
                if process.returncode == 0:
                    _build_status = "Build completed successfully!"
                else:
                    _build_status = f"Build failed (code {process.returncode}). Check terminal."
            except Exception as e:
                _build_status = f"Build encountered error: {str(e)}"
                
        _build_thread = threading.Thread(target=run_build, daemon=True)
        _build_thread.start()
        
        self._timer = context.window_manager.event_timer_add(0.2, window=context.window())
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


register, unregister = bpy.utils.register_classes_factory((
    BTOA_OT_build_delegate,
))