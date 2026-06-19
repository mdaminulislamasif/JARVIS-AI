@echo off
chcp 65001 >nul
color 0B
title JARVIS Master Feature Runner - সব Feature চালান

echo.
echo ═══════════════════════════════════════════════════════════════
echo    🤖 JARVIS MASTER FEATURE RUNNER 🤖
echo    সব JARVIS Feature এক জায়গায়
echo ═══════════════════════════════════════════════════════════════
echo.

:MAIN_MENU
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    🤖 JARVIS MASTER FEATURE RUNNER 🤖
echo ═══════════════════════════════════════════════════════════════
echo.
echo আপনি কি করতে চান? What do you want to do?
echo.
echo ┌─────────────────────────────────────────────────────────────┐
echo │  1. 🚀 JARVIS চালু করুন (Start JARVIS)                     │
echo │  2. 🧠 Learning Features (শেখার Features)                  │
echo │  3. 🌐 Browser Features (Browser Features)                  │
echo │  4. 🎭 3D Face Features (3D মুখ Features)                   │
echo │  5. 🔧 Setup Features (Setup করুন)                         │
echo │  6. 🧪 Testing Features (Test করুন)                        │
echo │  7. 🛠️ Fix Features (সমস্যা ঠিক করুন)                      │
echo │  8. 📚 Dictionary Features (Dictionary Features)            │
echo │  9. 🔄 Update Features (Update Features)                    │
echo │ 10. 🎯 Run ALL Features (সব Features চালান)                │
echo │ 11. ❌ Exit (বের হন)                                        │
echo └─────────────────────────────────────────────────────────────┘
echo.
set /p choice="আপনার পছন্দ লিখুন (Enter your choice): "

if "%choice%"=="1" goto START_JARVIS
if "%choice%"=="2" goto LEARNING_FEATURES
if "%choice%"=="3" goto BROWSER_FEATURES
if "%choice%"=="4" goto FACE_FEATURES
if "%choice%"=="5" goto SETUP_FEATURES
if "%choice%"=="6" goto TESTING_FEATURES
if "%choice%"=="7" goto FIX_FEATURES
if "%choice%"=="8" goto DICTIONARY_FEATURES
if "%choice%"=="9" goto UPDATE_FEATURES
if "%choice%"=="10" goto RUN_ALL
if "%choice%"=="11" goto END
goto MAIN_MENU

:START_JARVIS
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    🚀 JARVIS চালু করুন (Start JARVIS)
echo ═══════════════════════════════════════════════════════════════
echo.
echo কোন version চালাবেন? Which version to start?
echo.
echo  1. JARVIS.bat (Standard)
echo  2. START_JARVIS.bat (Standard Start)
echo  3. JARVIS_START.bat (Alternative Start)
echo  4. Launch_Jarvis_Pro.bat (Pro Version)
echo  5. JARVIS_WITH_SUPER_BRAIN.bat (Super Brain)
echo  6. Start_JARVIS_Background.bat (Background Mode)
echo  7. Back to Main Menu (ফিরে যান)
echo.
set /p start_choice="আপনার পছন্দ (Your choice): "

if "%start_choice%"=="1" (
    echo Starting JARVIS.bat...
    call JARVIS.bat
)
if "%start_choice%"=="2" (
    echo Starting START_JARVIS.bat...
    call START_JARVIS.bat
)
if "%start_choice%"=="3" (
    echo Starting JARVIS_START.bat...
    call JARVIS_START.bat
)
if "%start_choice%"=="4" (
    echo Starting Launch_Jarvis_Pro.bat...
    call Launch_Jarvis_Pro.bat
)
if "%start_choice%"=="5" (
    echo Starting JARVIS_WITH_SUPER_BRAIN.bat...
    call JARVIS_WITH_SUPER_BRAIN.bat
)
if "%start_choice%"=="6" (
    echo Starting Start_JARVIS_Background.bat...
    call Start_JARVIS_Background.bat
)
if "%start_choice%"=="7" goto MAIN_MENU
pause
goto MAIN_MENU

