#!/bin/bash
export BTOA_ROOT="$HOME/.btoa/btoa-5.0-7.4.4.0"

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
GRANDPARENT_DIR="$(dirname "$SCRIPT_DIR")"

echo $GRANDPARENT_DIR

export PXR_PLUGINPATH_NAME="$BTOA_ROOT/plugin:$BTOA_ROOT/lib/usd"
export LD_LIBRARY_PATH="$BTOA_ROOT/bin:$LD_LIBRARY_PATH"
export PATH="$BTOA_ROOT/bin:$PATH"

export PYTHONPATH=$GRANDPARENT_DIR:$PYTHONPATH

export TF_DEBUG="USDIMAGING_*,USD_STAGE_*"

export PROCEDURAL_USE_HYDRA=1

export RLM_LICENSE="5063@burton"

$HOME/software/blender-5.0.0-linux-x64/blender --python-use-system-env --python-expr "import btoa; btoa.register()"