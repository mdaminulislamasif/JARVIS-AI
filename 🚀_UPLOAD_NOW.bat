@echo off
chcp 65001 >nul
color 0A
echo.
echo ════════════════════════════════════════════════════════════════════
echo    🚀 JARVIS AI - GitHub Upload (One-Click)
echo ════════════════════════════════════════════════════════════════════
echo.
echo    আপনার JARVIS AI project GitHub এ upload হচ্ছে...
echo.
echo ════════════════════════════════════════════════════════════════════
echo.
timeout /t 2 >nul

REM Step 1: Check Personal Data
echo [1/5] 🔍 Checking for personal data...
echo.
python CHECK_PERSONAL_DATA.py
if errorlevel 1 (
    echo.
    echo ❌ Personal data check failed!
    echo Please fix issues and try again.
    pause
    exit /b 1
)

echo.
echo ════════════════════════════════════════════════════════════════════
echo.

REM Step 2: Open GitHub
echo [2/5] 🌐 Opening GitHub in browser...
echo.
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
echo   5. Click: "Create repository" button
echo.
echo ════════════════════════════════════════════════════════════════════
echo.
pause

echo.
echo ════════════════════════════════════════════════════════════════════
echo.

REM Step 3: Get Repository URL
echo [3/5] 📋 Repository URL...
echo.
echo Repository create করার পর URL copy করুন
echo Example: https://github.com/YOUR_USERNAME/jarvis-ai.git
echo.
set /p REPO_URL="Paste Repository URL here: "

if "%REPO_URL%"=="" (
    echo.
    echo ❌ No URL provided!
    pause
    exit /b 1
)

echo.
echo ✅ URL received: %REPO_URL%
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

REM Step 4: Git Setup
echo [4/5] ⚙️ Setting up Git...
echo.

REM Configure Git
git config --global user.email "asifgk.hacer@gmail.com"
git config --global user.name "JARVIS AI Team"

REM Initialize if needed
if not exist ".git" (
    git init
    echo ✅ Git initialized
) else (
    echo ℹ️ Git already initialized
)

REM Add files
git add .
echo ✅ Files staged

REM Create commit
git commit -m "Initial commit: JARVIS AI System

Complete AI Assistant with:
- Voice control (pyttsx3)
- 3D face visualization  
- Antigravity control panel
- Autonomous learning
- Python GUI applications
- Comprehensive documentation

Version: 1.5.0
License: MIT
Status: Production Ready
Email: asifgk.hacer@gmail.com"

echo ✅ Commit created
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

REM Step 5: Upload
echo [5/5] 📤 Uploading to GitHub...
echo.

REM Add remote
git remote remove origin 2>nul
git remote add origin %REPO_URL%

REM Push
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ Upload failed!
    echo.
    echo Possible reasons:
    echo   • Wrong repository URL
    echo   • Authentication required
    echo   • Network issue
    echo.
    echo Please check and try again.
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
echo ════════════════════════════════════════════════════════════════════
echo    🌟 Next Steps
echo ════════════════════════════════════════════════════════════════════
echo.
echo 1. ✅ Visit your repository
echo 2. ✅ Add topics (ai, jarvis, voice-control, python)
echo 3. ✅ Enable issues
echo 4. ✅ Share with community
echo 5. ✅ Star your own repository
echo.
echo Opening your repository...
echo.

REM Open repository
for /f "tokens=1 delims=." %%a in ("%REPO_URL%") do set REPO_WEB=%%a
set REPO_WEB=%REPO_URL:.git=%
start %REPO_WEB%

timeout /t 3 >nul

echo.
echo ════════════════════════════════════════════════════════════════════
echo    🎊 SUCCESS!
echo ════════════════════════════════════════════════════════════════════
echo.
echo Your JARVIS AI project is live on GitHub!
echo.
echo Share it: %REPO_WEB%
echo.
echo ════════════════════════════════════════════════════════════════════
echo.
pause
