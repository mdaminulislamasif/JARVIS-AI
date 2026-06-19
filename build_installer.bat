@echo off
title Building JARVIS Installer
echo ================================================================================
echo   BUILDING JARVIS ONE-CLICK INSTALLER
echo   JARVIS ওয়ান-ক্লিক ইনস্টলার তৈরি করা হচ্ছে
echo ================================================================================
echo.

echo [1/3] Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo   Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo   ❌ Failed to install PyInstaller
        pause
        exit /b 1
    )
)
echo   ✅ PyInstaller ready
echo.

echo [2/3] Building installer...
pyinstaller --clean --noconfirm jarvis_installer.spec
if errorlevel 1 (
    echo   ❌ Build failed
    pause
    exit /b 1
)
echo   ✅ Build complete
echo.

echo [3/3] Finalizing...
if exist "dist\JARVIS_Installer.exe" (
    echo   ✅ Installer created: dist\JARVIS_Installer.exe
    echo.
    echo ================================================================================
    echo   ✅ SUCCESS!
    echo ================================================================================
    echo.
    echo   Installer location: dist\JARVIS_Installer.exe
    echo   Size: 
    dir "dist\JARVIS_Installer.exe" | find "JARVIS_Installer.exe"
    echo.
    echo   You can now:
    echo   1. Copy JARVIS_Installer.exe to any Windows computer
    echo   2. Double-click to install
    echo   3. JARVIS will be installed on Desktop automatically
    echo.
    echo ================================================================================
) else (
    echo   ❌ Installer not found
)
echo.
pause
