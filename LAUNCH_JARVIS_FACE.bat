@echo off
set RUN_SCRIPT="engine.face3d_run"

echo.
echo [JARVIS] STARTING 3D REACTION ENGINE...
echo.
cd /d "%~dp0"
python -m %RUN_SCRIPT%

pause
