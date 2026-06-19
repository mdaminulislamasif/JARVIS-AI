@echo off
echo [*] STARTING ANTIGRAVITY LOCAL SERVER...
echo [*] PORT: 8000
echo [*] URL: http://localhost:8000/antigravity_panel.html

cd /d "%~dp0"

:: Start Python's built-in web server in the background
start /b python -m http.server 8000

:: Wait for a second to ensure server is up
timeout /t 2 >nul

:: Open the panel in the default browser
start http://localhost:8000/antigravity_panel.html

echo [SUCCESS] JARVIS PANEL IS NOW LIVE!
echo [INFO] Close this window when you are done.
pause
