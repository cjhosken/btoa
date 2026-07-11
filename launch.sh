#!/bin/bash
export BTOA_ROOT="$HOME/.btoa/btoa-5.2-7.4.5.1"

SCRIPT_DIR="$(dirname "$(realpath "$0")")"

export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
export LD_LIBRARY_PATH="$BTOA_ROOT/bin:$LD_LIBRARY_PATH"
export OCIO="$BTOA_ROOT/ocio/configs/arnold/config.ocio"

/public/software/blender_foundation/blender/blender-5.2-linux-x64/blender --python-expr "import btoa; btoa.register()"