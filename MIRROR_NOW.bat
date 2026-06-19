@echo off
title JARVIS - Phone Mirror
echo ================================================
echo  JARVIS - Symphony ATOM 5 Screen Mirror
echo ================================================
echo.
echo  Device : Symphony ATOM 5
echo  Serial : BD354558452086043  
echo  Status : Launching mirror...
echo.

set SCRCPY="%~dp0scrcpy\scrcpy-win64-v2.4\scrcpy.exe"
set ADB="%~dp0platform-tools\adb.exe"

echo Checking ADB device...
%ADB% devices

echo.
echo Starting screen mirror on PC...
echo (Your phone screen will appear as a window)
echo.

%SCRCPY% -s BD354558452086043 --always-on-top --window-title "Symphony ATOM 5 - JARVIS Mirror" --turn-screen-off

echo.
echo Mirror session ended.
pause
