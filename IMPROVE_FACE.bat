@echo off
set BLENDER_EXE="C:\Program Files\WindowsApps\BlenderFoundation.Blender_5.1.1.0_x64__ppwjx1n5r4v9t\Blender\blender.exe"
set SCRIPT_PY="c:\Users\PHP\Desktop\ai\jarvis_learned_files\improve_face_blender.py"
set LOG_FILE="c:\Users\PHP\Desktop\ai\blender_improve.log"

echo [*] INITIATING BLENDER NEURAL RIGGING...
echo [*] Path: %BLENDER_EXE%
echo [*] Script: %SCRIPT_PY%

%BLENDER_EXE% --background --python %SCRIPT_PY% > %LOG_FILE% 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] JARVIS FACE IMPROVED SUCCESSFULLY!
    echo [INFO] Check: c:\Users\PHP\Desktop\ai\jarvis_face_pro.glb
) else (
    echo [ERROR] BLENDER OPERATION FAILED!
    echo [INFO] Check log for details: %LOG_FILE%
)
pause
