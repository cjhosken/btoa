#!/usr/bin/env bash
set -e

############################
# CONFIGURABLE PARAMETERS
############################

BLENDER_VERSION="${1:-5.0}"   # default 5.0 if not passed
ARNOLD_VERSION="${2:-7.4.3.0}" # default 7.4.3.0 if not passed

# Paths
ARNOLD_ROOT="$HOME/.arnold"
BLENDER_LIB_REPO="https://projects.blender.org/blender/lib-linux_x64.git"
ARNOLD_USD_REPO="https://github.com/Autodesk/arnold-usd.git"
ARNOLD_SDK_URL="https://github.com/cjhosken/btoa/releases/download/arnoldsdk/Arnold-${ARNOLD_VERSION}-linux.tgz"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "$SCRIPT_DIR"

rm -rf $ARNOLD_ROOT

############################
# DIRECTORY SETUP
############################

echo "==> Creating directory tree…"
mkdir -p $ARNOLD_ROOT/{source,build,install}

mkdir -p \
    $ARNOLD_ROOT/source/{arnoldusd,blender,arnoldsdk} \
    $ARNOLD_ROOT/install/{arnoldusd}

############################
# FETCH SOURCES
############################

echo "==> Cloning Arnold USD…"
git clone --depth 1 -b "Arnold-$ARNOLD_VERSION" $ARNOLD_USD_REPO $ARNOLD_ROOT/source/arnoldusd

echo "==> Cloning Blender libraries…"
git clone --depth 1 -b "blender-v$BLENDER_VERSION-release" $BLENDER_LIB_REPO $ARNOLD_ROOT/source/blender

echo "==> Downloading Arnold SDK ${ARNOLD_VERSION}…"
wget -q $ARNOLD_SDK_URL -O $ARNOLD_ROOT/source/arnoldsdk.tgz

echo "==> Unpacking Arnold SDK…"
tar -xzf $ARNOLD_ROOT/source/arnoldsdk.tgz -C $ARNOLD_ROOT/source/arnoldsdk
rm $ARNOLD_ROOT/source/arnoldsdk.tgz

############################
# QUICK FIXES
############################

# Currently Arnold USD is looking for an stddef.h file, but modern versions of TBB provide a version.h file instead.
cp $ARNOLD_ROOT/source/blender/tbb/include/tbb/version.h $ARNOLD_ROOT/source/arnoldusd/deps/tbb/include/tbb/stddef.h 

############################
# CONFIGURE & BUILD
############################

echo "==> Running CMake…"
cd $ARNOLD_ROOT/build

cmake $ARNOLD_ROOT/source/arnoldusd \
    -DCMAKE_INSTALL_PREFIX=$ARNOLD_ROOT/install/arnoldusd \
    -DARNOLD_LOCATION=$ARNOLD_ROOT/source/arnoldsdk \
    -DUSD_INCLUDE_DIR=$ARNOLD_ROOT/source/blender/usd/include \
    -DUSD_LIBRARY_DIR=$ARNOLD_ROOT/source/blender/usd/lib \
    -DUSD_BINARY_DIR=$ARNOLD_ROOT/source/blender/usd/bin \
    -DPython3_ROOT=$ARNOLD_ROOT/source/blender/python \
    -DTBB_ROOT_DIR=$ARNOLD_ROOT/source/blender/tbb \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSD_MONOLITHIC_BUILD=True \
    -DBUILD_USDGENSCHEMA_ARNOLD=OFF \
    -DBUILD_PROCEDURAL=OFF \
    -DBUILD_DOCS=OFF \
    -DBUILD_TESTSUITE=OFF \
    -DBUILD_SCHEMAS=OFF

echo "==> Building Arnold USD…"
cmake --build . --target install -- -j$(nproc)

cp -r $ARNOLD_ROOT/source/arnoldsdk/* $ARNOLD_ROOT/install/arnoldusd

mkdir -p $HOME/.config/blender/${BLENDER_VERSION}/scripts/startup/

sed \
    -e "s|__BLENDER_VERSION__|${BLENDER_VERSION}|g" \
    -e "s|__ARNOLD_VERSION__|${ARNOLD_VERSION}|g" \
    "$SCRIPT_DIR/arnold_env.py" > "$HOME/.config/blender/${BLENDER_VERSION}/scripts/startup/arnold_env.py"

echo "==> DONE!"
echo "Arnold USD installed into: ${ARNOLD_ROOT}/install/arnoldusd"