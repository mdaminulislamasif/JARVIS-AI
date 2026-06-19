@echo off
chcp 65001 >nul
color 0B
title JARVIS Face - Complete Auto Setup

echo.
echo ═══════════════════════════════════════════════════════════════
echo    🎭 JARVIS 3D FACE - COMPLETE AUTO SETUP 🎭
echo    সম্পূর্ণ Automatic Setup
echo ═══════════════════════════════════════════════════════════════
echo.
echo This will:
echo   1. Check if Blender is installed
echo   2. If not, download and install Blender
echo   3. Create JARVIS 3D face automatically
echo   4. Export as jarvis_face_complete.glb
echo   5. Copy to JARVIS directory
echo.
echo Total time: 5-10 minutes (depending on internet speed)
echo.
pause

echo.
echo ═══════════════════════════════════════════════════════════════
echo    [1/5] Checking Blender Installation...
echo ═══════════════════════════════════════════════════════════════
echo.

:: Check if Blender is installed
where blender >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Blender is already installed!
    goto CREATE_FACE
)

echo ✗ Blender not found
echo.
echo ═══════════════════════════════════════════════════════════════
echo    [2/5] Downloading Blender...
echo ═══════════════════════════════════════════════════════════════
echo.

:: Create temp directory
if not exist "temp_blender" mkdir temp_blender
cd temp_blender

:: Download Blender portable (Windows 64-bit)
echo Downloading Blender 4.0 (Portable)...
echo This may take 5-10 minutes depending on your internet speed...
echo.

powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://download.blender.org/release/Blender4.0/blender-4.0.2-windows-x64.zip' -OutFile 'blender.zip'}"

if not exist "blender.zip" (
    echo.
    echo ✗ Download failed!
    echo.
    echo Please download Blender manually:
    echo   1. Go to: https://www.blender.org/download/
    echo   2. Download Windows version
    echo   3. Install it
    echo   4. Run this script again
    echo.
    pause
    exit /b 1
)

echo ✓ Download complete!
echo.
echo ═══════════════════════════════════════════════════════════════
echo    [3/5] Installing Blender...
echo ═══════════════════════════════════════════════════════════════
echo.

:: Extract Blender
echo Extracting Blender...
powershell -Command "Expand-Archive -Path 'blender.zip' -DestinationPath '.' -Force"

:: Find Blender executable
for /d %%i in (blender-*) do (
    set BLENDER_DIR=%%i
    goto FOUND_BLENDER
)

:FOUND_BLENDER
if not defined BLENDER_DIR (
    echo ✗ Extraction failed!
    pause
    exit /b 1
)

echo ✓ Blender installed!
cd ..

:: Set Blender path
set BLENDER_PATH=%CD%\temp_blender\%BLENDER_DIR%\blender.exe

:CREATE_FACE
echo.
echo ═══════════════════════════════════════════════════════════════
echo    [4/5] Creating JARVIS 3D Face...
echo ═══════════════════════════════════════════════════════════════
echo.
echo This will take 1-2 minutes...
echo Please wait...
echo.

:: Use system Blender if available, otherwise use downloaded one
where blender >nul 2>&1
if %errorlevel% equ 0 (
    set BLENDER_CMD=blender
) else (
    set BLENDER_CMD=%BLENDER_PATH%
)

:: Run Blender script
"%BLENDER_CMD%" --background --python CREATE_JARVIS_FACE_WITH_SKIN.py -- --output "%CD%\jarvis_face_complete.glb"

if not exist "jarvis_face_complete.glb" (
    echo.
    echo ✗ Face creation failed!
    echo.
    echo Trying alternative method...
    echo Opening Blender GUI for manual creation...
    echo.
    
    :: Open Blender with script loaded
    "%BLENDER_CMD%" --python CREATE_JARVIS_FACE_WITH_SKIN.py
    
    echo.
    echo After Blender opens:
    echo   1. The face will be created automatically
    echo   2. Go to: File → Export → glTF 2.0 (.glb)
    echo   3. Save as: jarvis_face_complete.glb
    echo   4. Close Blender
    echo   5. Run this script again
    echo.
    pause
    exit /b 0
)

echo ✓ JARVIS face created successfully!
echo.
echo ═══════════════════════════════════════════════════════════════
echo    [5/5] Copying to JARVIS Directory...
echo ═══════════════════════════════════════════════════════════════
echo.

:: Find JARVIS directory
if exist "jarvis" (
    copy /Y "jarvis_face_complete.glb" "jarvis\jarvis_face.glb"
    echo ✓ Copied to jarvis\jarvis_face.glb
)

if exist "JARVIS" (
    copy /Y "jarvis_face_complete.glb" "JARVIS\jarvis_face.glb"
    echo ✓ Copied to JARVIS\jarvis_face.glb
)

if exist "engine" (
    copy /Y "jarvis_face_complete.glb" "engine\jarvis_face.glb"
    echo ✓ Copied to engine\jarvis_face.glb
)

if exist "static" (
    copy /Y "jarvis_face_complete.glb" "static\jarvis_face.glb"
    echo ✓ Copied to static\jarvis_face.glb
)

if exist "assets" (
    copy /Y "jarvis_face_complete.glb" "assets\jarvis_face.glb"
    echo ✓ Copied to assets\jarvis_face.glb
)

echo.
echo ✓ File also saved in current directory: jarvis_face_complete.glb
echo.
echo ═══════════════════════════════════════════════════════════════
echo    ✅ SUCCESS - সম্পন্ন হয়েছে! ✅
echo ═══════════════════════════════════════════════════════════════
echo.
echo Your JARVIS 3D face is ready with:
echo   ✓ Realistic head mesh with facial features
echo   ✓ Cybernetic skin material (cyan glow)
echo   ✓ Glowing eyes
echo   ✓ Eyelids for blinking
echo   ✓ Mouth for talking
echo   ✓ 7 Lip sync shape keys (কথা বলার ভঙ্গি):
echo     • A_Open - Open mouth (আ)
echo     • E_Smile - Smile (ই)
echo     • O_Round - Round mouth (ও)
echo     • U_Pucker - Pucker lips (উ)
echo     • M_Closed - Closed lips (ম)
echo     • F_Teeth - Teeth on lip (ফ)
echo     • S_Teeth - Teeth smile (স)
echo   ✓ Full armature rigging (bones)
echo   ✓ Professional lighting
echo.
echo File location: jarvis_face_complete.glb
echo.
echo You can now use this in your JARVIS application!
echo.
echo ═══════════════════════════════════════════════════════════════
pause