:LEARNING_FEATURES
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    🧠 Learning Features (শেখার Features)
echo ═══════════════════════════════════════════════════════════════
echo.
echo  1. JARVIS_LEARN_EVERYTHING.bat (সব কিছু শিখুন)
echo  2. JARVIS_MASTER_AUTO_LEARN.bat (Master Auto Learning)
echo  3. START_AUTO_LEARNING.bat (Auto Learning চালু করুন)
echo  4. START_SEARCH_LEARNING.bat (Search Learning)
echo  5. START_MULTI_AI_LEARNING.bat (Multi AI Learning)
echo  6. LEARN_ARTICLES.bat (Articles শিখুন)
echo  7. RUN_AUTO_TRAINING.bat (Auto Training)
echo  8. START_INFINITY_BRAIN.bat (Infinity Brain)
echo  9. START_COLLECTIVE_INTELLIGENCE.bat (Collective Intelligence)
echo 10. START_SELF_IMPROVEMENT.bat (Self Improvement)
echo 11. Run ALL Learning Features (সব Learning Features)
echo 12. Back to Main Menu (ফিরে যান)
echo.
set /p learn_choice="আপনার পছন্দ (Your choice): "

if "%learn_choice%"=="1" call JARVIS_LEARN_EVERYTHING.bat
if "%learn_choice%"=="2" call JARVIS_MASTER_AUTO_LEARN.bat
if "%learn_choice%"=="3" call START_AUTO_LEARNING.bat
if "%learn_choice%"=="4" call START_SEARCH_LEARNING.bat
if "%learn_choice%"=="5" call START_MULTI_AI_LEARNING.bat
if "%learn_choice%"=="6" call LEARN_ARTICLES.bat
if "%learn_choice%"=="7" call RUN_AUTO_TRAINING.bat
if "%learn_choice%"=="8" call START_INFINITY_BRAIN.bat
if "%learn_choice%"=="9" call START_COLLECTIVE_INTELLIGENCE.bat
if "%learn_choice%"=="10" call START_SELF_IMPROVEMENT.bat
if "%learn_choice%"=="11" (
    echo Running all learning features...
    call JARVIS_LEARN_EVERYTHING.bat
    call JARVIS_MASTER_AUTO_LEARN.bat
    call START_AUTO_LEARNING.bat
    call START_SEARCH_LEARNING.bat
    call START_MULTI_AI_LEARNING.bat
    call LEARN_ARTICLES.bat
    call RUN_AUTO_TRAINING.bat
    call START_INFINITY_BRAIN.bat
    call START_COLLECTIVE_INTELLIGENCE.bat
    call START_SELF_IMPROVEMENT.bat
)
if "%learn_choice%"=="12" goto MAIN_MENU
pause
goto MAIN_MENU

:BROWSER_FEATURES
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    🌐 Browser Features (Browser Features)
echo ═══════════════════════════════════════════════════════════════
echo.
echo  1. JARVIS_BROWSER.bat (JARVIS Browser)
echo  2. JARVIS_BROWSER_LAUNCHER.bat (Browser Launcher)
echo  3. JARVIS_VOICE_BROWSER.bat (Voice Browser)
echo  4. BUILD_WEBSITE.bat (Website তৈরি করুন)
echo  5. Run ALL Browser Features (সব Browser Features)
echo  6. Back to Main Menu (ফিরে যান)
echo.
set /p browser_choice="আপনার পছন্দ (Your choice): "

if "%browser_choice%"=="1" call JARVIS_BROWSER.bat
if "%browser_choice%"=="2" call JARVIS_BROWSER_LAUNCHER.bat
if "%browser_choice%"=="3" call JARVIS_VOICE_BROWSER.bat
if "%browser_choice%"=="4" call BUILD_WEBSITE.bat
if "%browser_choice%"=="5" (
    echo Running all browser features...
    call JARVIS_BROWSER.bat
    call JARVIS_BROWSER_LAUNCHER.bat
    call JARVIS_VOICE_BROWSER.bat
    call BUILD_WEBSITE.bat
)
if "%browser_choice%"=="6" goto MAIN_MENU
pause
goto MAIN_MENU

