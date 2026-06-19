@echo off
REM Open Blender and run the JARVIS face fix script
SET SCRIPT_PATH=%~dp0BLENDER_FIX_ALL_FACE_PROBLEMS.py
SET BLENDER_EXE="C:\Program Files\Blender Foundation\Blender\blender.exe"
IF NOT EXIST %BLENDER_EXE% (
  IF DEFINED ProgramFiles(x86) IF EXIST "%ProgramFiles(x86)%\Blender Foundation\Blender\blender.exe" (
    SET BLENDER_EXE="%ProgramFiles(x86)%\Blender Foundation\Blender\blender.exe"
  ) ELSE (
    echo Blender executable not found at %BLENDER_EXE%
    echo Please install Blender or update OPEN_BLENDER_FACE_FIX.bat with the correct path.
    pause
    exit /b 1
  )
)
start "JARVIS Blender Face Fix" %BLENDER_EXE% --python "%SCRIPT_PATH%"
exit /b 0
