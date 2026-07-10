#!/bin/bash
export BTOA_ROOT="$HOME/.btoa/btoa-5.1-7.4.4.0"

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
GRANDPARENT_DIR="$(dirname "$SCRIPT_DIR")"

echo $GRANDPARENT_DIR

export LD_LIBRARY_PATH="$BTOA_ROOT/bin:$LD_LIBRARY_PATH"
export PATH="$BTOA_ROOT/bin:$PATH"

export PYTHONPATH=$GRANDPARENT_DIR:$PYTHONPATH
export ARNOLD_PLUGIN_PATH="$BTOA_ROOT/plugin:$BTOA_ROOT/plugins:$BTOA_ROOT/procedural:$ARNOLD_PLUGIN_PATH"
export OCIO="$BTOA_ROOT/ocio/configs/arnold/config.ocio"

export TF_DEBUG="USD*"

/usr/local/bin/blender --python-use-system-env --python-expr "import btoa; btoa.register()"