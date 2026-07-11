#!/usr/bin/env bash
set -euo pipefail

BTOA_ROOT="${BTOA_ROOT:-$HOME/.btoa/btoa-5.2-7.4.5.1}"
BIN_DIR="$BTOA_ROOT/bin"
PLUGIN_DIR="$BTOA_ROOT/plugin"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

export BTOA_ROOT
export LD_LIBRARY_PATH="${BIN_DIR}:${LD_LIBRARY_PATH:-}"
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH:-}"
export OCIO="${OCIO:-$BTOA_ROOT/ocio/configs/arnold/config.ocio}"

exec /public/software/blender_foundation/blender/blender-5.2-linux-x64/blender "$@"
