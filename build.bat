@echo off
setlocal enabledelayedexpansion

::::::::::::::::::::::::::::::::::::::::
:: CONFIGURABLE PARAMETERS
::::::::::::::::::::::::::::::::::::::::

:: Defaults if params not passed
set "BLENDER_VERSION=%~1"
if "%BLENDER_VERSION%"=="" set "BLENDER_VERSION=5.0"

set "ARNOLD_VERSION=%~2"
if "%ARNOLD_VERSION%"=="" set "ARNOLD_VERSION=7.4.4.0"

:: Paths
set "SCRIPT_DIR=%~dp0"
echo %SCRIPT_DIR%

set "ARNOLD_ROOT=%SCRIPT_DIR%"
set "BLENDER_LIB_REPO=https://projects.blender.org/blender/lib-windows_x64.git"
set "ARNOLD_USD_REPO=https://github.com/Autodesk/arnold-usd.git"
set "ARNOLD_SDK_URL=https://github.com/cjhosken/btoa/releases/download/arnoldsdk/Arnold-%ARNOLD_VERSION%-windows.zip"

set "INSTALL_ROOT=%USERPROFILE%\.btoa\btoa-%BLENDER_VERSION%-%ARNOLD_VERSION%"

::::::::::::::::::::::::::::::::::::::::
:: DIRECTORY SETUP
::::::::::::::::::::::::::::::::::::::::

echo ==^> Creating directory tree…
if not exist "%ARNOLD_ROOT%\source" mkdir "%ARNOLD_ROOT%\source"
if not exist "%ARNOLD_ROOT%\build" mkdir "%ARNOLD_ROOT%\build"

::::::::::::::::::::::::::::::::::::::::
:: FETCH SOURCES
::::::::::::::::::::::::::::::::::::::::

echo.
echo ==^> Cloning Arnold USD…
if not exist "%ARNOLD_ROOT%\source\arnoldusd" (
    git clone --depth 1 -b Arnold-%ARNOLD_VERSION% "%ARNOLD_USD_REPO%" "%ARNOLD_ROOT%\source\arnoldusd"
) else (
    echo Arnold USD already exists, skipping clone.
)

echo.
echo ==^> Cloning Blender libraries…
if not exist "%ARNOLD_ROOT%\source\blender" (
    git clone --depth 1 -b blender-v%BLENDER_VERSION%-release "%BLENDER_LIB_REPO%" "%ARNOLD_ROOT%\source\blender"
) else (
    echo Blender libraries already exist, skipping clone.
)

echo.
echo ==^> Downloading Arnold SDK %ARNOLD_VERSION%…
if exist "%ARNOLD_ROOT%\source\arnoldsdk.zip" del "%ARNOLD_ROOT%\source\arnoldsdk.zip"
curl -L "%ARNOLD_SDK_URL%" -o "%ARNOLD_ROOT%\source\arnoldsdk.zip"

echo ==^> Unpacking Arnold SDK…
if not exist "%ARNOLD_ROOT%\source\arnoldsdk" mkdir "%ARNOLD_ROOT%\source\arnoldsdk"

:: Use tar from Windows 10+ or Git
tar -xf "%ARNOLD_ROOT%\source\arnoldsdk.zip" -C "%ARNOLD_ROOT%\source\arnoldsdk"
del "%ARNOLD_ROOT%\source\arnoldsdk.zip"

::::::::::::::::::::::::::::::::::::::::
:: QUICK FIXES
::::::::::::::::::::::::::::::::::::::::

echo ==^> Copying TBB quickfix…
copy "%ARNOLD_ROOT%\source\blender\tbb\include\tbb\version.h" "%ARNOLD_ROOT%\source\blender\tbb\include\tbb\tbb_stddef.h" >nul

::::::::::::::::::::::::::::::::::::::::
:: CONFIGURE & BUILD
::::::::::::::::::::::::::::::::::::::::

echo.
echo ==^> Running CMake…
cd /d "%ARNOLD_ROOT%\build"

cmake "%ARNOLD_ROOT%\source\arnoldusd" ^
    -DCMAKE_INSTALL_PREFIX="%INSTALL_ROOT%" ^
    -DARNOLD_LOCATION="%ARNOLD_ROOT%\source\arnoldsdk" ^
    -DUSD_INCLUDE_DIR="%ARNOLD_ROOT%\source\blender\usd\include" ^
    -DUSD_LIBRARY_DIR="%ARNOLD_ROOT%\source\blender\usd\lib" ^
    -DUSD_BINARY_DIR="%ARNOLD_ROOT%\source\blender\usd\bin" ^
    -DPython3_ROOT="%ARNOLD_ROOT%\source\blender\python" ^
    -DTBB_ROOT_DIR="%ARNOLD_ROOT%\source\blender\tbb" ^
    -DCMAKE_BUILD_TYPE=Release ^
    -DUSD_MONOLITHIC_BUILD=True ^
    -DBUILD_USDGENSCHEMA_ARNOLD=OFF ^
    -DBUILD_PROCEDURAL=OFF ^
    -DBUILD_DOCS=OFF ^
    -DBUILD_TESTSUITE=OFF ^
    -DBUILD_SCHEMAS=OFF

echo.
echo ==^> Building Arnold USD…
cmake --build . --config Release --target install

echo.
echo ==^> Copying Arnold SDK into install root…
robocopy "%ARNOLD_ROOT%\source\arnoldsdk" "%INSTALL_ROOT%" /E >nul

echo.
echo ==^> Build finished!
