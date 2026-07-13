# Arnold for Blender (btoa)

`btoa` is a high-performance integration of Autodesk's **Arnold Production Renderer** inside of Blender, utilizing the **USD Hydra** rendering framework (`HdArnold`).

---

## Key Features

- **USD Hydra Render Delegate Integration**: Fully connects Blender's geometry and material data with the Autodesk Arnold USD backend.
- **Interactive Viewport Rendering**: Real-time rendering directly within the 3D viewport with support for Blender's shading modes.
- **Progressive Refinement**: Highly responsive look-development via progressive image refinement inside the viewport.
- **Custom Viewport AOVs**: Switch between different viewport render passes (Combined, Depth, Position, Normal, Diffuse, Specular, etc.) on the fly.
- **Flexible Render Devices**: Seamlessly switch between CPU and GPU rendering directly from Blender's Render properties.
- **Thread Optimization**: Automatic detection of available logical CPU cores for optimal rendering performance.

---

## Getting Started

### Prerequisites
Before building and running the plugin, ensure you have:
- **Blender** (v5.2 recommended)
- **Arnold SDK** (v7.4.5.2 or newer)
- **CMake** (v3.12 or newer)
- **Git**
- A C++ compiler supporting C++17 (e.g. GCC 13+ on Linux)

### Building the Delegate
The repository contains a build helper script `build.py` to compile the Arnold USD render delegate. Run the script with the path to your local Arnold SDK:

```bash
python3 build.py --arnold-sdk /path/to/arnold-sdk
```

Optional build parameters:
- `--blender-version`: Specify target Blender version (defaults to `5.2`).
- `--arnold-version`: Specify target Arnold version (defaults to `7.4.5.2`).
- `--build-dir`: Custom build workspace directory.
- `--install-dir`: Custom install location for built libraries.

### Installing and Running
Use the provided `launch.sh` wrapper script to set up environment paths (such as `PYTHONPATH` and `LD_LIBRARY_PATH`) and link the plugin to Blender's addons directory automatically:

```bash
./launch.sh
```

---

## Usage

1. **Select Renderer**: Open Blender, navigate to the **Render Properties** tab, and select **HdArnold** (`ARNOLD`) as the active Render Engine.
2. **Viewport Render**: Switch the 3D Viewport shading mode to **Rendered** (shortcut `Z` -> `Rendered`).
3. **Change Viewport AOV**: In the 3D Viewport header, open the **Render Pass** dropdown under Shading options to switch between available AOVs.
4. **Configure Device**: Change the render device (CPU or GPU) under the Render Properties panel.

---

## Community & Help

- Join the discussion on the [Arnold for Blender Discord](https://discord.gg/TeVFR5JVE) for support, updates, and community sharing.

---

## Acknowledgements

- **Christopher Hosken** (Lead Developer)
- Autodesk Arnold & USD/Hydra Teams