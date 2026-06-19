@echo off
echo ================================================================================
echo   TESTING JARVIS WITH OFFLINE BRAIN
echo   JARVIS OFFLINE BRAIN টেস্ট করা হচ্ছে
echo ================================================================================
echo.
echo This will:
echo   1. Verify all fixes are in place
echo   2. Show you how to test JARVIS
echo.
echo এটা করবে:
echo   1. সব fix যাচাই করবে
echo   2. JARVIS কিভাবে টেস্ট করবেন দেখাবে
echo.
pause
echo.
echo ================================================================================
echo   STEP 1: VERIFYING FIXES
echo   ধাপ ১: FIX যাচাই করা হচ্ছে
echo ================================================================================
echo.
python VERIFY_ALL_FIXES.py
echo.
echo ================================================================================
echo   STEP 2: INSTRUCTIONS TO TEST JARVIS
echo   ধাপ ২: JARVIS টেস্ট করার নির্দেশনা
echo ================================================================================
echo.
echo IMPORTANT: Close this window and follow these steps:
echo গুরুত্বপূর্ণ: এই window বন্ধ করুন এবং এই ধাপগুলো অনুসরণ করুন:
echo.
echo 1. If JARVIS is running, CLOSE IT (close the window completely)
echo    যদি JARVIS চালু থাকে, বন্ধ করুন (window সম্পূর্ণ বন্ধ করুন)
echo.
echo 2. Double-click one of these files to start JARVIS:
echo    JARVIS চালু করতে এই files এর একটিতে double-click করুন:
echo    - JARVIS.bat
echo    - START_JARVIS.bat
echo    - JARVIS_START.bat
echo.
echo 3. When JARVIS starts, type one of these commands:
echo    JARVIS চালু হলে, এই commands এর একটি টাইপ করুন:
echo    - HELLO
echo    - 2+2
echo    - help
echo    - open chrome
echo.
echo 4. You should see:
echo    আপনি দেখবেন:
echo    [SYSTEM]^> API quota exceeded. Switching to OFFLINE BRAIN...
echo    [JARVIS]^> [OFFLINE] ^<response^>
echo.
echo 5. If you see [OFFLINE] in the response, IT WORKS!
echo    যদি response এ [OFFLINE] দেখেন, তাহলে কাজ করছে!
echo.
echo ================================================================================
echo   WHAT IF IT DOESN'T WORK?
echo   যদি কাজ না করে?
echo ================================================================================
echo.
echo If you still see the quota error:
echo যদি এখনও quota error দেখেন:
echo.
echo 1. Make sure you COMPLETELY CLOSED JARVIS before restarting
echo    নিশ্চিত করুন যে JARVIS সম্পূর্ণ বন্ধ করেছেন restart করার আগে
echo.
echo 2. Delete these folders if they exist:
echo    এই folders মুছে ফেলুন যদি থাকে:
echo    - __pycache__
echo    - core/__pycache__
echo    - engine/__pycache__
echo.
echo 3. Run this file again: TEST_JARVIS_NOW.bat
echo    এই file আবার চালান: TEST_JARVIS_NOW.bat
echo.
echo 4. Read the guide: FIX_COMPLETE_GUIDE.txt
echo    গাইড পড়ুন: FIX_COMPLETE_GUIDE.txt
echo.
echo ================================================================================
pause
