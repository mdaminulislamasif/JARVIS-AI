@echo off
echo ========================================
echo JARVIS Face Auto Creator
echo ========================================
echo.
echo This will automatically:
echo 1. Open Blender
echo 2. Run the face creation script
echo 3. Create JARVIS face with skin and lip sync
echo 4. Export as GLB file
echo.
echo Please wait 1-2 minutes...
echo.

REM Find Blender installation
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
    pause
    exit /b 1
)

echo Found Blender: %BLENDER_PATH%
echo.

REM Check if script exists
if not exist "CREATE_JARVIS_FACE_WITH_SKIN.py" (
    echo ERROR: CREATE_JARVIS_FACE_WITH_SKIN.py not found!
    echo.
    echo Please make sure the script is in the same folder as this batch file.
    echo.
    pause
    exit /b 1
)

echo Starting Blender...
echo Creating JARVIS face...
echo.

REM Run Blender with the script
%BLENDER_PATH% --python CREATE_JARVIS_FACE_WITH_SKIN.py

echo.
echo ========================================
echo DONE!
echo ========================================
echo.
echo Blender should now be open with your JARVIS face!
echo.
echo Next steps:
echo 1. Review the face in Blender
echo 2. Test shape keys (Object Data Properties)
echo 3. Export: File -^> Export -^> glTF 2.0 (.glb)
echo 4. Save as: jarvis_face.glb
echo 5. Copy to JARVIS directory
echo.
pause
