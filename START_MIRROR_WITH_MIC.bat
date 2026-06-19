@echo off
echo ================================================================
echo    JARVIS - Android Mirror with Microphone Forwarding
echo ================================================================
echo.
echo This script will mirror your phone screen and forward the phone's
echo MICROPHONE audio to your PC speakers.
echo.
echo (Ensure your Symphony ATOM 5 is connected via USB and ADB is authorized)
echo ================================================================
echo.

cd /d "%~dp0"
set SCRCPY_EXE=scrcpy\scrcpy-win64-v2.4\scrcpy.exe

if exist "%SCRCPY_EXE%" (
    echo Launching scrcpy with phone microphone forwarded to PC...
    "%SCRCPY_EXE%" --always-on-top --audio-source=mic
) else (
    echo Error: scrcpy.exe not found at %SCRCPY_EXE%
    echo Please make sure scrcpy is downloaded and extracted.
)

pause
