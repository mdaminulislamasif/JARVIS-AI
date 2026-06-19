@echo off
set BLENDER_PATH="C:\Program Files\WindowsApps\BlenderFoundation.Blender_5.1.1.0_x64__ppwjx1n5r4v9t\Blender\blender.exe"
set SCRIPT_PATH="c:\Users\PHP\Desktop\ai\jarvis_learned_files\prepare_face.py"

echo =======================================================
echo JARVIS 3D FACE AUTO-RIGGER (FIXED VERSION)
echo =======================================================
echo.
echo Running Blender in background to fix your face...
echo.

%BLENDER_PATH% --background --python %SCRIPT_PATH%

echo.
echo =======================================================
echo PROCESS COMPLETE!
echo Your Face is now Fixed (No more shaking, only talking).
echo =======================================================
pause
