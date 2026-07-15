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

    if sys.platform == "win32":
        pass
    else:
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
    parser.add_argument("--arnoldusd-version", default="7.4.5.1", help="Arnold USD version (default: 7.4.5.1)")
    parser.add_argument("--arnoldsdk", required=True, help="Path to local Arnold SDK directory")
    parser.add_argument("--build-dir", help="Override build workspace directory")
    parser.add_argument("--install-dir", help="Override install destination directory")
    
    args = parser.parse_args()
    
    check_requirements()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = args.build_dir or script_dir
    
    source_dir = os.path.join(workspace_dir, "source")
    build_dir = os.path.join(workspace_dir, "build")
    plugins_dir = os.path.join(workspace_dir, "plugins")
    
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(plugins_dir, exist_ok=True)
    
    blender_version = args.blender_version
    arnold_version = args.arnoldusd_version
    
    install_root = args.install_dir or os.path.join(script_dir, "plugins", f"btoa-{blender_version}-{arnold_version}")
    
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
            f.write("usd/\ntbb/\npython/")
            
        run_cmd(["git", "pull", "--depth", "1", "origin", f"blender-v{blender_version}-release"], cwd=blender_libs_dir) 
    
    # 3. Setup Arnold SDK
    sdk_target_dir = os.path.join(source_dir, "arnoldsdk")
    arnold_sdk_path = os.path.abspath(args.arnoldsdk)
    if not os.path.isdir(arnold_sdk_path):
        log(f"Error: Arnold SDK path does not exist: {arnold_sdk_path}")
        sys.exit(1)
    log(f"Using local Arnold SDK from {arnold_sdk_path}")
    if os.path.exists(sdk_target_dir):
        shutil.rmtree(sdk_target_dir)
    shutil.copytree(arnold_sdk_path, sdk_target_dir)
    
    # 4. Quick fix for stddef.h in TBB
    oneapi_version_h = os.path.join(blender_libs_dir, "tbb", "include", "oneapi", "tbb", "version.h")
    version_h = os.path.join(blender_libs_dir, "tbb", "include", "tbb", "version.h")
    stddef_h = os.path.join(blender_libs_dir, "tbb", "include", "tbb", "tbb_stddef.h")
    
    log("Applying TBB stddef.h fix...")
    if os.path.exists(oneapi_version_h):
        shutil.copy2(oneapi_version_h, stddef_h)
    elif os.path.exists(version_h):
        shutil.copy2(version_h, stddef_h)
    
    # 5. CMake Configure & Build
    log("Running CMake configure...")
    
    blender_python_dir = os.path.join(blender_libs_dir, "python")

    if platform == "windows":
        blender_python_dir = os.path.join(blender_python_dir, "313")

    cmake_args = [
        "cmake", arnold_usd_dir,
        "-DCMAKE_BUILD_TYPE=Release",
        f"-DCMAKE_INSTALL_PREFIX={install_root}",
        "-DCMAKE_TOOLCHAIN_FILE=",
        "-DBUILD_SCHEMAS=OFF",
        "-DBUILD_RENDER_DELEGATE=ON",
        "-DBUILD_NDR_PLUGIN=ON",
        "-DBUILD_SCENE_INDEX=OFF",
        "-DBUILD_USD_IMAGING_PLUGIN=ON",
        "-DBUILD_PROCEDURAL=OFF",
        "-DBUILD_BUNDLE=OFF",
        "-DBUILD_TESTSUITE=OFF",
        "-DBUILD_UNIT_TESTS=OFF",
        "-DBUILD_DOCS=OFF",
        "-DBUILD_DISABLE_CXX11_ABI=OFF",
        "-DBUILD_HEADERS_AS_SOURCES=OFF",
        "-DBUILD_WITH_USD_STATIC=OFF",
        f"-DARNOLD_LOCATION={sdk_target_dir}",
        f"-DUSD_INCLUDE_DIR={os.path.join(blender_libs_dir, 'usd', 'include')}",
        f"-DUSD_LIBRARY_DIR={os.path.join(blender_libs_dir, 'usd', 'lib')}",
        f"-DUSD_BINARY_DIR={os.path.join(blender_libs_dir, 'usd', 'bin')}",
        f"-DUSD_LIBRARIES={os.path.join(blender_libs_dir, 'usd', 'lib', 'usd_ms.dll' if platform == 'windows' else 'usd_ms.lib')}",
        "-DUSD_MONOLITHIC_BUILD=ON",
        f"-DPython3_ROOT={blender_python_dir}",
        f"-DPython3_INCLUDE_DIRS={os.path.join(blender_python_dir, 'include', '' if platform == 'windows' else 'python3.13')}",
        f"-DPython3_LIBRARY={os.path.join(blender_python_dir, 'libs' if platform == 'windows' else 'lib', 'python313.lib' if platform == 'windows' else 'libpython3.13.a')}",
        f"-DPython3_EXECUTABLE={os.path.join(blender_python_dir, 'bin', 'python.exe' if platform == 'windows' else 'python3.13')}",
        f"-DTBB_ROOT_DIR={os.path.join(blender_libs_dir, 'tbb')}"
    ]
    
    if platform == "windows":
        cmake_args.append(f"-DTBB_LIBRARY={os.path.join(blender_libs_dir, 'tbb', 'lib')}")
    else:
        cmake_args.append(f"-DUSD_LOCATION={os.path.join(blender_libs_dir, 'usd')}")
    
    run_cmd(cmake_args, cwd=build_dir)
    
    log("Building Arnold USD delegate...")
    nproc = str(os.cpu_count() or 2)
    if platform == "windows":
        run_cmd(["cmake", "--build", ".", "--config", "Release", "--target", "install", "-j", nproc], cwd=build_dir)
    else:
        run_cmd(["cmake", "--build", ".", "--target", "install", "--", f"-j{nproc}"], cwd=build_dir)
    
    log("Build completed successfully!")

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

    log(f"Copying ArnoldSDK libraries to {install_root}...")
    # Emulate: cp -r $ARNOLD_ROOT/source/arnoldsdk/* $INSTALL_ROOT
    for item in os.listdir(sdk_target_dir):
        s = os.path.join(sdk_target_dir, item)
        d = os.path.join(install_root, item)
        robust_copy(s, d)

    log(f"Installed to: {install_root}")

if __name__ == "__main__":
    main()
