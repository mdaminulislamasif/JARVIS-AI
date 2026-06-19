@echo off
color 0A
cls
echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║         JARVIS ADB SOUND CARD BRIDGE                     ║
echo  ║   PC Mic ←→ Phone — দুদিক একসাথে!                       ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.

set "ADB=C:\Users\asifg\OneDrive\Desktop\ai\platform-tools\adb.exe"
set "SERIAL=BD354558452086043"
set PATH=C:\Users\asifg\OneDrive\Desktop\ai\platform-tools;%PATH%

echo  [1/3] Checking phone connection...
"%ADB%" -s %SERIAL% get-state >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Phone not connected! Connect your phone via USB.
    pause
    exit /b 1
)
echo  [OK] Phone connected!
echo.

echo  [2/3] Granting permissions...
"%ADB%" -s %SERIAL% shell pm grant com.genymobile.scrcpy android.permission.RECORD_AUDIO 2>nul
"%ADB%" -s %SERIAL% shell pm grant com.genymobile.scrcpy android.permission.MODIFY_AUDIO_SETTINGS 2>nul
echo  [OK] Permissions granted.
echo.

echo  [3/3] Launching JARVIS Sound Card Bridge GUI...
echo.
echo  ┌─────────────────────────────────────────────────────────┐
echo  │  PC Mic → Phone  :  PC-তে কথা বললে Phone-এ শোনা যাবে  │
echo  │  Phone Mic → PC  :  Phone-এ কথা বললে PC-তে শোনা যাবে  │
echo  └─────────────────────────────────────────────────────────┘
echo.

python "C:\Users\asifg\OneDrive\Desktop\ai\JARVIS_SOUND_CARD.py"

echo.
pause
