#!/bin/bash

SCRIPT_DIR="$(dirname "$(realpath "$0")")"

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

echo -e "boost\nimath\nmaterialx\nopencolorio\nopenexr\nopenimagedenoise\nopenimageio\nopensubdiv\nopenvdb\npython\nusd\ntbb" > .git/info/sparse-checkout

git fetch origin

git checkout 483736b00b6a767342e30f5bd95eebcc3c6a4219

cd $BTOA_DIR

cp -r $SCRIPT_DIR/configs/linux_x64/* $BTOA_DIR/dependencies

mkdir -p $BTOA_DIR/arnoldusd
mkdir -p $BTOA_DIR/arnoldusd/arnoldsdk

cp -r $SCRIPT_DIR/arnoldsdk/linux_x64/* $BTOA_DIR/arnoldusd/arnoldsdk

cd $BTOA_DIR/source 
mkdir -p build
cd build

LD_LIBRARY_PATH=$BTOA_DIR/dependencies/boost/lib:$BTOA_DIR/dependencies/tbb/lib:$BTOA_DIR/dependencies/materialx/lib:$BTOA_DIR/dependencies/imath/lib:$BTOA_DIR/dependencies/openvdb/lib:$BTOA_DIR/dependencies/opensubdiv/lib:$BTOA_DIR/dependencies/openimageio/lib:$LD_LIBRARY_PATH

cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DARNOLD_LOCATION=$BTOA_DIR/arnoldusd/arnoldsdk \
    -DUSD_LOCATION=$BTOA_DIR/dependencies/usd \
    -DPython3_ROOT=$BTOA_DIR/dependencies/python \
    -DCMAKE_PREFIX_PATH="$BTOA_DIR/dependencies" \
    -DCMAKE_INSTALL_PREFIX=$BTOA_DIR/arnoldusd \
    -DBUILD_SCHEMAS=OFF \
    -DBUILD_USDGENSCHEMA_ARNOLD=OFF \
    -DBUILD_DOCS=OFF

make
make install

echo "ArnoldUSD has been successfully built at $BTOA_DIR!"