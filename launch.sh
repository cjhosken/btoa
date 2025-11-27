#!/bin/bash
ROOT="$HOME/.arnold/install/arnoldusd"

export PXR_PLUGINPATH_NAME="$ROOT/plugin:$ROOT/lib/usd"
export LD_LIBRARY_PATH="$ROOT/bin:$LD_LIBRARY_PATH"
export PATH="$ROOT/bin:$PATH"

$HOME/software/blender-5.0.0-linux-x64/blender
