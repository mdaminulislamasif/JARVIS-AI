@echo off
title PC Microphone to Phone Bridge (Socket Streamer)
color 0A
cls
echo.
echo  ╔════════════════════════════════════════════════════════╗
echo  ║   PC MICROPHONE  →→→  ATOM 5 PHONE MICROPHONE          ║
echo  ║   আপনার PC-র মাইক্রোফোন = Phone-এর মাইক্রোফোন         ║
echo  ╚════════════════════════════════════════════════════════╝
echo.

set "ADB=C:\Users\asifg\OneDrive\Desktop\ai\platform-tools\adb.exe"
set "SERIAL=BD354558452086043"
set PATH=C:\Users\asifg\OneDrive\Desktop\ai\platform-tools;%PATH%
set ANDROID_SERIAL=%SERIAL%

echo  [1/4] Checking phone connection...
"%ADB%" -s %SERIAL% get-state
if %errorlevel% neq 0 (
    echo  [ERROR] Phone not connected! Connect ATOM 5 via USB.
    pause
    exit /b 1
)
echo  [OK] ATOM 5 connected!
echo.

echo  [2/4] Setting up ADB port reverse (tcp:8010)...
"%ADB%" -s %SERIAL% reverse tcp:8010 tcp:8010
if %errorlevel% neq 0 (
    echo  [WARN] ADB reverse failed. Make sure phone is connected over USB.
) else (
    echo  [OK] Port reverse active: Phone localhost:8010 is mapped to PC.
)
echo.

echo  [3/4] Instructions for phone:
echo  -------------------------------------------------------
echo    1. Open Google Chrome or VLC on your phone.
echo    2. Open this address: http://localhost:8010
echo    3. Press play to start hearing your PC mic live!
echo  -------------------------------------------------------
echo.

echo  [4/4] Starting PC Mic Streamer Server...
echo  (Streaming audio from your PC microphone over USB)
echo.
python pc_mic_streamer.py

echo.
pause
