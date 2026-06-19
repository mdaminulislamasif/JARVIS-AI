@echo off
cls
echo.
echo ================================================================================
echo   🔄 JARVIS AUTO-UPDATE SETUP
echo   🔄 জার্ভিস স্বয়ংক্রিয় আপডেট সেটআপ
echo ================================================================================
echo.
echo   This will setup JARVIS to update itself automatically!
echo   এটি জার্ভিসকে স্বয়ংক্রিয়ভাবে আপডেট করার জন্য সেটআপ করবে!
echo.
echo ================================================================================
echo.
echo   Options:
echo   অপশন:
echo.
echo   1. Add to Windows Startup (Windows চালু হলে চলবে)
echo   2. Run Update Now (এখনই আপডেট চালান)
echo   3. Run Continuous Updater (ক্রমাগত আপডেটার চালান)
echo   4. Remove from Startup (Startup থেকে সরান)
echo   5. Exit (বের হন)
echo.
echo ================================================================================
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto add_startup
if "%choice%"=="2" goto run_now
if "%choice%"=="3" goto run_continuous
if "%choice%"=="4" goto remove_startup
if "%choice%"=="5" goto exit
goto invalid

:add_startup
echo.
echo Adding JARVIS Auto-Updater to Windows Startup...
echo Windows Startup-এ জার্ভিস স্বয়ংক্রিয় আপডেটার যোগ করছি...
echo.

REM Get current directory
set "CURRENT_DIR=%cd%"

REM Create shortcut in Startup folder
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT=%STARTUP_FOLDER%\JARVIS_Auto_Update.lnk"

REM Create VBS script to create shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%SHORTCUT%" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%CURRENT_DIR%\JARVIS_AUTO_UPDATE_STARTUP.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "JARVIS Auto-Updater" >> CreateShortcut.vbs
echo oLink.WindowStyle = 7 >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

REM Run VBS script
cscript //nologo CreateShortcut.vbs

REM Delete VBS script
del CreateShortcut.vbs

echo.
echo ✅ JARVIS Auto-Updater added to Windows Startup!
echo ✅ জার্ভিস স্বয়ংক্রিয় আপডেটার Windows Startup-এ যোগ করা হয়েছে!
echo.
echo    JARVIS will now update itself automatically when Windows starts!
echo    Windows চালু হলে জার্ভিস এখন স্বয়ংক্রিয়ভাবে আপডেট হবে!
echo.
pause
goto menu

:run_now
echo.
echo Running JARVIS Auto-Updater now...
echo জার্ভিস স্বয়ংক্রিয় আপডেটার এখন চালাচ্ছি...
echo.
python jarvis_auto_updater.py
echo.
pause
goto menu

:run_continuous
echo.
echo Starting JARVIS Continuous Auto-Updater...
echo জার্ভিস ক্রমাগত স্বয়ংক্রিয় আপডেটার শুরু করছি...
echo.
echo This will run in the background and update JARVIS automatically.
echo এটি ব্যাকগ্রাউন্ডে চলবে এবং জার্ভিসকে স্বয়ংক্রিয়ভাবে আপডেট করবে।
echo.
echo Press Ctrl+C to stop
echo বন্ধ করতে Ctrl+C চাপুন
echo.
python jarvis_auto_updater.py --continuous
pause
goto menu

:remove_startup
echo.
echo Removing JARVIS Auto-Updater from Windows Startup...
echo Windows Startup থেকে জার্ভিস স্বয়ংক্রিয় আপডেটার সরাচ্ছি...
echo.

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT=%STARTUP_FOLDER%\JARVIS_Auto_Update.lnk"

if exist "%SHORTCUT%" (
    del "%SHORTCUT%"
    echo ✅ JARVIS Auto-Updater removed from Windows Startup!
    echo ✅ জার্ভিস স্বয়ংক্রিয় আপডেটার Windows Startup থেকে সরানো হয়েছে!
) else (
    echo ℹ️ JARVIS Auto-Updater was not in Windows Startup.
    echo ℹ️ জার্ভিস স্বয়ংক্রিয় আপডেটার Windows Startup-এ ছিল না।
)
echo.
pause
goto menu

:invalid
echo.
echo ❌ Invalid choice! Please try again.
echo ❌ ভুল পছন্দ! আবার চেষ্টা করুন।
echo.
pause
goto menu

:menu
cls
goto :eof

:exit
echo.
echo Goodbye! বিদায়!
echo.
exit
