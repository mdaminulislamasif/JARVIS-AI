@echo off
echo ========================================
echo JARVIS Face 3D Fixer
echo ========================================
echo.

REM Check if Blender is installed
set BLENDER_PATH="C:\Program Files\Blender Foundation\Blender 4.0\blender.exe"
if not exist %BLENDER_PATH% (
    set BLENDER_PATH="C:\Program Files\Blender Foundation\Blender 3.6\blender.exe"
)
if not exist %BLENDER_PATH% (
    set BLENDER_PATH="C:\Program Files\Blender Foundation\Blender\blender.exe"
)

if not exist %BLENDER_PATH% (
    echo ERROR: Blender not found!
    echo.
    echo Please install Blender from: https://www.blender.org/download/
    echo.
    echo Or update BLENDER_PATH in this batch file to point to your Blender installation.
    pause
    exit /b 1
)

echo Found Blender: %BLENDER_PATH%
echo.

REM Get input file path
set INPUT_FILE=%~1
if "%INPUT_FILE%"=="" (
    set /p INPUT_FILE="Enter path to GLB file to fix (or drag and drop): "
)

REM Remove quotes if present
set INPUT_FILE=%INPUT_FILE:"=%

REM Check if input file exists
if not exist "%INPUT_FILE%" (
    echo ERROR: Input file not found: %INPUT_FILE%
    echo.
    echo Trying default location: %USERPROFILE%\Documents\Untitled.glb
    set INPUT_FILE=%USERPROFILE%\Documents\Untitled.glb
    
    if not exist "%INPUT_FILE%" (
        echo ERROR: Default file also not found!
        pause
        exit /b 1
    )
)

echo Input file: %INPUT_FILE%
echo.

REM Set output file
set OUTPUT_FILE=jarvis_face_fixed.glb
echo Output file: %OUTPUT_FILE%
echo.

echo Starting Blender in background mode...
echo This may take 1-2 minutes...
echo.

REM Run Blender with the script
%BLENDER_PATH% --background --python FIX_JARVIS_FACE_3D.py -- "%INPUT_FILE%" "%OUTPUT_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS!
    echo ========================================
    echo.
    echo Fixed file saved to: %OUTPUT_FILE%
    echo.
    echo You can now:
    echo 1. Copy this file to your JARVIS directory
    echo 2. Rename it to jarvis_face.glb
    echo 3. Restart JARVIS to see the fixed 3D face
    echo.
) else (
    echo.
    echo ========================================
    echo FAILED!
    echo ========================================
    echo.
    echo Check the error messages above.
    echo.
)

pause