:FACE_FEATURES
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    🎭 3D Face Features (3D মুখ Features)
echo ═══════════════════════════════════════════════════════════════
echo.
echo  1. AUTO_CREATE_JARVIS_FACE.bat (Auto Face তৈরি - Blender GUI)
echo  2. CREATE_AND_EXPORT_JARVIS_FACE.bat (Face তৈরি + Export)
echo  3. OPEN_JARVIS_FACE_CREATOR.bat (Browser Version)
echo  4. OPEN_TRANSPARENT_JARVIS_FACE.bat (Transparent Background)
echo  5. LAUNCH_JARVIS_FACE.bat (Face চালু করুন)
echo  6. AUTO_RIG_FACE.bat (Face Rigging)
echo  7. Run ALL Face Features (সব Face Features)
echo  8. Back to Main Menu (ফিরে যান)
echo.
set /p face_choice="আপনার পছন্দ (Your choice): "

if "%face_choice%"=="1" call AUTO_CREATE_JARVIS_FACE.bat
if "%face_choice%"=="2" call CREATE_AND_EXPORT_JARVIS_FACE.bat
if "%face_choice%"=="3" call OPEN_JARVIS_FACE_CREATOR.bat
if "%face_choice%"=="4" call OPEN_TRANSPARENT_JARVIS_FACE.bat
if "%face_choice%"=="5" call LAUNCH_JARVIS_FACE.bat
if "%face_choice%"=="6" call AUTO_RIG_FACE.bat
if "%face_choice%"=="7" (
    echo Running all face features...
    call AUTO_CREATE_JARVIS_FACE.bat
    call CREATE_AND_EXPORT_JARVIS_FACE.bat
    call OPEN_JARVIS_FACE_CREATOR.bat
    call OPEN_TRANSPARENT_JARVIS_FACE.bat
    call LAUNCH_JARVIS_FACE.bat
    call AUTO_RIG_FACE.bat
)
if "%face_choice%"=="8" goto MAIN_MENU
pause
goto MAIN_MENU

:SETUP_FEATURES
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    🔧 Setup Features (Setup করুন)
echo ═══════════════════════════════════════════════════════════════
echo.
echo  1. SETUP_JARVIS_COMPLETE.bat (Complete Setup)
echo  2. SETUP_AUTO_UPDATE.bat (Auto Update Setup)
echo  3. SETUP_AUTO_WORLD_AI_CHAT.bat (World AI Chat Setup)
echo  4. SETUP_CHROME_DEVTOOLS.bat (Chrome DevTools Setup)
echo  5. ADD_SHORTCUTS.bat (Shortcuts যোগ করুন)
echo  6. ADD_FILE_UPLOAD.bat (File Upload যোগ করুন)
echo  7. Run ALL Setup Features (সব Setup Features)
echo  8. Back to Main Menu (ফিরে যান)
echo.
set /p setup_choice="আপনার পছন্দ (Your choice): "

if "%setup_choice%"=="1" call SETUP_JARVIS_COMPLETE.bat
if "%setup_choice%"=="2" call SETUP_AUTO_UPDATE.bat
if "%setup_choice%"=="3" call SETUP_AUTO_WORLD_AI_CHAT.bat
if "%setup_choice%"=="4" call SETUP_CHROME_DEVTOOLS.bat
if "%setup_choice%"=="5" call ADD_SHORTCUTS.bat
if "%setup_choice%"=="6" call ADD_FILE_UPLOAD.bat
if "%setup_choice%"=="7" (
    echo Running all setup features...
    call SETUP_JARVIS_COMPLETE.bat
    call SETUP_AUTO_UPDATE.bat
    call SETUP_AUTO_WORLD_AI_CHAT.bat
    call SETUP_CHROME_DEVTOOLS.bat
    call ADD_SHORTCUTS.bat
    call ADD_FILE_UPLOAD.bat
)
if "%setup_choice%"=="8" goto MAIN_MENU
pause
goto MAIN_MENU

