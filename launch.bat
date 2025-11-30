@echo off
setlocal EnableDelayedExpansion

REM --- Set BTOA root ---
set "BTOA_ROOT=%USERPROFILE%\.btoa\btoa-5.0-7.4.4.0"

REM --- Resolve script directory ---
set "SCRIPT_DIR=%~dp0"
REM Remove trailing backslash
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM --- Get grandparent folder of the script ---
for %%A in ("%SCRIPT_DIR%\..") do set "GRANDPARENT_DIR=%%~fA"

REM --- Set USD plugin paths ---
set "PXR_PLUGINPATH_NAME=%BTOA_ROOT%\plugin;%BTOA_ROOT%\lib\usd"

REM --- Shared library paths ---
set "PATH=%BTOA_ROOT%\bin;%PATH%"

REM --- Python import path ---
set "PYTHONPATH=%GRANDPARENT_DIR%;%PYTHONPATH%"

REM --- Disable TF_DEBUG ---
set "TF_DEBUG="

REM --- Run Blender with BtoA ---
"W:\Workspace\blender\blender-5.0.0-windows-x64\blender.exe" ^
    --python-use-system-env ^
    --python-expr "import btoa; btoa.register()"

endlocal
