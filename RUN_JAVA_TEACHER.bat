@echo off
REM JARVIS JAVA TEACHER LAUNCHER
REM জার্ভিস জাভা শিক্ষক লঞ্চার

title JARVIS Java Teacher
color 0A

echo.
echo ========================================
echo   JARVIS JAVA TEACHER
echo   জার্ভিস জাভা শিক্ষক
echo ========================================
echo.

:MENU
echo.
echo Choose an option / একটি বিকল্প চয়ন করুন:
echo.
echo 1. Show Curriculum (সম্পূর্ণ পাঠ্যক্রম দেখুন)
echo 2. Start Lesson 1 (পাঠ ১ শুরু করুন)
echo 3. Start Lesson 2 (পাঠ ২ শুরু করুন)
echo 4. Show Progress (অগ্রগতি দেখুন)
echo 5. Mark Lesson Complete (পাঠ সম্পূর্ণ চিহ্নিত করুন)
echo 6. Exit (প্রস্থান)
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto CURRICULUM
if "%choice%"=="2" goto LESSON1
if "%choice%"=="3" goto LESSON2
if "%choice%"=="4" goto PROGRESS
if "%choice%"=="5" goto COMPLETE
if "%choice%"=="6" goto EXIT

echo Invalid choice! / অবৈধ পছন্দ!
goto MENU

:CURRICULUM
cls
python jarvis_java_teacher.py curriculum
pause
goto MENU

:LESSON1
cls
python jarvis_java_teacher.py lesson 1
pause
goto MENU

:LESSON2
cls
python jarvis_java_teacher.py lesson 2
pause
goto MENU

:PROGRESS
cls
python jarvis_java_teacher.py progress
pause
goto MENU

:COMPLETE
echo.
set /p lesson_num="Enter lesson number to mark complete: "
python jarvis_java_teacher.py complete %lesson_num%
pause
goto MENU

:EXIT
echo.
echo Thank you for learning with JARVIS!
echo জার্ভিসের সাথে শেখার জন্য ধন্যবাদ!
echo.
pause
exit
