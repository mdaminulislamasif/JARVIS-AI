@echo off
echo ================================================================
echo    JARVIS - Android OTG Mode (USB HID Emulation)
echo ================================================================
echo.
echo This mode allows you to use your PC's keyboard and mouse as
echo physical input devices directly connected to your phone.
echo Use this to blindly unlock your phone and accept ADB prompts!
echo.
echo Instructions:
echo 1. Connect your phone via USB.
echo 2. Press Spacebar/Power to wake screen.
echo 3. Type your PIN/Password and press Enter to unlock.
echo 4. Press Tab and Space to check "Always allow".
echo 5. Press Tab again and Enter to click "Allow/OK".
echo.
echo ================================================================
echo.

cd /d "%~dp0"
set SCRCPY_EXE=scrcpy\scrcpy-win64-v2.4\scrcpy.exe

if exist "%SCRCPY_EXE%" (
    echo Launching scrcpy in OTG mode...
    "%SCRCPY_EXE%" --otg
) else (
    echo Error: scrcpy.exe not found at %SCRCPY_EXE%
    echo Please make sure scrcpy is downloaded and extracted.
)

pause
