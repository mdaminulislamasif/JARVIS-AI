@echo off
title System Clean and Bot Launcher

:: --- Cleanup Section ---
echo Cleaning temporary files...

:: Clean Windows Temp
del /s /f /q "C:\Windows\Temp\*.*" >nul 2>&1
rd /s /q "C:\Windows\Temp" >nul 2>&1
md "C:\Windows\Temp"

:: Clean Prefetch
del /s /f /q "C:\Windows\Prefetch\*.*" >nul 2>&1

:: Clean User Temp
del /s /f /q "%temp%\*.*" >nul 2>&1
rd /s /q "%temp%" >nul 2>&1
md "%temp%"

:: Clean History, Cookies, and Recent
rd /s /q "C:\Windows\History" >nul 2>&1
rd /s /q "C:\Windows\Cookies" >nul 2>&1
rd /s /q "C:\Windows\Recent" >nul 2>&1
rd /s /q "C:\Windows\Spool\Printers" >nul 2>&1

:: --- Bot Launch Section ---
cls
echo Launching Bots...
cd /d "%~dp0"

start "Bot Main" python "login_bot.py"
start "Bot 1" python "login_bot - 1.py"
start "Bot 2" python "login_bot - 2.py"
start "Bot 3" python "login_bot - 3.py"
start "Bot 4" python "login_bot - 4.py"

echo All processes started. Exiting...
timeout /t 3 >nul
exit
