@echo off
chcp 65001 >nul
color 0A
cls
echo.
echo ════════════════════════════════════════════════════════════════════
echo    🚀 JARVIS AI - Direct GitHub Upload
echo ════════════════════════════════════════════════════════════════════
echo.
echo    আপনার JARVIS AI project GitHub এ upload হচ্ছে...
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

REM Open GitHub
echo [1/4] 🌐 Opening GitHub...
start https://github.com/new
timeout /t 3 >nul
echo ✅ Browser opened!
echo.

echo ════════════════════════════════════════════════════════════════════
echo    📝 Create Repository on GitHub
echo ════════════════════════════════════════════════════════════════════
echo.
echo Browser এ এই steps follow করুন:
echo.
echo   1. Repository name: jarvis-ai
echo   2. Description: Complete AI Assistant System
echo   3. Select: Public ✅
echo   4. DON'T check "Initialize with README" ❌
echo   5. Click: "Create repository"
echo.
pause
echo.

REM Get repository URL
echo ════════════════════════════════════════════════════════════════════
echo [2/4] 📋 Repository URL
echo ════════════════════════════════════════════════════════════════════
echo.
echo Repository create করার পর URL copy করুন
echo Example: https://github.com/YOUR_USERNAME/jarvis-ai.git
echo.
set /p REPO_URL="Paste Repository URL: "
echo.

if "%REPO_URL%"=="" (
    echo ❌ No URL provided!
    pause
    exit /b 1
)

echo ✅ URL: %REPO_URL%
echo.

REM Configure Git
echo ════════════════════════════════════════════════════════════════════
echo [3/4] ⚙️ Git Setup
echo ════════════════════════════════════════════════════════════════════
echo.

git config --global user.email "asifgk.hacer@gmail.com"
git config --global user.name "JARVIS AI Team"

if not exist ".git" (
    git init
    echo ✅ Git initialized
) else (
    echo ℹ️ Git already initialized
)

git add .
echo ✅ Files staged

git commit -m "Initial commit: JARVIS AI System - Complete AI Assistant with voice control, 3D face, autonomous learning. Version 1.5.0, MIT License"
echo ✅ Commit created
echo.

REM Upload
echo ════════════════════════════════════════════════════════════════════
echo [4/4] 📤 Uploading to GitHub
echo ════════════════════════════════════════════════════════════════════
echo.

git remote remove origin 2>nul
git remote add origin %REPO_URL%
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ Upload failed!
    echo.
    echo Possible reasons:
    echo   • Wrong URL
    echo   • Authentication needed
    echo   • Network issue
    echo.
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════════════
echo    ✅ UPLOAD COMPLETE!
echo ════════════════════════════════════════════════════════════════════
echo.
echo 🎉 Your JARVIS AI project is now on GitHub!
echo.
echo Repository: %REPO_URL%
echo.

REM Open repository
set REPO_WEB=%REPO_URL:.git=%
start %REPO_WEB%

echo.
echo Opening repository in browser...
echo.
timeout /t 3 >nul

echo ════════════════════════════════════════════════════════════════════
echo    🎊 SUCCESS!
echo ════════════════════════════════════════════════════════════════════
echo.
pause
