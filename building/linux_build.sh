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

echo -e "boost\nimath\nmaterialx\nopencolorio\nopenexr\nopenimagedenoise\nopenimageio\nopensubdiv\nopenvdb\npython\nusd" > .git/info/sparse-checkout

git fetch origin

git checkout 483736b00b6a767342e30f5bd95eebcc3c6a4219

cd $BTOA_DIR

cp -r $SCRIPT_DIR/configs/linux_x64/* $BTOA_DIR/dependencies

mkdir -p $BTOA_DIR/arnoldusd
mkdir -p $BTOA_DIR/arnoldusd/arnoldsdk

cp -r $SCRIPT_DIR/arnoldsdk/linux_x64/* $BTOA_DIR/arnoldusd/arnoldsdk

mkdir -p $BTOA_DIR/source/build
cd $BTOA_DIR/source/build

LD_LIBRARY_PATH=$BTOA_DIR/dependencies/boost/lib:$BTOA_DIR/dependencies/materialx/lib:$BTOA_DIR/dependencies/imath/lib:$BTOA_DIR/dependencies/openvdb/lib:$BTOA_DIR/dependencies/opensubdiv/lib:$BTOA_DIR/dependencies/openimageio/lib:$LD_LIBRARY_PATH

cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DARNOLD_LOCATION=$BTOA_DIR/arnoldusd/arnoldsdk \
    -DUSD_LOCATION=$BTOA_DIR/dependencies/usd \
    -DPYTHON_INCLUDE_DIR=$BTOA_DIR/dependencies/python/include \
    -DPYTHON_LIBRARY=$BTOA_DIR/dependencies/python/lib/libpython3.11.a \
    -DCMAKE_PREFIX_PATH="$BTOA_DIR/dependencies" \
    -DCMAKE_INSTALL_PREFIX=$BTOA_DIR/arnoldusd \
    -DBUILD_SCHEMAS=OFF \
    -DBUILD_USDGENSCHEMA_ARNOLD=OFF \
    -DBUILD_DOCS=OFF

make
make install

# Define the path to be added
LD_LIBRARY_PATH_UPDATE="$BTOA_DIR/arnoldusd/arnoldsdk/bin"

# Check if LD_LIBRARY_PATH is already set in .bashrc, and add it if not
if ! grep -q "export LD_LIBRARY_PATH=.*$LD_LIBRARY_PATH_UPDATE" "$HOME/.bashrc"; then
    echo >> "$HOME/.bashrc"
    echo "export LD_LIBRARY_PATH=\"$LD_LIBRARY_PATH_UPDATE:\$LD_LIBRARY_PATH\"" >> "$HOME/.bashrc"
    echo "LD_LIBRARY_PATH updated in .bashrc"
else
    echo "LD_LIBRARY_PATH is already set in .bashrc"
fi

# Source .bashrc to make it available in the current session
source "$HOME/.bashrc"

echo "ArnoldUSD has been successfully built at $BTOA_DIR, and LD_LIBRARY_PATH has been updated!"