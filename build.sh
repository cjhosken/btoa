ARNOLD_ROOT="$HOME/.arnold"

mkdir -p $ARNOLD_ROOT/{source,build,install}

git clone https://github.com/Autodesk/arnold-usd.git $ARNOLD_ROOT/source/arnoldusd
git clone https://projects.blender.org/blender/lib-linux_x64.git $ARNOLD_ROOT/source/blender

wget https://github.com/cjhosken/btoa/releases/download/arnoldsdk/Arnold-7.4.3.0-linux.tgz -O $ARNOLD_ROOT/source/arnoldsdk.tgz

mkdir -p $ARNOLD_ROOT/source/arnoldsdk
tar -xvzf $ARNOLD_ROOT/source/arnoldsdk.tgz -C $ARNOLD_ROOT/source/arnoldsdk
rm $ARNOLD_ROOT/source/arnoldsdk.tgz

cd $ARNOLD_ROOT/build



mkdir -p $ARNOLD_ROOT/install/arnoldusd

# Currently there are problems with BUILD_USDGENSCHEMA_ARNOLD, BUILD_SCHEMAS, and BUILD_PROCEDURAL.
cmake $ARNOLD_ROOT/source/arnoldusd \
    -DCMAKE_INSTALL_PREFIX=$ARNOLD_ROOT/install/arnoldusd \
    -DARNOLD_LOCATION=$ARNOLD_ROOT/source/arnoldsdk \
    -DUSD_INCLUDE_DIR=$ARNOLD_ROOT/source/blender/usd/include \
    -DUSD_LIBRARY_DIR=$ARNOLD_ROOT/source/blender/usd/lib \
    -DUSD_BINARY_DIR=$ARNOLD_ROOT/source/blender/usd/bin \
    -DPython3_ROOT=$ARNOLD_ROOT/source/blender/python/ \
    -DTBB_ROOT_DIR=$ARNOLD_ROOT/source/blender/tbb \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_USDGENSCHEMA_ARNOLD=False \
    -DUSD_MONOLITHIC_BUILD=True \
    -DBUILD_PROCEDURAL=False \
    -DBUILD_DOCS=False \
    -DBUILD_SCHEMAS=False \
    -DBUILD_TESTSUITE=False

cmake --build . --target install -- -j$(nproc)

cp -r $ARNOLD_ROOT/source/arnoldsk/* $ARNOLD_ROOT/install/arnoldusd/