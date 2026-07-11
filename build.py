#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import argparse

def log(msg):
    print(f"==> {msg}", flush=True)

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
    blender_libs_dir = os.path.join(source_dir, "blender")
    if not os.path.exists(blender_libs_dir):
        log("Cloning Blender libraries (using sparse-checkout)...")
        os.makedirs(blender_libs_dir, exist_ok=True)
        run_cmd(["git", "init"], cwd=blender_libs_dir)
        run_cmd(["git", "remote", "add", "origin", "https://projects.blender.org/blender/lib-linux_x64.git"], cwd=blender_libs_dir)
        run_cmd(["git", "config", "core.sparseCheckout", "true"], cwd=blender_libs_dir)
        
        sparse_file = os.path.join(blender_libs_dir, ".git", "info", "sparse-checkout")
        os.makedirs(os.path.dirname(sparse_file), exist_ok=True)
        with open(sparse_file, "w") as f:
            f.write("usd/\ntbb/\npython/\n")
            
        run_cmd(["git", "pull", "--depth", "1", "origin", f"blender-v{blender_version}-release"], cwd=blender_libs_dir)
    else:
        log("Blender libraries already exist, skipping clone.")
        
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
    cmake_args = [
        "cmake", arnold_usd_dir,
        f"-DCMAKE_INSTALL_PREFIX={install_root}",
        f"-DARNOLD_LOCATION={sdk_target_dir}",
        f"-DUSD_INCLUDE_DIR={os.path.join(blender_libs_dir, 'usd', 'include')}",
        f"-DUSD_LIBRARY_DIR={os.path.join(blender_libs_dir, 'usd', 'lib')}",
        f"-DUSD_BINARY_DIR={os.path.join(blender_libs_dir, 'usd', 'bin')}",
        f"-DPython3_ROOT={os.path.join(blender_libs_dir, 'python')}",
        f"-DTBB_ROOT_DIR={os.path.join(blender_libs_dir, 'tbb')}",
        f"-DTBB_LIBRARY={os.path.join(blender_libs_dir, 'tbb', 'lib')}",
        f"-DTBB_tbb_LIBRARY={os.path.join(blender_libs_dir, 'tbb', 'lib', 'libtbb.so')}",
        f"-DTBB_tbbmalloc_LIBRARY={os.path.join(blender_libs_dir, 'tbb', 'lib', 'libtbbmalloc.so')}",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DCMAKE_TOOLCHAIN_FILE=",
        "-DUSD_MONOLITHIC_BUILD=ON",
        "-DBUILD_USDGENSCHEMA_ARNOLD=OFF",
        "-DBUILD_PROCEDURAL=OFF",
        "-DBUILD_DOCS=OFF",
        "-DBUILD_TESTSUITE=OFF",
        "-DBUILD_SCHEMAS=OFF",
        "-DBUILD_SCENE_INDEX_PLUGIN=ON"
    ]
    run_cmd(cmake_args, cwd=build_dir)
    
    log("Building Arnold USD delegate...")
    # Use nproc to set parallel jobs if available
    nproc = str(os.cpu_count() or 2)
    run_cmd(["cmake", "--build", ".", "--target", "install", "--", f"-j{nproc}"], cwd=build_dir)
    
    log("Copying SDK libraries to install target...")
    # Emulate: cp -r $ARNOLD_ROOT/source/arnoldsdk/* $INSTALL_ROOT
    for item in os.listdir(sdk_target_dir):
        s = os.path.join(sdk_target_dir, item)
        d = os.path.join(install_root, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
            
    log("Build completed successfully!")
    log(f"Installed to: {install_root}")

if __name__ == "__main__":
    main()
