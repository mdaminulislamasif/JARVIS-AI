@echo off
title Rebuilding JARVIS with Icon
echo ================================================================================
echo   REBUILDING JARVIS WITH ICON
echo   আইকন সহ JARVIS পুনর্নির্মাণ করা হচ্ছে
echo ================================================================================
echo.

echo [1/2] Rebuilding JARVIS Installer with icon...
pyinstaller --clean --noconfirm jarvis_installer.spec
if errorlevel 1 (
    echo   ❌ Installer build failed
    pause
    exit /b 1
)
echo   ✅ Installer built with icon
echo.

echo [2/2] Copying to Desktop...
if exist "dist\JARVIS_Installer.exe" (
    copy /Y "dist\JARVIS_Installer.exe" "C:\Users\PHP\Desktop\JARVIS_Installer.exe"
    echo   ✅ Copied to Desktop
) else (
    echo   ❌ Installer not found
)
echo.

echo ================================================================================
echo   ✅ DONE!
echo ================================================================================
echo.
echo   New installer with icon: C:\Users\PHP\Desktop\JARVIS_Installer.exe
echo   আইকন সহ নতুন ইনস্টলার: C:\Users\PHP\Desktop\JARVIS_Installer.exe
echo.
pause