:TESTING_FEATURES
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    🧪 Testing Features (Test করুন)
echo ═══════════════════════════════════════════════════════════════
echo.
echo  1. TEST_JARVIS_NOW.bat (এখনই Test করুন)
echo  2. TEST_AUTONOMOUS.bat (Autonomous Test)
echo  3. TEST_WEB_SEARCH.bat (Web Search Test)
echo  4. TEST_WEB_SEARCH_BUTTON.bat (Web Search Button Test)
echo  5. TEST_SUPER_BRAIN.bat (Super Brain Test)
echo  6. TEST_TREE_LEARNING_QA.bat (Tree Learning QA Test)
echo  7. TEST_TREE_AUTO_LEARNER.bat (Tree Auto Learner Test)
echo  8. TEST_TREE_TAB_LEARNING.bat (Tree Tab Learning Test)
echo  9. TEST_ULTIMATE_LEARNER.bat (Ultimate Learner Test)
echo 10. TEST_INTERNET_LEARNER.bat (Internet Learner Test)
echo 11. TEST_INFINITE_TAB_LEARNING.bat (Infinite Tab Learning Test)
echo 12. TEST_OFFLINE_COMMANDS.bat (Offline Commands Test)
echo 13. TEST_MRX_ALL_SYSTEMS.bat (MRX All Systems Test)
echo 14. DEMO_TREE_LEARNING_QA.bat (Tree Learning QA Demo)
echo 15. Run ALL Testing Features (সব Testing Features)
echo 16. Back to Main Menu (ফিরে যান)
echo.
set /p test_choice="আপনার পছন্দ (Your choice): "

if "%test_choice%"=="1" call TEST_JARVIS_NOW.bat
if "%test_choice%"=="2" call TEST_AUTONOMOUS.bat
if "%test_choice%"=="3" call TEST_WEB_SEARCH.bat
if "%test_choice%"=="4" call TEST_WEB_SEARCH_BUTTON.bat
if "%test_choice%"=="5" call TEST_SUPER_BRAIN.bat
if "%test_choice%"=="6" call TEST_TREE_LEARNING_QA.bat
if "%test_choice%"=="7" call TEST_TREE_AUTO_LEARNER.bat
if "%test_choice%"=="8" call TEST_TREE_TAB_LEARNING.bat
if "%test_choice%"=="9" call TEST_ULTIMATE_LEARNER.bat
if "%test_choice%"=="10" call TEST_INTERNET_LEARNER.bat
if "%test_choice%"=="11" call TEST_INFINITE_TAB_LEARNING.bat
if "%test_choice%"=="12" call TEST_OFFLINE_COMMANDS.bat
if "%test_choice%"=="13" call TEST_MRX_ALL_SYSTEMS.bat
if "%test_choice%"=="14" call DEMO_TREE_LEARNING_QA.bat
if "%test_choice%"=="15" (
    echo Running all testing features...
    call TEST_JARVIS_NOW.bat
    call TEST_AUTONOMOUS.bat
    call TEST_WEB_SEARCH.bat
    call TEST_WEB_SEARCH_BUTTON.bat
    call TEST_SUPER_BRAIN.bat
    call TEST_TREE_LEARNING_QA.bat
    call TEST_TREE_AUTO_LEARNER.bat
    call TEST_TREE_TAB_LEARNING.bat
    call TEST_ULTIMATE_LEARNER.bat
    call TEST_INTERNET_LEARNER.bat
    call TEST_INFINITE_TAB_LEARNING.bat
    call TEST_OFFLINE_COMMANDS.bat
    call TEST_MRX_ALL_SYSTEMS.bat
    call DEMO_TREE_LEARNING_QA.bat
)
if "%test_choice%"=="16" goto MAIN_MENU
pause
goto MAIN_MENU

