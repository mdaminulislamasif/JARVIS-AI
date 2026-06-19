@echo off
chcp 65001 >nul
title JARVIS Infinity Brain - জার্ভিস ইনফিনিটি ব্রেইন

echo.
echo ================================================================================
echo   ♾️  JARVIS INFINITY BRAIN
echo   ♾️  জার্ভিস ইনফিনিটি ব্রেইন
echo ================================================================================
echo.
echo   Unlimited Knowledge Through Internet!
echo   ইন্টারনেটের মাধ্যমে সীমাহীন জ্ঞান!
echo.
echo ================================================================================
echo.
echo   Choose Mode:
echo   মোড নির্বাচন করুন:
echo.
echo   1. Demo Mode (Learn 5 sample topics)
echo      ডেমো মোড (৫টি নমুনা বিষয় শিখুন)
echo.
echo   2. Interactive Mode (Ask anything!)
echo      ইন্টারঅ্যাক্টিভ মোড (যেকোনো কিছু জিজ্ঞাসা করুন!)
echo.
echo   3. Exit
echo      বের হন
echo.
echo ================================================================================
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Starting Demo Mode...
    echo ডেমো মোড শুরু হচ্ছে...
    echo.
    python jarvis_infinity_brain.py --demo
) else if "%choice%"=="2" (
    echo.
    echo Starting Interactive Mode...
    echo ইন্টারঅ্যাক্টিভ মোড শুরু হচ্ছে...
    echo.
    python jarvis_infinity_brain.py --interactive
) else (
    echo.
    echo Exiting...
    echo বের হচ্ছে...
    timeout /t 2 >nul
    exit
)

echo.
echo ================================================================================
echo   Press any key to exit... (বন্ধ করতে যেকোনো কী চাপুন...)
echo ================================================================================
pause >nul
