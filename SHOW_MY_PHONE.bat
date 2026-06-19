@echo off
color 0A
cls
echo.
echo  ========================================================
echo    JARVIS ^| Symphony ATOM 5 ^| Screen Mirror
echo  ========================================================
echo.
echo   Connecting to your phone...
echo.

:: Set paths
set "ADB=C:\Users\asifg\OneDrive\Desktop\ai\platform-tools\adb.exe"
set "SCRCPY=C:\Users\asifg\OneDrive\Desktop\ai\scrcpy\scrcpy-win64-v2.4\scrcpy.exe"
set PATH=C:\Users\asifg\OneDrive\Desktop\ai\platform-tools;%PATH%

:: Check device
echo [1/3] Checking ADB device...
"%ADB%" devices
echo.

:: Kill old ADB if stuck
"%ADB%" kill-server >nul 2>&1
timeout /t 1 /nobreak >nul
"%ADB%" start-server >nul 2>&1
timeout /t 1 /nobreak >nul

:: Confirm device
echo [2/3] Device status:
"%ADB%" -s BD354558452086043 get-state
echo.

:: Launch mirror
echo [3/3] Launching phone screen on your PC...
echo.
echo  *** Your ATOM 5 screen will appear as a window ***
echo  *** You can control your phone from PC! ***
echo.
echo  Controls:
echo  - Mouse click = Phone tap
echo  - Scroll = Phone scroll
echo  - Keyboard = Phone keyboard input
echo  - Ctrl+H = Home button
echo  - Ctrl+B = Back button
echo.

"%SCRCPY%" -s BD354558452086043 --always-on-top --window-title "ATOM 5 - JARVIS Mirror" --max-size 1024 --video-bit-rate 8M

echo.
echo Mirror session ended.
pause
