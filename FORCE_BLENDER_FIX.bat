@echo off
:: JARVIS EMERGENCY BLENDER RIGGING FIX
:: This script will bypass the "Access Denied" error by running as Admin.

echo ============================================================
echo   JARVIS 3D FACE: EMERGENCY BLENDER RIGGING
echo ============================================================

set BLENDER_PATH="C:\Program Files\WindowsApps\BlenderFoundation.Blender_5.1.1.0_x64__ppwjx1n5r4v9t\Blender\blender.exe"
set SCRIPT_PATH="c:\Users\PHP\Desktop\ai\jarvis_learned_files\prepare_face.py"

echo [*] Requesting Administrator Privileges...
powershell -Command "Start-Process cmd -ArgumentList '/c %BLENDER_PATH% --background --python %SCRIPT_PATH% && pause' -Verb RunAs"

echo.
echo [!] A new window should have opened asking for Admin permission.
echo [!] Please click YES in that window to finish the 3D Face Rigging.
echo ============================================================
pause
