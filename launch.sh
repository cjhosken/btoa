#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export BTOA_ROOT=$SCRIPT_DIR/plugins/btoa-5.2-7.4.5.1

BLENDER_VERSION="5.2"
ADDONS_DIR="$HOME/.config/blender/${BLENDER_VERSION}/scripts/addons"
mkdir -p "$ADDONS_DIR"
if [ ! -e "$ADDONS_DIR/btoa" ]; then
    echo "[BtoA] Linking addon to Blender addons directory..."
    ln -sf "$SCRIPT_DIR" "$ADDONS_DIR/btoa"
fi

export LD_LIBRARY_PATH="$BTOA_ROOT/bin:$LD_LIBRARY_PATH"
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
export OCIO="$BTOA_ROOT/ocio/configs/arnold/config.ocio"

exec /home/s5605094/Downloads/blender-5.2.0-candidate+v52.710df102694f-linux.x86_64-release/blender "$@"