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
echo vulkan >> .git\info\sparse-checkout
echo openpgl >> .git\info\sparse-checkout
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
git checkout v4.4.0
git pull

:: Copy configuration files for linux_x64 (you may need to adjust these for Windows)
cd /d "%BTOA_DIR%"
xcopy /E /I "%SCRIPT_DIR%\configs\windows_x64" "%BTOA_DIR%\dependencies" /Y

:: Create ArnoldUSD directories
mkdir "%BTOA_DIR%\arnoldusd"
mkdir "%BTOA_DIR%\arnoldusd\arnoldsdk"

:: Copy ArnoldSDK files for linux_x64 (adjust for Windows as needed)
xcopy /E /I "%SCRIPT_DIR%arnoldsdk\windows_x64" "%BTOA_DIR%\arnoldusd\arnoldsdk" /Y

mkdir "%BTOA_DIR%\source\build"
cd "%BTOA_DIR%\source\build"

cmake .. ^
    -G "Visual Studio 17 2022" ^
    -DCMAKE_CXX_STANDARD=14 ^
    -DCMAKE_INSTALL_PREFIX="%BTOA_DIR%\arnoldusd" ^
    -DCMAKE_PREFIX_PATH="%BTOA_DIR%\dependencies" ^
    -DARNOLD_LOCATION="%BTOA_DIR%\arnoldusd\arnoldsdk" ^
    -Dpxr_DIR="%BTOA_DIR%\dependencies\usd" ^
    -DPython3_ROOT_DIR="%BTOA_DIR%\dependencies\python\311" ^
    -DTBB_INCLUDE_DIRS="%BTOA_DIR%\dependencies\tbb\include" ^
    -DBUILD_SCHEMAS=OFF

cmake --build .
cmake --install . --prefix "%BTOA_DIR%\arnoldusd"

echo ArnoldUSD has been successfully built at %BTOA_DIR%!
