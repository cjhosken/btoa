# Arnold for Blender (btoa)

`btoa` is a high-performance integration of Autodesk's **Arnold Production Renderer** inside of Blender, utilizing the **USD Hydra** rendering framework (`HdArnold`).

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
python3 build.py --blender-version=5.2 --arnoldusd-version=7.4.5.2 --arnoldsdk=/path/to/arnold-sdk
```

Optional build parameters:
- `--blender-version`: Specify target Blender version (defaults to `5.2`).
- `--arnoldusd-version`: Specify target Arnold version (defaults to `7.4.5.2`).
- `--arnoldsdk`: path to the local Arnold SDK.
- `--build-dir`: Custom build workspace directory.
- `--install-dir`: Custom install location for built libraries.

### Installing and Running
Use the provided `launch.sh` wrapper script to set up environment paths (such as `PYTHONPATH` and `LD_LIBRARY_PATH`) and link the plugin to Blender's addons directory automatically:

```bash
./launch.sh
```

---

## Community & Help

- Join the discussion on the [Arnold for Blender Discord](https://discord.gg/TeVFR5JVE) for support, updates, and community sharing.

---

## Acknowledgements

- **Christopher Hosken** (Lead Developer)
- Autodesk Team
- Blender Foundation