@echo off
echo [*] INITIATING JARVIS NEURAL UPLOAD...
echo [*] Folder: c:\Users\PHP\Desktop\ai

cd /d "c:\Users\PHP\Desktop\ai"

:: Check if git is initialized
if not exist .git (
    echo [!] Initializing Git...
    git init
)

:: Stage all files
echo [*] Staging all files...
git add .

:: Commit
echo [*] Committing changes...
git commit -m "Initial Neural Upload: JARVIS Antigravity v5.0"

:: Check for remote
git remote -v | findstr "origin" >nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] No GitHub repository linked!
    set /p REPO_URL="[>] Please enter your GitHub Repository URL: "
    git remote add origin %REPO_URL%
)

:: Push to GitHub
echo [*] Pushing to GitHub (Main)...
git branch -M main
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] JARVIS IS NOW ONLINE ON GITHUB!
) else (
    echo [ERROR] UPLOAD FAILED! Please check your internet or repository permissions.
)

pause
