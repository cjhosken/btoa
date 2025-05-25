#!/bin/bash

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
SOURCE_DIR=$SCRIPT_DIR/source
BUILD_DIR=$SCRIPT_DIR/build
INSTALL_DIR=$SCRIPT_DIR/arnoldusd
BLENDER_DIR=$SCRIPT_DIR/build-deps
ARNOLD_DIR=$SCRIPT_DIR/arnoldsdk
ARNOLD_VERSION=7.4.2.0
BLENDER_VERSION=4.4

git clone https://github.com/Autodesk/arnold-usd.git $SOURCE_DIR
cd $SOURCE_DIR
git checkout Arnold-$ARNOLD_VERSION

cd $SCRIPT_DIR

git clone https://projects.blender.org/blender/lib-linux_x64.git $BLENDER_DIR
cd $BLENDER_DIR
git checkout blender-v$BLENDER_VERSION-release

if [ ! -d "$ARNOLD_DIR" ]; then
    curl -L https://github.com/cjhosken/btoa/releases/download/arnoldsdk-$ARNOLD_VERSION/Arnold-$ARNOLD_VERSION-linux.tgz -o "$SCRIPT_DIR/arnoldsdk.tgz"
    mkdir -p "$ARNOLD_DIR"
    tar -xzf "$SCRIPT_DIR/arnoldsdk.tgz" -C "$ARNOLD_DIR"
fi

mkdir -p $BUILD_DIR
cd $BUILD_DIR

cmake $SOURCE_DIR \
    -DCMAKE_CXX_STANDARD=14 \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR \
    -DCMAKE_PREFIX_PATH="$SCRIPT_DIR/build-deps" \
    -DARNOLD_LOCATION=$ARNOLD_DIR \
    -DUSD_LOCATION="$SCRIPT_DIR/build-deps/usd" \
    -DPython3_ROOT="$SCRIPT_DIR/build-deps/python" \
    -DBUILD_SCHEMAS=OFF \
    -DBUILD_USDGENSCHEMA_ARNOLD=ON \
    -DBUILD_DOCS=OFF \
    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON \
    -DCMAKE_INSTALL_RPATH="$ARNOLD_DIR/bin"

make
make install

echo "ArnoldUSD has been successfully built at $BTOA_DIR!"