@echo off
:: This script repairs Windows system files and resolves SFC scannow errors.
:: You MUST run this script as an Administrator (Right-click -> Run as administrator).

echo Checking administrator privileges...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Administrator privileges confirmed.
) else (
    echo [ERROR] You must run this script as an administrator!
    echo Please right-click this file and select "Run as administrator".
    pause
    exit /b
)

echo.
echo ===================================================
echo 1. Configuring and starting Windows Modules Installer...
echo ===================================================
sc config trustedinstaller start=auto
net start trustedinstaller
echo.

echo ===================================================
echo 2. Running DISM (Repairing Windows System Image)...
echo ===================================================
echo This may take 10-20 minutes. Please be patient.
dism /online /cleanup-image /restorehealth
echo.

echo ===================================================
echo 3. Running SFC (Restoring Missing/Corrupted Files)...
echo ===================================================
sfc /scannow
echo.

echo ===================================================
echo Windows repairs completed!
echo ===================================================
echo It is recommended to restart your computer now.
pause
