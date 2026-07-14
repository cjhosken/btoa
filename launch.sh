#!/usr/bin/env bash
set -euo pipefail

BTOA_ROOT="${BTOA_ROOT:-$HOME/.btoa/btoa-5.2-7.4.5.1}"
BIN_DIR="$BTOA_ROOT/bin"
PLUGIN_DIR="$BTOA_ROOT/plugin"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Ensure the addon is symlinked into Blender's user config addons folder
# so it shows up in Blender's Add-ons preferences.
BLENDER_VERSION="5.2"
ADDONS_DIR="$HOME/.config/blender/${BLENDER_VERSION}/scripts/addons"
mkdir -p "$ADDONS_DIR"
if [ ! -e "$ADDONS_DIR/btoa" ]; then
    echo "[BtoA] Linking addon to Blender addons directory..."
    ln -sf "$SCRIPT_DIR" "$ADDONS_DIR/btoa"
fi

export BTOA_ROOT
export LD_LIBRARY_PATH="${BIN_DIR}:${LD_LIBRARY_PATH:-}"
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH:-}"
export OCIO="${OCIO:-$BTOA_ROOT/ocio/configs/arnold/config.ocio}"

exec /home/s5605094/Downloads/blender-5.2.0-candidate+v52.710df102694f-linux.x86_64-release/blender "$@"
