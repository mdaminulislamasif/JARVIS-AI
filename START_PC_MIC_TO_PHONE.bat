@echo off
title PC Microphone to Phone Bridge
color 0B
cls
echo.
echo  ╔═══════════════════════════════════════════════════════╗
echo  ║     JARVIS PC MIC TO PHONE BRIDGE                         ║
echo  ║     PC Mic -> Android Phone Speakers/System Audio         ║
echo  ╚═══════════════════════════════════════════════════════╝
echo.

set PATH=C:\Users\asifg\OneDrive\Desktop\ai\platform-tools;%PATH%
set ADB=C:\Users\asifg\OneDrive\Desktop\ai\platform-tools\adb.exe

echo  [1/3] Checking phone connection...
"%ADB%" devices
echo.

echo  [2/3] Setting up ADB port reverse (tcp:8010)...
"%ADB%" reverse tcp:8010 tcp:8010
if %errorlevel% neq 0 (
    echo  [WARN] ADB reverse failed. Make sure phone is connected over USB.
) else (
    echo  [OK] Port reverse active: Phone localhost:8010 is mapped to PC.
)
echo.

echo  [3/3] Starting PC Mic Streamer Server...
echo  -------------------------------------------------------
echo  Instructions for phone:
echo    1. Open Google Chrome or VLC on your phone.
echo    2. Open this address: http://localhost:8010
echo    3. Press play to start hearing your PC mic live!
echo  -------------------------------------------------------
echo.
python pc_mic_streamer.py
echo.
pause
