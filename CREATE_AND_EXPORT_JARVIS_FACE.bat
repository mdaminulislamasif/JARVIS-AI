@echo off
echo ========================================
echo JARVIS Face Complete Auto Creator
echo ========================================
echo.
echo This will AUTOMATICALLY:
echo   1. Create JARVIS face in Blender
echo   2. Add skin material with cyan glow
echo   3. Add lip sync shape keys
echo   4. Add rigging (bones)
echo   5. Export as jarvis_face.glb
echo   6. Copy to JARVIS directory
echo.
echo NO MANUAL WORK NEEDED!
echo Just wait 1-2 minutes...
echo.
pause
echo.

REM Find Blender
set BLENDER_PATH="C:\Program Files\Blender Foundation\Blender 4.0\blender.exe"
if not exist %BLENDER_PATH% (
    set BLENDER_PATH="C:\Program Files\Blender Foundation\Blender 3.6\blender.exe"
)
if not exist %BLENDER_PATH% (
    set BLENDER_PATH="C:\Program Files\Blender Foundation\Blender\blender.exe"
)

if not exist %BLENDER_PATH% (
    echo ERROR: Blender not found!
    echo Please install from: https://www.blender.org/download/
    pause
    exit /b 1
)

echo [1/4] Found Blender: %BLENDER_PATH%
echo.

REM Check script
if not exist "CREATE_JARVIS_FACE_WITH_SKIN.py" (
    echo ERROR: Script not found!
    pause
    exit /b 1
)

echo [2/4] Creating JARVIS face in Blender...
echo       (This will take 30-60 seconds)
echo.

REM Set output path
set OUTPUT_FILE=jarvis_face.glb

REM Run Blender in background with auto-export
%BLENDER_PATH% --background --python CREATE_JARVIS_FACE_WITH_SKIN.py -- --output "%OUTPUT_FILE%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Face creation failed!
    echo Check the error messages above.
    pause
    exit /b 1
)

echo.
echo [3/4] Checking output file...

if not exist "%OUTPUT_FILE%" (
    echo ERROR: GLB file not created!
    echo.
    echo Trying with Blender GUI instead...
    echo (Blender will open - please wait)
    %BLENDER_PATH% --python CREATE_JARVIS_FACE_WITH_SKIN.py
    echo.
    echo Please manually export:
    echo   File -^> Export -^> glTF 2.0 (.glb)
    echo   Save as: jarvis_face.glb
    pause
    exit /b 0
)

echo   ✓ GLB file created: %OUTPUT_FILE%
echo.

REM Get file size
for %%A in ("%OUTPUT_FILE%") do set FILE_SIZE=%%~zA
echo   File size: %FILE_SIZE% bytes
echo.

REM Copy to JARVIS directory
echo [4/4] Copying to JARVIS directory...

set JARVIS_DIR=C:\Users\PHP\Desktop\ai

if not exist "%JARVIS_DIR%" (
    echo WARNING: JARVIS directory not found: %JARVIS_DIR%
    echo.
    echo Please manually copy jarvis_face.glb to your JARVIS directory.
    echo.
) else (
    REM Backup old file
    if exist "%JARVIS_DIR%\jarvis_face.glb" (
        echo   Backing up old file...
        copy "%JARVIS_DIR%\jarvis_face.glb" "%JARVIS_DIR%\jarvis_face_old.glb" >nul
        echo   ✓ Backup created: jarvis_face_old.glb
    )
    
    REM Copy new file
    copy "%OUTPUT_FILE%" "%JARVIS_DIR%\jarvis_face.glb" >nul
    
    if %ERRORLEVEL% EQU 0 (
        echo   ✓ Copied to: %JARVIS_DIR%\jarvis_face.glb
    ) else (
        echo   ERROR: Failed to copy file!
    )
)

echo.
echo ========================================
echo SUCCESS!
echo ========================================
echo.
echo Your JARVIS face has been created with:
echo   ✓ Realistic head mesh
echo   ✓ Cybernetic skin (cyan glow)
echo   ✓ Glowing eyes
echo   ✓ Eyelids (blinking)
echo   ✓ Lip sync shape keys (7 phonemes)
echo   ✓ Full rigging (bones)
echo.
echo File location: %OUTPUT_FILE%
echo.
echo Next steps:
echo   1. Restart JARVIS
echo   2. Your new 3D face will appear!
echo   3. Face will blink and animate automatically
echo.
echo To test in Blender:
echo   - Double-click: AUTO_CREATE_JARVIS_FACE.bat
echo   - Test shape keys and animations
echo.
pause
