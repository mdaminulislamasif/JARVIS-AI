@echo off
title JARVIS SUPER BRAIN TEST
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║              JARVIS SUPER BRAIN TEST                             ║
echo ║          সুপার ব্রেইন পরীক্ষা করুন                              ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo Testing JARVIS Super Brain capabilities...
echo JARVIS সুপার ব্রেইন এর ক্ষমতা পরীক্ষা করছি...
echo.

:MENU
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    TEST MENU / পরীক্ষা মেনু                      ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo [1] Test Calculator Software / Calculator Software পরীক্ষা
echo [2] Test Android App / Android App পরীক্ষা
echo [3] Test PC Panel / PC Panel পরীক্ষা
echo [4] Test General Software / General Software পরীক্ষা
echo [5] Test Search & Learn / Search এবং Learn পরীক্ষা
echo [6] Open Projects Folder / Projects Folder খুলুন
echo [7] Read Guide / গাইড পড়ুন
echo [8] Exit / বের হন
echo.
set /p choice="Enter your choice / আপনার পছন্দ লিখুন (1-8): "

if "%choice%"=="1" goto TEST1
if "%choice%"=="2" goto TEST2
if "%choice%"=="3" goto TEST3
if "%choice%"=="4" goto TEST4
if "%choice%"=="5" goto TEST5
if "%choice%"=="6" goto FOLDER
if "%choice%"=="7" goto GUIDE
if "%choice%"=="8" goto END
goto MENU

:TEST1
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Testing: Create Calculator Software
echo পরীক্ষা: Calculator Software তৈরি
echo ═══════════════════════════════════════════════════════════════════
echo.
python jarvis_super_brain.py create calculator software
echo.
pause
goto MENU

:TEST2
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Testing: Build Android App
echo পরীক্ষা: Android App তৈরি
echo ═══════════════════════════════════════════════════════════════════
echo.
python jarvis_super_brain.py build android app
echo.
pause
goto MENU

:TEST3
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Testing: Make PC Panel
echo পরীক্ষা: PC Panel তৈরি
echo ═══════════════════════════════════════════════════════════════════
echo.
python jarvis_super_brain.py make pc panel
echo.
pause
goto MENU

:TEST4
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Testing: Create Todo List Software
echo পরীক্ষা: Todo List Software তৈরি
echo ═══════════════════════════════════════════════════════════════════
echo.
python jarvis_super_brain.py create todo list software
echo.
pause
goto MENU

:TEST5
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Testing: Search and Learn
echo পরীক্ষা: Search এবং Learn
echo ═══════════════════════════════════════════════════════════════════
echo.
python jarvis_super_brain.py search Python programming
echo.
pause
goto MENU

:FOLDER
echo.
echo Opening projects folder...
echo Projects folder খুলছি...
if exist jarvis_projects (
    start jarvis_projects
) else (
    echo Projects folder not found! Create a project first!
    echo Projects folder পাওয়া যায়নি! প্রথমে একটি project তৈরি করুন!
)
echo.
pause
goto MENU

:GUIDE
echo.
echo Opening guide...
echo গাইড খুলছি...
if exist SUPER_BRAIN_GUIDE.txt (
    start SUPER_BRAIN_GUIDE.txt
) else (
    echo Guide not found!
    echo গাইড পাওয়া যায়নি!
)
echo.
pause
goto MENU

:END
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Thank you for testing JARVIS Super Brain!
echo JARVIS সুপার ব্রেইন পরীক্ষা করার জন্য ধন্যবাদ!
echo ═══════════════════════════════════════════════════════════════════
echo.
pause
exit
