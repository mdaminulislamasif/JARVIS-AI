@echo off
title JARVIS AUTONOMOUS SYSTEM TEST
color 0C

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          🔥 JARVIS AUTONOMOUS SYSTEM TEST 🔥                      ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo Testing JARVIS Autonomous System...
echo JARVIS স্বয়ংক্রিয় সিস্টেম পরীক্ষা করছি...
echo.

:MENU
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                    AUTONOMOUS TEST MENU                          ║
echo ║                স্বয়ংক্রিয় পরীক্ষা মেনু                           ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo [1] Check Admin Rights / Admin Rights চেক করুন
echo [2] Get Admin Rights / Admin Rights নিন
echo [3] Collect System Data / System Data Collect করুন
echo [4] Add to Startup / Startup এ Add করুন
echo [5] Show Capabilities / ক্ষমতা দেখুন
echo [6] Create Software (Autonomous) / Software তৈরি (স্বয়ংক্রিয়)
echo [7] Read Guide / গাইড পড়ুন
echo [8] Exit / বের হন
echo.
set /p choice="Enter your choice / আপনার পছন্দ লিখুন (1-8): "

if "%choice%"=="1" goto CHECK_ADMIN
if "%choice%"=="2" goto GET_ADMIN
if "%choice%"=="3" goto COLLECT_DATA
if "%choice%"=="4" goto ADD_STARTUP
if "%choice%"=="5" goto SHOW_CAPS
if "%choice%"=="6" goto CREATE_SOFTWARE
if "%choice%"=="7" goto GUIDE
if "%choice%"=="8" goto END
goto MENU

:CHECK_ADMIN
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Checking Admin Rights...
echo Admin Rights চেক করছি...
echo ═══════════════════════════════════════════════════════════════════
echo.
python -c "from jarvis_autonomous_system import AutonomousSystem; sys = AutonomousSystem(); print('Admin Rights:', 'YES' if sys.is_admin else 'NO')"
echo.
pause
goto MENU

:GET_ADMIN
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Getting Admin Rights...
echo Admin Rights নিচ্ছি...
echo ═══════════════════════════════════════════════════════════════════
echo.
python jarvis_autonomous_system.py "get admin rights"
echo.
pause
goto MENU

:COLLECT_DATA
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Collecting System Data...
echo System Data Collect করছি...
echo ═══════════════════════════════════════════════════════════════════
echo.
python jarvis_autonomous_system.py "collect system data"
echo.
pause
goto MENU

:ADD_STARTUP
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Adding to Startup...
echo Startup এ Add করছি...
echo ═══════════════════════════════════════════════════════════════════
echo.
python jarvis_autonomous_system.py "add to startup"
echo.
pause
goto MENU

:SHOW_CAPS
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Showing Capabilities...
echo ক্ষমতা দেখাচ্ছি...
echo ═══════════════════════════════════════════════════════════════════
echo.
python -c "from jarvis_autonomous_system import AutonomousSystem; sys = AutonomousSystem(); result = sys.get_capabilities(); print(result['response'])"
echo.
pause
goto MENU

:CREATE_SOFTWARE
echo.
echo ═══════════════════════════════════════════════════════════════════
echo Creating Software Autonomously...
echo স্বয়ংক্রিয়ভাবে Software তৈরি করছি...
echo ═══════════════════════════════════════════════════════════════════
echo.
python jarvis_autonomous_system.py "create calculator software"
echo.
pause
goto MENU

:GUIDE
echo.
echo Opening guide...
echo গাইড খুলছি...
if exist AUTONOMOUS_SYSTEM_GUIDE.txt (
    start AUTONOMOUS_SYSTEM_GUIDE.txt
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
echo Thank you for testing JARVIS Autonomous System!
echo JARVIS স্বয়ংক্রিয় সিস্টেম পরীক্ষা করার জন্য ধন্যবাদ!
echo ═══════════════════════════════════════════════════════════════════
echo.
pause
exit
