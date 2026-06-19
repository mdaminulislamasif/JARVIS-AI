@echo off
color 0A
title JARVIS WEBSITE BUILDER
echo ================================================================================
echo   JARVIS WEBSITE BUILDER
echo   JARVIS ওয়েবসাইট বিল্ডার
echo ================================================================================
echo.
echo Build professional websites with simple commands!
echo সহজ commands দিয়ে professional websites তৈরি করুন!
echo.
echo Choose website type / ওয়েবসাইট এর ধরন বেছে নিন:
echo.
echo   1. Simple Website (একটা simple website)
echo   2. Portfolio Website (Portfolio website)
echo   3. Business Website (Business website)
echo   4. Blog Website (Blog website)
echo   5. Landing Page (Landing page)
echo   6. E-commerce Website (E-commerce website)
echo   7. Exit (বের হন)
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    set type=simple
    set typename=Simple Website
) else if "%choice%"=="2" (
    set type=portfolio
    set typename=Portfolio Website
) else if "%choice%"=="3" (
    set type=business
    set typename=Business Website
) else if "%choice%"=="4" (
    set type=blog
    set typename=Blog Website
) else if "%choice%"=="5" (
    set type=landing
    set typename=Landing Page
) else if "%choice%"=="6" (
    set type=ecommerce
    set typename=E-commerce Website
) else if "%choice%"=="7" (
    echo.
    echo Exiting... / বের হচ্ছে...
    exit /b
) else (
    echo.
    echo Invalid choice! / ভুল choice!
    pause
    exit /b
)

echo.
echo You selected: %typename%
echo আপনি বেছে নিয়েছেন: %typename%
echo.
set /p name="Enter website name (or press Enter for default): "

if "%name%"=="" (
    set name=My Website
)

echo.
echo Building %typename%: %name%
echo %typename% তৈরি করা হচ্ছে: %name%
echo.

python jarvis_website_builder.py %type% "%name%"

echo.
echo ================================================================================
echo   WEBSITE BUILT SUCCESSFULLY!
echo   ওয়েবসাইট সফলভাবে তৈরি হয়েছে!
echo ================================================================================
echo.
echo Your website is ready! / আপনার website প্রস্তুত!
echo.
echo To view / দেখতে:
echo   1. Go to jarvis_websites folder
echo   2. Find your website folder
echo   3. Double-click index.html
echo   4. It will open in browser!
echo.
echo   1. jarvis_websites folder এ যান
echo   2. আপনার website folder খুঁজুন
echo   3. index.html এ double-click করুন
echo   4. Browser এ খুলবে!
echo.
echo Read WEBSITE_BUILDER_GUIDE.txt for more information!
echo আরো তথ্যের জন্য WEBSITE_BUILDER_GUIDE.txt পড়ুন!
echo.
pause
