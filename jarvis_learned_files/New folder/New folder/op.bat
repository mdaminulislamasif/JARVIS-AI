@echo off
timeout /t 30 /nobreak >nul
cd /d "%~dp0"
start "Bot Main" python "login_bot.py"
start "Bot 1" python "login_bot - 1.py"
start "Bot 2" python "login_bot - 2.py"
start "Bot 3" python "login_bot - 3.py"
start "Bot 4" python "login_bot - 4.py"
exit
