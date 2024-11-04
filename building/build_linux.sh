#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Define variables
ARNOLD_ROOT="$HOME/.btoa"
MY_ARNOLD_VERSION="7.3.4.1"
MY_USD_VERSION="23.11"
MY_CMAKE_VERSION="3.30.5"

# Create required directories
mkdir -p "$ARNOLD_ROOT/deps/src"

# Download and extract USD if not already present
USD_TAR="$ARNOLD_ROOT/deps/src/v$MY_USD_VERSION.tar.gz"
if [ ! -f "$USD_TAR" ]; then
    echo "Downloading USD version $MY_USD_VERSION..."
    wget -P "$ARNOLD_ROOT/deps/src" "https://github.com/PixarAnimationStudios/OpenUSD/archive/refs/tags/v$MY_USD_VERSION.tar.gz"
else
    echo "USD tarball already exists. Skipping download."
fi

if [ ! -d "$ARNOLD_ROOT/deps/src/OpenUSD-$MY_USD_VERSION" ]; then
    echo "Extracting USD..."
    tar -zxf "$USD_TAR" -C "$ARNOLD_ROOT/deps/src"
else
    echo "USD source directory already exists. Skipping extraction."
fi

# Install Python dependencies
python3 -m pip install --user pyside6 PyOpenGL jinja2

# Build USD
if [ ! -d "$ARNOLD_ROOT/deps/lib" ]; then
    echo "Building USD..."
    python3 "$ARNOLD_ROOT/deps/src/OpenUSD-$MY_USD_VERSION/build_scripts/build_usd.py" "$ARNOLD_ROOT/deps"
else
    echo "USD is already built. Skipping build."
fi

# Download and extract USD if not already present
CMAKE_TAR="$ARNOLD_ROOT/deps/src/cmake-$MY_CMAKE_VERSION-linux-x86_64.tar.gz"
if [ ! -f "$CMAKE_TAR" ]; then
    echo "Downloading CMake version $MY_CMAKE_VERSION..."
    wget -P "$ARNOLD_ROOT/deps/src" "https://github.com/Kitware/CMake/releases/download/v$MY_CMAKE_VERSION/cmake-$MY_CMAKE_VERSION-linux-x86_64.tar.gz"
else
    echo "CMake tarball already exists. Skipping download."
fi

if [ ! -d "$ARNOLD_ROOT/deps/src/cmake-$MY_CMAKE_VERSION-linux-x86_64" ]; then
    echo "Extracting CMake..."
    tar -zxf "$CMAKE_TAR" -C "$ARNOLD_ROOT/deps/src"
else
    echo "CMake source directory already exists. Skipping extraction."
fi

PATH="$ARNOLD_ROOT/deps/src/cmake-$MY_CMAKE_VERSION-linux-x86_x64/bin:$ARNOLD_ROOT/deps/bin:$PATH"
PYTHONPATH="$ARNOLD_ROOT/deps/python:$PYTHONPATH"
LD_LIBRARY_PATH="$ARNOLD_ROOT/deps/lib:$LD_LIBRARY_PATH"


# Download and extract Arnold USD plugin if not already present
ARNOLD_TAR="$ARNOLD_ROOT/deps/src/Arnold-$MY_ARNOLD_VERSION.tar.gz"
if [ ! -f "$ARNOLD_TAR" ]; then
    echo "Downloading Arnold USD plugin version $MY_ARNOLD_VERSION..."
    wget -P "$ARNOLD_ROOT/deps/src" "https://github.com/Autodesk/arnold-usd/archive/refs/tags/Arnold-$MY_ARNOLD_VERSION.tar.gz"
else
    echo "Arnold USD tarball already exists. Skipping download."
fi

if [ ! -d "$ARNOLD_ROOT/deps/src/arnold-usd-Arnold-$MY_ARNOLD_VERSION" ]; then
    echo "Extracting Arnold USD..."
    tar -zxf "$ARNOLD_TAR" -C "$ARNOLD_ROOT/deps/src"
else
    echo "Arnold USD source directory already exists. Skipping extraction."
fi

# Set paths and environment variables for building Arnold USD
cd "$ARNOLD_ROOT/deps/src/arnold-usd-Arnold-$MY_ARNOLD_VERSION"

ARNOLD_PATH="$ARNOLD_ROOT/arnoldSDK"
USD_PATH="$ARNOLD_ROOT/deps"
BOOST_INCLUDE="$ARNOLD_ROOT/deps/include"
PYTHON_INCLUDE="/usr/include/python3.9"
SHCXX="/usr/bin/g++"
PYTHON_LIB="/usr/lib"
PYTHON_LIB_NAME="python3.9"
PREFIX="$ARNOLD_ROOT/arnold-usd"

mkdir -p build
cd build

cmake .. \
 -DCMAKE_BUILD_TYPE=Release \
 -DARNOLD_LOCATION=$ARNOLD_PATH \
 -DUSD_LOCATION=$USD_PATH \
 -DBUILD_UNIT_TESTS=ON \
 -DCMAKE_CXX_STANDARD=14 \
 -DCMAKE_INSTALL_PREFIX=$PREFIX 
make
make install
