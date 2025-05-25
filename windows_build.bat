@echo off
setlocal enabledelayedexpansion

:: Define variables
set SCRIPT_DIR=%~dp0
set SOURCE_DIR=%SCRIPT_DIR%\source
set BUILD_DIR=%SCRIPT_DIR%\build
set INSTALL_DIR=%SCRIPT_DIR%\arnoldusd
set BLENDER_DIR=%SCRIPT_DIR%\build-deps
set ARNOLD_DIR=%SCRIPT_DIR%\arnoldsdk
set BLENDER_VERSION=4.4
set ARNOLD_VERSION=7.4.2.0

git clone https://github.com/Autodesk/arnold-usd.git %SOURCE_DIR%
cd %SOURCE_DIR%
git checkout Arnold-%ARNOLD_VERSION%

cd %SCRIPT_DIR%
git clone https://projects.blender.org/blender/lib-windows_x64.git %BLENDER_DIR%

cd %BLENDER_DIR%
git checkout blender-v%BLENDER_VERSION%-release

cd %SCRIPT_DIR%
IF NOT EXIST "%ARNOLD_DIR%" (
    echo Downloading Arnold SDK...
    curl -L https://github.com/cjhosken/btoa/releases/download/arnoldsdk-%ARNOLD_VERSION%/Arnold-%ARNOLD_VERSION%-windows.zip -o "%SCRIPT_DIR%\arnoldsdk.zip"
    
    REM Check if the zip file was downloaded successfully (size > 0)
    IF NOT EXIST "%SCRIPT_DIR%\arnoldsdk.zip" (
        echo Download failed. The file does not exist.
        exit /b 1
    )

    REM Check if the file size is greater than 0
    for %%F in ("%SCRIPT_DIR%\arnoldsdk.zip") do set filesize=%%~zF
    IF !filesize! EQU 0 (
        echo The downloaded file is empty or corrupted.
        exit /b 1
    )

    REM Try to unzip the file using 7zip (if installed)
    REM This assumes 7z.exe is in your PATH, or you can specify the full path to 7z.exe
    echo Extracting Arnold SDK...
    "C:\Program Files\7-Zip\7z.exe" x "%SCRIPT_DIR%\arnoldsdk.zip" -o"%ARNOLD_DIR%" -y

    REM If 7zip isn't available, fall back to PowerShell extraction
    IF NOT EXIST "%ARNOLD_DIR%" (
        echo 7zip extraction failed, trying PowerShell...
        powershell -Command "Expand-Archive -Path '%SCRIPT_DIR%\arnoldsdk.zip' -DestinationPath '%ARNOLD_DIR%'"
    )
)

mkdir "%BUILD_DIR%"
cd "%BUILD_DIR%"

cmake %SOURCE_DIR% ^
    -G "Visual Studio 17 2022" ^
    -DCMAKE_BUILD_TYPE=Release ^
    -DCMAKE_CXX_STANDARD=17 ^
    -DBUILD_UNIT_TESTS=OFF ^
    -DBUILD_TESTSUITE=OFF ^
    -DCMAKE_INSTALL_PREFIX="%INSTALL_DIR%" ^
    -DCMAKE_PREFIX_PATH="%SCRIPT_DIR%\build-deps" ^
    -DARNOLD_LOCATION="%ARNOLD_DIR%" ^
    -DUSD_LOCATION="%SCRIPT_DIR%\build-deps\usd" ^
    -DPython3_ROOT="%SCRIPT_DIR%\build-deps\python\311" ^
    -DPython3_EXECUTABLE="%SCRIPT_DIR%\build-deps\python\311\bin\python.exe" ^
    -DTBB_INCLUDE_DIRS="%SCRIPT_DIR%\build-deps\tbb\include" ^
    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON ^
    -DBUILD_SCHEMAS=ON ^
    -DBUILD_USDGENSCHEMA_ARNOLD=ON ^
    -DCMAKE_INSTALL_RPATH="%ARNOLD_DIR%\bin"

cmake --build .
cmake --install . --prefix "%INSTALL_DIR%"

echo ArnoldUSD has been successfully built at %INSTALL_DIR%!
endlocal