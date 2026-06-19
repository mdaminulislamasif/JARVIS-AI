@echo off
chcp 65001 >nul
color 0B
title JARVIS 3D Face Creator - Browser Version

echo.
echo ═══════════════════════════════════════════════════════════════
echo    🎭 JARVIS 3D FACE CREATOR - BROWSER VERSION 🎭
echo ═══════════════════════════════════════════════════════════════
echo.
echo This will open JARVIS 3D Face Creator in your browser!
echo.
echo Features:
echo   ✓ No Blender installation needed
echo   ✓ Works in any modern browser
echo   ✓ Interactive 3D view
echo   ✓ Lip sync animations (কথা বলার ভঙ্গি)
echo   ✓ Export to GLB format
echo   ✓ Real-time controls
echo.
echo Controls in browser:
echo   • Mouse drag - Rotate view
echo   • Mouse wheel - Zoom in/out
echo   • Click buttons - Test animations
echo   • Export GLB - Save 3D model
echo.
pause

echo.
echo Opening in browser using local Python server...
echo.

:: Launch via Python script
python jarvis_face_threejs_python.py

echo.
echo ✓ Application closed!
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
pause
