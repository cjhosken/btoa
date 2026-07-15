#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import argparse

def log(msg):
    print(f"==> {msg}", flush=True)

def get_platform():
    if sys.platform == "win32":
        return "windows"
    elif sys.platform == "darwin":
        return "macos"
    return "linux"

def check_requirements():
    tools = ["git", "cmake"]
    # Check compiler
    if sys.platform == "win32":
        # Usually Visual Studio on Windows
        pass
    else:
        # check make or ninja
        if not shutil.which("make") and not shutil.which("ninja"):
            tools.append("make/ninja")
            
    missing = []
    for tool in tools:
        if tool == "make/ninja":
            if not shutil.which("make") and not shutil.which("ninja"):
                missing.append("make or ninja")
        elif not shutil.which(tool):
            missing.append(tool)
            
    if missing:
        log(f"Error: Missing required system tools: {', '.join(missing)}")
        sys.exit(1)

def run_cmd(cmd, cwd=None):
    log(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.returncode != 0:
        print(result.stdout)
        log(f"Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description="Build Arnold USD Render Delegate for btoa")
    parser.add_argument("--blender-version", default="5.2", help="Blender version (default: 5.2)")
    parser.add_argument("--arnold-version", default="7.4.5.2", help="Arnold version (default: 7.4.5.2)")
    parser.add_argument("--arnold-sdk", required=True, help="Path to local Arnold SDK directory")
    parser.add_argument("--build-dir", help="Override build workspace directory")
    parser.add_argument("--install-dir", help="Override install destination directory")
    
    args = parser.parse_args()
    
    check_requirements()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = args.build_dir or script_dir
    
    source_dir = os.path.join(workspace_dir, "source")
    build_dir = os.path.join(workspace_dir, "build")
    
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(build_dir, exist_ok=True)
    
    blender_version = args.blender_version
    arnold_version = args.arnold_version
    
    install_root = args.install_dir or os.path.expanduser(f"~/.btoa/btoa-{blender_version}-{arnold_version}")
    
    # 1. Fetch Arnold USD
    arnold_usd_dir = os.path.join(source_dir, "arnoldusd")
    if not os.path.exists(arnold_usd_dir):
        log("Cloning Arnold USD...")
        run_cmd([
            "git", "clone", "--depth", "1", "-b", f"Arnold-{arnold_version}",
            "https://github.com/Autodesk/arnold-usd.git", arnold_usd_dir
        ])
    else:
        log("Arnold USD already exists, skipping clone.")
        
    # 2. Fetch Blender libs (sparse checkout to avoid gigabytes of download)
    platform = get_platform()
    blender_libs_map = {
        "linux": "lib-linux_x64",
        "windows": "lib-windows_x64",
        "macos": "lib-macos_arm64",
    }
    blender_libs_repo = blender_libs_map[platform]
    
    blender_libs_dir = os.path.join(source_dir, "blender")
    if not os.path.exists(blender_libs_dir):
        log("Cloning Blender libraries (using sparse-checkout)...")
        os.makedirs(blender_libs_dir, exist_ok=True)
        run_cmd(["git", "init"], cwd=blender_libs_dir)
        run_cmd(["git", "remote", "add", "origin", f"https://projects.blender.org/blender/{blender_libs_repo}.git"], cwd=blender_libs_dir)
        run_cmd(["git", "config", "core.sparseCheckout", "true"], cwd=blender_libs_dir)
        
        sparse_file = os.path.join(blender_libs_dir, ".git", "info", "sparse-checkout")
        os.makedirs(os.path.dirname(sparse_file), exist_ok=True)
        with open(sparse_file, "w") as f:
            f.write("usd/\ntbb/\npython/\nimath/\nMaterialX/\nvulkan/\n")
            
        run_cmd(["git", "pull", "--depth", "1", "origin", f"blender-v{blender_version}-release"], cwd=blender_libs_dir)
    else:
        log("Blender libraries already exist, skipping clone.")
        needed_dirs = ["imath", "MaterialX", "vulkan"]
        missing = [d for d in needed_dirs if not os.path.isdir(os.path.join(blender_libs_dir, d))]
        if missing:
            log(f"Updating sparse-checkout to add: {', '.join(missing)}")
            sparse_file = os.path.join(blender_libs_dir, ".git", "info", "sparse-checkout")
            existing = ""
            if os.path.exists(sparse_file):
                with open(sparse_file) as f:
                    existing = f.read()
            additions = "\n".join(f"{d}/" for d in missing if f"{d}/" not in existing)
            if additions:
                with open(sparse_file, "a") as f:
                    f.write("\n" + additions + "\n")
            run_cmd(["git", "checkout", f"blender-v{blender_version}-release"], cwd=blender_libs_dir)
        
    # 3. Setup Arnold SDK
    sdk_target_dir = os.path.join(source_dir, "arnoldsdk")
    arnold_sdk_path = os.path.abspath(args.arnold_sdk)
    if not os.path.isdir(arnold_sdk_path):
        log(f"Error: Arnold SDK path does not exist: {arnold_sdk_path}")
        sys.exit(1)
    log(f"Using local Arnold SDK from {arnold_sdk_path}")
    if os.path.exists(sdk_target_dir):
        shutil.rmtree(sdk_target_dir)
    shutil.copytree(arnold_sdk_path, sdk_target_dir)
        
    # Ensure empty directories exist for deps that reference them
    os.makedirs(os.path.join(blender_libs_dir, "MaterialX", "resources"), exist_ok=True)
    
    # 4. Quick fix for stddef.h in TBB
    oneapi_version_h = os.path.join(blender_libs_dir, "tbb", "include", "oneapi", "tbb", "version.h")
    version_h = os.path.join(blender_libs_dir, "tbb", "include", "tbb", "version.h")
    stddef_h = os.path.join(blender_libs_dir, "tbb", "include", "tbb", "tbb_stddef.h")
    
    log("Applying TBB stddef.h fix...")
    if os.path.exists(oneapi_version_h):
        shutil.copy2(oneapi_version_h, stddef_h)
    elif os.path.exists(version_h):
        shutil.copy2(version_h, stddef_h)
    
    # Fix TBB cmake config: generator expression defines TBB_USE_DEBUG without a value
    tbb_targets_cmake = os.path.join(blender_libs_dir, "tbb", "lib", "cmake", "TBB", "TBBTargets.cmake")
    if os.path.exists(tbb_targets_cmake):
        with open(tbb_targets_cmake, "r") as f:
            content = f.read()
        fixed = content.replace("TBB_USE_DEBUG>", "TBB_USE_DEBUG=1>")
        if fixed != content:
            log("Fixing TBBTargets.cmake: TBB_USE_DEBUG missing value")
            with open(tbb_targets_cmake, "w") as f:
                f.write(fixed)
    
    # 5. CMake Configure & Build
    log("Running CMake configure...")
    
    usd_lib_dir = os.path.join(blender_libs_dir, "usd", "lib").replace("\\", "/")
    tbb_lib_dir = os.path.join(blender_libs_dir, "tbb", "lib").replace("\\", "/")
    python_lib_dir = os.path.join(blender_libs_dir, "python", "313", "libs").replace("\\", "/")
    cmake_init = os.path.join(build_dir, "btoa_init.cmake")
    with open(cmake_init, "w") as f:
        f.write(f'link_directories("{usd_lib_dir}" "{tbb_lib_dir}" "{python_lib_dir}")\n')
    
    vulkan_shim_dir = os.path.join(build_dir, "cmake_shims")
    os.makedirs(vulkan_shim_dir, exist_ok=True)
    for name in ["VulkanUtilityLibraries", "VulkanMemoryAllocator"]:
        with open(os.path.join(vulkan_shim_dir, f"{name}Config.cmake"), "w") as f:
            f.write(f"# Minimal {name} shim\n")
            f.write(f"set({name}_FOUND TRUE)\n")
    
    tbb_lib_map = {
        "linux": ("libtbb.so", "libtbbmalloc.so"),
        "windows": ("tbb.lib", "tbbmalloc.lib"),
        "macos": ("libtbb.dylib", "libtbbmalloc.dylib"),
    }
    tbb_tbb, tbb_malloc = tbb_lib_map[platform]
    
    blender_python_dir = os.path.join(blender_libs_dir, "python", "313")
    
    python_lib_map = {
        "linux": "libpython3.13.so",
        "windows": os.path.join("libs", "python313.lib"),
        "macos": "libpython3.13.dylib",
    }
    python_lib = python_lib_map[platform]
    
    python_exe_map = {
        "linux": os.path.join("bin", "python3"),
        "windows": os.path.join("bin", "python.exe"),
        "macos": os.path.join("bin", "python3"),
    }
    python_exe = os.path.join(blender_python_dir, python_exe_map[platform])
    
    cmake_args = [
        "cmake", arnold_usd_dir,
        f"-DCMAKE_BUILD_TYPE=Release",
        f"-DCMAKE_INSTALL_PREFIX={install_root}",
        f"-DARNOLD_LOCATION={sdk_target_dir}",
        f"-DUSD_LOCATION={os.path.join(blender_libs_dir, 'usd')}",
        f"-DUSD_INCLUDE_DIR={os.path.join(blender_libs_dir, 'usd', 'include')}",
        f"-DUSD_LIBRARY_DIR={os.path.join(blender_libs_dir, 'usd', 'lib')}",
        f"-DUSD_BINARY_DIR={os.path.join(blender_libs_dir, 'usd', 'bin')}",
        f"-DPython3_ROOT_DIR={blender_python_dir}",
        f"-DPython3_EXECUTABLE={python_exe}",
        f"-DPython3_INCLUDE_DIR={os.path.join(blender_python_dir, 'include')}",
        f"-DPython3_LIBRARY={os.path.join(blender_python_dir, python_lib)}",
        "-DPython3_VERSION=3.13",
        f"-DTBB_ROOT_DIR={os.path.join(blender_libs_dir, 'tbb')}",
        f"-DTBB_DIR={os.path.join(blender_libs_dir, 'tbb', 'lib', 'cmake', 'TBB')}",
        f"-DTBB_INCLUDE_DIRS={os.path.join(blender_libs_dir, 'tbb', 'include')}",
        f"-DTBB_LIBRARY={os.path.join(blender_libs_dir, 'tbb', 'lib')}",
        f"-DTBB_tbb_LIBRARY={os.path.join(blender_libs_dir, 'tbb', 'lib', tbb_tbb)}",
        f"-DTBB_tbbmalloc_LIBRARY={os.path.join(blender_libs_dir, 'tbb', 'lib', tbb_malloc)}",
        f"-DMaterialX_DIR={os.path.join(blender_libs_dir, 'MaterialX', 'lib', 'cmake', 'MaterialX')}",
        f"-DImath_DIR={os.path.join(blender_libs_dir, 'imath', 'lib', 'cmake', 'Imath')}",
        f"-DVulkanHeaders_DIR={os.path.join(blender_libs_dir, 'vulkan', 'share', 'cmake', 'VulkanHeaders')}",
        f"-DVulkanUtilityLibraries_DIR={vulkan_shim_dir}",
        f"-DVulkanMemoryAllocator_DIR={vulkan_shim_dir}",
        "-DCMAKE_TOOLCHAIN_FILE=",
        f"-DCMAKE_PROJECT_INCLUDE={cmake_init}",
        "-DUSD_MONOLITHIC_BUILD=ON",
        "-DBUILD_USDGENSCHEMA_ARNOLD=OFF",
        "-DBUILD_PROCEDURAL=OFF",
        "-DBUILD_DOCS=OFF",
        "-DBUILD_TESTSUITE=OFF",
        "-DBUILD_SCHEMAS=OFF",
        "-DBUILD_SCENE_INDEX_PLUGIN=ON"
    ]
    
    if platform != "windows":
        cmake_args.append("-DCMAKE_BUILD_TYPE=Release")
    
    run_cmd(cmake_args, cwd=build_dir)
    
    log("Building Arnold USD delegate...")
    nproc = str(os.cpu_count() or 2)
    if platform == "windows":
        run_cmd(["cmake", "--build", ".", "--config", "Release", "--target", "install", "-j", nproc], cwd=build_dir)
    else:
        run_cmd(["cmake", "--build", ".", "--target", "install", "--", f"-j{nproc}"], cwd=build_dir)
    
    def robust_copy(src, dst):
        if os.path.isdir(src):
            os.makedirs(dst, exist_ok=True)
            for item in os.listdir(src):
                robust_copy(os.path.join(src, item), os.path.join(dst, item))
        else:
            if os.path.exists(dst):
                try:
                    os.unlink(dst)
                except Exception:
                    pass
            try:
                shutil.copy2(src, dst)
            except Exception as e:
                log(f"Warning: Failed to copy {src} to {dst}: {e}")

    log("Copying SDK libraries to install target...")
    # Emulate: cp -r $ARNOLD_ROOT/source/arnoldsdk/* $INSTALL_ROOT
    for item in os.listdir(sdk_target_dir):
        s = os.path.join(sdk_target_dir, item)
        d = os.path.join(install_root, item)
        robust_copy(s, d)
            
    log("Build completed successfully!")
    log(f"Installed to: {install_root}")

if __name__ == "__main__":
    main()