:FIX_FEATURES
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    🛠️ Fix Features (সমস্যা ঠিক করুন)
echo ═══════════════════════════════════════════════════════════════
echo.
echo  1. FIX_AND_TEST_EVERYTHING.bat (সব কিছু ঠিক করুন + Test)
echo  2. FIX_WORLD_AI_CHAT.bat (World AI Chat ঠিক করুন)
echo  3. FIX_JARVIS_FACE_3D.bat (3D Face ঠিক করুন)
echo  4. FIX_API_PROBLEM.bat (API সমস্যা ঠিক করুন)
echo  5. RUN_FIX.bat (Fix চালান)
echo  6. CLEAN_CACHE.bat (Cache পরিষ্কার করুন)
echo  7. Run ALL Fix Features (সব Fix Features)
echo  8. Back to Main Menu (ফিরে যান)
echo.
set /p fix_choice="আপনার পছন্দ (Your choice): "

if "%fix_choice%"=="1" call FIX_AND_TEST_EVERYTHING.bat
if "%fix_choice%"=="2" call FIX_WORLD_AI_CHAT.bat
if "%fix_choice%"=="3" call FIX_JARVIS_FACE_3D.bat
if "%fix_choice%"=="4" call FIX_API_PROBLEM.bat
if "%fix_choice%"=="5" call RUN_FIX.bat
if "%fix_choice%"=="6" call CLEAN_CACHE.bat
if "%fix_choice%"=="7" (
    echo Running all fix features...
    call FIX_AND_TEST_EVERYTHING.bat
    call FIX_WORLD_AI_CHAT.bat
    call FIX_JARVIS_FACE_3D.bat
    call FIX_API_PROBLEM.bat
    call RUN_FIX.bat
    call CLEAN_CACHE.bat
)
if "%fix_choice%"=="8" goto MAIN_MENU
pause
goto MAIN_MENU

:DICTIONARY_FEATURES
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    📚 Dictionary Features (Dictionary Features)
echo ═══════════════════════════════════════════════════════════════
echo.
echo  1. ADD_DICTIONARY.bat (Dictionary যোগ করুন)
echo  2. Back to Main Menu (ফিরে যান)
echo.
set /p dict_choice="আপনার পছন্দ (Your choice): "

if "%dict_choice%"=="1" call ADD_DICTIONARY.bat
if "%dict_choice%"=="2" goto MAIN_MENU
pause
goto MAIN_MENU

:UPDATE_FEATURES
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    🔄 Update Features (Update Features)
echo ═══════════════════════════════════════════════════════════════
echo.
echo  1. JARVIS_AUTO_UPDATE_STARTUP.bat (Auto Update Startup)
echo  2. CHANGE_CHENG BOT_NAME.bat (Cheng Bot নাম পরিবর্তন করুন)
echo  3. Back to Main Menu (ফিরে যান)
echo.
set /p update_choice="আপনার পছন্দ (Your choice): "

if "%update_choice%"=="1" call JARVIS_AUTO_UPDATE_STARTUP.bat
if "%update_choice%"=="2" call CHANGE_CHENG BOT_NAME.bat
if "%update_choice%"=="3" goto MAIN_MENU
pause
goto MAIN_MENU

:RUN_ALL
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    ⚠️ WARNING - সতর্কতা ⚠️
echo ═══════════════════════════════════════════════════════════════
echo.
echo এটি সব Features একসাথে চালাবে! এটি অনেক সময় নিতে পারে।
echo This will run ALL features together! This may take a long time.
echo.
echo আপনি কি নিশ্চিত? Are you sure?
echo.
echo  1. Yes, run everything (হ্যাঁ, সব চালান)
echo  2. No, go back (না, ফিরে যান)
echo.
set /p confirm="আপনার পছন্দ (Your choice): "

