#!/bin/bash

SCRIPT_DIR="$(dirname "$(realpath "$0")")"

ARNOLD_VERISON=7.3.2.1

DEFAULT_BTOA_DIR="$HOME/.btoa"

# Initialize variables with default values
BTOA_DIR="$DEFAULT_BTOA_DIR"

# Parse command-line arguments using getopts
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --btoa-dir)
            BTOA_DIR="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--btoa-dir /path/to/btoa]"
            exit 1
            ;;
    esac
done

echo "BTOA_DIR: $BTOA_DIR"

mkdir -p "$BTOA_DIR"
cd "$BTOA_DIR"

git clone https://github.com/Autodesk/arnold-usd.git $BTOA_DIR/source

git init $BTOA_DIR/dependencies
cd $BTOA_DIR/dependencies

git remote add -f origin https://projects.blender.org/blender/lib-linux_x64.git
git config core.sparseCheckout true

echo -e "tbb\nimath\nmaterialx\nopencolorio\nopenexr\nopenimagedenoise\nopenimageio\nopensubdiv\nopenvdb\npython\nusd" > .git/info/sparse-checkout

git fetch origin

git checkout blender-v4.4-release

cd $BTOA_DIR

mkdir -p $BTOA_DIR/arnoldusd

if [ ! -d "$BTOA_DIR/arnoldusd/arnoldsdk" ]; then
    curl -L https://downloads.arnoldforblender.com/$ARNOLD_VERISON/Arnold-$ARNOLD_VERISON-linux.zip -o $BTOA_DIR/arnoldusd/arnoldsdk.zip
    unzip $BTOA_DIR/arnoldusd/arnoldsdk.zip -d $BTOA_DIR/arnoldusd/arnoldsdk
fi



cp -r $SCRIPT_DIR/cmake/pxrConfig.cmake $BTOA_DIR/dependencies/usd/

mkdir -p $BTOA_DIR/source/build
cd $BTOA_DIR/source/build

cmake .. \
    -DCMAKE_CXX_STANDARD=14 \
    -DCMAKE_TOOLCHAIN_FILE="" \
    -DCMAKE_INSTALL_PREFIX=$BTOA_DIR/arnoldusd \
    -DCMAKE_PREFIX_PATH="$BTOA_DIR/dependencies" \
    -DARNOLD_LOCATION=$BTOA_DIR/arnoldusd/arnoldsdk \
    -DARNOLD_LIBRARY=$BTOA_DIR/arnoldusd/arnoldsdk/bin/libai.so \
    -Dpxr_DIR=$BTOA_DIR/dependencies/usd \
    -DPython3_ROOT=$BTOA_DIR/dependencies/python \
    -DBUILD_SCHEMAS=OFF \
    -DCMAKE_INSTALL_RPATH="$BTOA_DIR/arnoldusd/arnoldsdk/bin;$BTOA_DIR/dependencies/tbb/lib;$BTOA_DIR/dependencies/materialx/lib;$BTOA_DIR/dependencies/imath/lib;$BTOA_DIR/dependencies/usd/lib;$BTOA_DIR/dependencies/openvdb/lib;$BTOA_DIR/dependencies/opensubdiv/lib;$BTOA_DIR/dependencies/openimageio/lib" \
    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON \
    -DCMAKE_EXE_LINKER_FLAGS="-Wl,--no-as-needed -ltbb"


make
make install

echo "ArnoldUSD has been successfully built at $BTOA_DIR, and LD_LIBRARY_PATH has been updated!"