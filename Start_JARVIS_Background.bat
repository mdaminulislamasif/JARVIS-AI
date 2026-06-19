@echo off
echo.
echo ================================================================================
echo   🤖 JARVIS BACKGROUND LEARNER - ব্যাকগ্রাউন্ড লার্নার
echo ================================================================================
echo.
echo   Checking dependencies...
echo   ডিপেন্ডেন্সি চেক করছি...
echo.

REM Check if dependencies are installed
python -c "import win32gui, psutil, keyboard, pyperclip" 2>nul
if errorlevel 1 (
    echo   ❌ Missing dependencies! Installing...
    echo   ❌ ডিপেন্ডেন্সি নেই! ইনস্টল করছি...
    echo.
    pip install -r requirements_background.txt
    echo.
    echo   ✅ Dependencies installed!
    echo   ✅ ডিপেন্ডেন্সি ইনস্টল হয়েছে!
    echo.
)

echo   ✅ All dependencies ready!
echo   ✅ সব ডিপেন্ডেন্সি প্রস্তুত!
echo.
echo ================================================================================
echo   🚀 Starting JARVIS Background Learner...
echo   🚀 জার্ভিস ব্যাকগ্রাউন্ড লার্নার শুরু হচ্ছে...
echo ================================================================================
echo.
echo   Hotkeys (হটকি):
echo   • Ctrl+Q : Stop JARVIS (বন্ধ করুন)
echo   • Ctrl+S : Show Statistics (পরিসংখ্যান দেখুন)
echo   • Ctrl+L : Show What Learned (কি শিখেছে দেখুন)
echo.
echo ================================================================================
echo.

python jarvis_background_learner.py

pause
