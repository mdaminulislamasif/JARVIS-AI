@echo off
title JARVIS SYSTEM MONITOR
color 0A
echo ================================================================================
echo   JARVIS SYSTEM MONITOR
echo   JARVIS সিস্টেম মনিটর
echo ================================================================================
echo.
echo This will show what JARVIS is doing on your system
echo এটা দেখাবে JARVIS আপনার system এ কি করছে
echo.
echo Choose an option / একটি অপশন বেছে নিন:
echo.
echo   1. Single Snapshot (one-time check)
echo      একবার দেখুন
echo.
echo   2. Live Monitor (updates every 2 seconds)
echo      Live মনিটর (প্রতি 2 সেকেন্ডে আপডেট)
echo.
echo   3. Exit / বের হন
echo.
set /p choice="Enter your choice (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo Running single snapshot...
    echo একবার চেক করা হচ্ছে...
    echo.
    python jarvis_system_monitor.py
    echo.
    pause
) else if "%choice%"=="2" (
    echo.
    echo Starting live monitor...
    echo Live monitor চালু হচ্ছে...
    echo Press Ctrl+C to stop
    echo বন্ধ করতে Ctrl+C চাপুন
    echo.
    python jarvis_system_monitor.py live
) else (
    echo.
    echo Exiting...
    echo বের হচ্ছে...
)
