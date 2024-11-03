ARNOLD_ROOT=$HOME/.btoa

mkdir -p $ARNOLD_ROOT

cd $ARNOLD_ROOT
mkdir -p arnoldsdk
mkidr -p installs

mkdir -p deps
mkdir -p deps/src
mkdir -p deps/install

wget -P deps/src https://github.com/Kitware/CMake/releases/download/v3.30.2/cmake-3.30.2-linux-x86_64.tar.gz
tar -zxf deps/src/cmake-3.30.2-linux-x86_64.tar.gz -C deps/src
rm -rf deps/src/cmake-3.30.2-linux-x86_64.tar.gz

export PATH=$ARNOLD_ROOT/deps/src/cmake-3.30.2-linux-x86_64/bin:$PATH

wget -P deps/src https://github.com/PixarAnimationStudios/OpenUSD/archive/refs/tags/v23.11.tar.gz
tar -zxf deps/src/v23.11.tar.gz -C deps/src
rm -rf deps/src/v23.11.tar.gz

python3 -m pip install pyside6
python3 -m pip install PyOpenGL
python3 deps/src/OpenUSD-23.11/build_scripts/build_usd.py $ARNOLD_ROOT/deps/install

wget -P deps/src https://github.com/Autodesk/arnold-usd/archive/refs/tags/Arnold-7.3.4.1.tar.gz
tar -zxf deps/src/Arnold-7.3.4.1.tar.gz -C deps/src
rm -rf deps/src/Arnold-7.3.4.1.tar.gz

cd deps/src/arnold-usd-Arnold-7.3.4.1
mkdir -p build
cd build

cmake .. -DCMAKE_BUILD_TYPE=Release -DARNOLD_LOCATION=$ARNOLD_ROOT/arnoldsdk/Arnold-7.3.4.1-linux -DBUILD_USDGENSCHEMA_ARNOLD=True -DUSD_LOCATION=$ARNOLD_ROOT/deps/install -DBUILD_UNIT_TESTS=OFF -DCMAKE_CXX_STANDARD=14 -DCMAKE_INSTALL_PREFIX=$ARNOLD_ROOT/arnold-usd
make
make install