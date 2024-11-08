@echo off
setlocal enabledelayedexpansion

:: Define variables
set SCRIPT_DIR=%~dp0
set DEFAULT_BTOA_DIR=%USERPROFILE%\.btoa
set BTOA_DIR=%DEFAULT_BTOA_DIR%

:: Parse command-line arguments
:parse_args
if "%~1"=="" goto done
if "%~1"=="--btoa-dir" (
    set BTOA_DIR=%~2
    shift
    shift
    goto parse_args
) else (
    echo Unknown option: %1
    echo Usage: %0 [--btoa-dir /path/to/btoa]
    exit /b 1
)

:done
echo BTOA_DIR: %BTOA_DIR%

:: Create necessary directories
if not exist "%BTOA_DIR%" mkdir "%BTOA_DIR%"
cd /d "%BTOA_DIR%"

:: Clone the Arnold USD repository
git clone https://github.com/Autodesk/arnold-usd.git "%BTOA_DIR%\source"

:: Initialize dependencies directory
mkdir "%BTOA_DIR%\dependencies"
cd /d "%BTOA_DIR%\dependencies"

:: Add remote and configure sparse checkout for dependencies
git init
git remote add -f origin https://projects.blender.org/blender/lib-windows_x64.git
git config core.sparseCheckout true

:: Set the sparse checkout file
echo boost > .git\info\sparse-checkout
echo imath >> .git\info\sparse-checkout
echo materialx >> .git\info\sparse-checkout
echo opencolorio >> .git\info\sparse-checkout
echo openexr >> .git\info\sparse-checkout
echo openimagedenoise >> .git\info\sparse-checkout
echo openimageio >> .git\info\sparse-checkout
echo opensubdiv >> .git\info\sparse-checkout
echo openvdb >> .git\info\sparse-checkout
echo python >> .git\info\sparse-checkout
echo tbb >> .git\info\sparse-checkout
echo usd >> .git\info\sparse-checkout

:: Fetch the dependencies and checkout specific commit
git fetch origin
git checkout 283d5458d373814824e5675d6fcd7a67d7c50cfb
git pull

:: Copy configuration files for linux_x64 (you may need to adjust these for Windows)
cd /d "%BTOA_DIR%"
xcopy /E /I "%SCRIPT_DIR%\configs\windows_x64" "%BTOA_DIR%\dependencies" /Y

:: Create ArnoldUSD directories
mkdir "%BTOA_DIR%\arnoldusd"
mkdir "%BTOA_DIR%\arnoldusd\arnoldsdk"

:: Copy ArnoldSDK files for linux_x64 (adjust for Windows as needed)
xcopy /E /I "%SCRIPT_DIR%arnoldsdk\windows_x64" "%BTOA_DIR%\arnoldusd\arnoldsdk" /Y

del "%BTOA_DIR%\source\cmake\modules\FindUSD.cmake"
del "%BTOA_DIR%\source\cmake\modules\FindTBB.cmake"

:: Create build directory
cd /d "%BTOA_DIR%\source"
mkdir build
cd build

:: Set environment variables for library paths
set DYLD_LIBRARY_PATH=%BTOA_DIR%\dependencies\tbb\lib;%BTOA_DIR%\dependencies\boost\lib;%BTOA_DIR%\dependencies\materialx\lib;%BTOA_DIR%\dependencies\imath\lib;%BTOA_DIR%\dependencies\openvdb\lib;%BTOA_DIR%\dependencies\opensubdiv\lib;%BTOA_DIR%\dependencies\openimageio\lib;%LD_LIBRARY_PATH%

:: Run CMake with the necessary flags
cmake .. ^
    -DARNOLD_LOCATION=%BTOA_DIR%\arnoldusd\arnoldsdk ^
    -DUSD_LOCATION=%BTOA_DIR%\dependencies\usd ^
    -DCMAKE_PREFIX_PATH="%BTOA_DIR%\dependencies" ^
    -DCMAKE_INSTALL_PREFIX=%BTOA_DIR%\arnoldusd ^
    -DBUILD_SCHEMAS=OFF ^
    -DBUILD_USDGENSCHEMA_ARNOLD=OFF ^
    -DBUILD_DOCS=OFF
cmake --build .

echo ArnoldUSD has been successfully built at %BTOA_DIR%!
