@echo off
setlocal enabledelayedexpansion

:: Define variables
set SCRIPT_DIR=%~dp0
set DEFAULT_BTOA_DIR=%SCRIPT_DIR%\..\btoa
set BTOA_DIR=%DEFAULT_BTOA_DIR%
set ARNOLD_VERSION=7.3.2.1

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


IF NOT EXIST "%BTOA_DIR%" (

    echo The specified BTOA_DIR does not exist. Creating it now...
    mkdir "%BTOA_DIR%"
)

cd /d "%BTOA_DIR%"

IF NOT EXIST "%BTOA_DIR%\source" (
    :: Clone the Arnold USD repository
    git clone https://github.com/Autodesk/arnold-usd.git "%BTOA_DIR%\source"
)

:: Initialize dependencies directory
IF NOT EXIST "%BTOA_DIR%\dependencies" (
    mkdir "%BTOA_DIR%\dependencies"
)

cd /d "%BTOA_DIR%\dependencies"

:: Add remote and configure sparse checkout for dependencies
git init
git remote add -f origin https://projects.blender.org/blender/lib-windows_x64.git
git config core.sparseCheckout true

:: Set the sparse checkout file
echo vulkan >> .git\info\sparse-checkout
echo boost >> .git\info\sparse-checkout
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
git checkout blender-v4.2-release

:: Create ArnoldUSD directories
IF NOT EXIST "%BTOA_DIR%\arnoldusd" (
    mkdir "%BTOA_DIR%\arnoldusd"
)


IF NOT EXIST "%BTOA_DIR%\arnoldusd\arnoldsdk" (
    echo Downloading Arnold SDK...
    curl -L https://downloads.arnoldforblender.com/%ARNOLD_VERSION%/Arnold-%ARNOLD_VERSION%-windows.zip -o "%BTOA_DIR%\arnoldusd\arnoldsdk.zip"
    
    REM Check if the zip file was downloaded successfully (size > 0)
    IF NOT EXIST "%BTOA_DIR%\arnoldusd\arnoldsdk.zip" (
        echo Download failed. The file does not exist.
        exit /b 1
    )

    REM Check if the file size is greater than 0
    for %%F in ("%BTOA_DIR%\arnoldusd\arnoldsdk.zip") do set filesize=%%~zF
    IF !filesize! EQU 0 (
        echo The downloaded file is empty or corrupted.
        exit /b 1
    )

    REM Try to unzip the file using 7zip (if installed)
    REM This assumes 7z.exe is in your PATH, or you can specify the full path to 7z.exe
    echo Extracting Arnold SDK...
    "C:\Program Files\7-Zip\7z.exe" x "%BTOA_DIR%\arnoldusd\arnoldsdk.zip" -o"%BTOA_DIR%\arnoldusd\arnoldsdk" -y

    REM If 7zip isn't available, fall back to PowerShell extraction
    IF NOT EXIST "%BTOA_DIR%\arnoldusd\arnoldsdk" (
        echo 7zip extraction failed, trying PowerShell...
        powershell -Command "Expand-Archive -Path '%BTOA_DIR%\arnoldusd\arnoldsdk.zip' -DestinationPath '%BTOA_DIR%\arnoldusd\arnoldsdk'"
    )
)

mkdir "%BTOA_DIR%\source\build"
cd "%BTOA_DIR%\source\build"

cmake .. ^
    -G "Visual Studio 17 2022" ^
    -DCMAKE_CXX_STANDARD=14 ^
    -DCMAKE_INSTALL_PREFIX="%BTOA_DIR%\arnoldusd" ^
    -DCMAKE_PREFIX_PATH="%BTOA_DIR%\dependencies" ^
    -DARNOLD_LOCATION="%BTOA_DIR%\arnoldusd\arnoldsdk" ^
    -DUSD_LOCATION="%BTOA_DIR%\dependencies\usd" ^
    -DPython3_ROOT_DIR="%BTOA_DIR%\dependencies\python\311" ^
    -DTBB_INCLUDE_DIRS="%BTOA_DIR%\dependencies\tbb\include" ^
    -DBoost_INCLUDE_DIRS="%BTOA_DIR%\dependencies\boost\include" ^
    -DBoost_LIBRARIES="%BTOA_DIR%\dependencies\boost\lib" ^
    -DBUILD_SCHEMAS=OFF ^
    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON ^
    -DCMAKE_INSTALL_RPATH="%BTOA_DIR%\arnoldusd\arnoldsdk\bin"

cmake --build .
cmake --install . --prefix "%BTOA_DIR%\arnoldusd"

echo ArnoldUSD has been successfully built at %BTOA_DIR%!


endlocal