if "%confirm%"=="2" goto MAIN_MENU
if not "%confirm%"=="1" goto MAIN_MENU

echo.
echo ═══════════════════════════════════════════════════════════════
echo    🚀 Running ALL Features - সব Features চালানো হচ্ছে
echo ═══════════════════════════════════════════════════════════════
echo.

echo [1/9] Running Learning Features...
call JARVIS_LEARN_EVERYTHING.bat
call JARVIS_MASTER_AUTO_LEARN.bat
call START_AUTO_LEARNING.bat
call START_SEARCH_LEARNING.bat
call START_MULTI_AI_LEARNING.bat
call LEARN_ARTICLES.bat
call RUN_AUTO_TRAINING.bat
call START_INFINITY_BRAIN.bat
call START_COLLECTIVE_INTELLIGENCE.bat
call START_SELF_IMPROVEMENT.bat

echo [2/9] Running Browser Features...
call JARVIS_BROWSER.bat
call JARVIS_BROWSER_LAUNCHER.bat
call JARVIS_VOICE_BROWSER.bat
call BUILD_WEBSITE.bat

echo [3/9] Running 3D Face Features...
call AUTO_CREATE_JARVIS_FACE.bat
call CREATE_AND_EXPORT_JARVIS_FACE.bat
call LAUNCH_JARVIS_FACE.bat
call AUTO_RIG_FACE.bat

echo [4/9] Running Setup Features...
call SETUP_JARVIS_COMPLETE.bat
call SETUP_AUTO_UPDATE.bat
call SETUP_AUTO_WORLD_AI_CHAT.bat
call SETUP_CHROME_DEVTOOLS.bat
call ADD_SHORTCUTS.bat
call ADD_FILE_UPLOAD.bat

echo [5/9] Running Testing Features...
call TEST_JARVIS_NOW.bat
call TEST_AUTONOMOUS.bat
call TEST_WEB_SEARCH.bat
call TEST_WEB_SEARCH_BUTTON.bat
call TEST_SUPER_BRAIN.bat
call TEST_TREE_LEARNING_QA.bat
call TEST_TREE_AUTO_LEARNER.bat
call TEST_TREE_TAB_LEARNING.bat
call TEST_ULTIMATE_LEARNER.bat
call TEST_INTERNET_LEARNER.bat
call TEST_INFINITE_TAB_LEARNING.bat
call TEST_OFFLINE_COMMANDS.bat
call TEST_MRX_ALL_SYSTEMS.bat
call DEMO_TREE_LEARNING_QA.bat

echo [6/9] Running Fix Features...
call FIX_AND_TEST_EVERYTHING.bat
call FIX_WORLD_AI_CHAT.bat
call FIX_JARVIS_FACE_3D.bat
call FIX_API_PROBLEM.bat
call RUN_FIX.bat
call CLEAN_CACHE.bat

echo [7/9] Running Dictionary Features...
call ADD_DICTIONARY.bat

echo [8/9] Running Update Features...
call JARVIS_AUTO_UPDATE_STARTUP.bat

echo [9/9] Running Additional Features...
call JARVIS_CONVERSATION.bat
call JARVIS_AUTONOMOUS.bat
call JARVIS_PROGRAMMING.bat
call JARVIS_MONITOR.bat
call RUN_JAVA_TEACHER.bat
call build_jarvis.bat
call build_installer.bat
call rebuild_with_icon.bat

echo.
echo ═══════════════════════════════════════════════════════════════
echo    ✅ ALL FEATURES COMPLETED - সব Features সম্পন্ন হয়েছে
echo ═══════════════════════════════════════════════════════════════
echo.
pause
goto MAIN_MENU

:END
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo    👋 Thank you for using JARVIS Master Feature Runner!
echo    JARVIS ব্যবহার করার জন্য ধন্যবাদ!
echo ═══════════════════════════════════════════════════════════════
echo.
timeout /t 2 >nul
exit
