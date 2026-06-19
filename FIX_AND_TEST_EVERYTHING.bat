@echo off
color 0A
echo ================================================================================
echo   🔧 COMPLETE FIX AND TEST FOR JARVIS API QUOTA PROBLEM
echo   🔧 JARVIS API QUOTA সমস্যার সম্পূর্ণ FIX এবং টেস্ট
echo ================================================================================
echo.
echo This script will:
echo এই script করবে:
echo   1. Clean Python cache files
echo   2. Verify all fixes are in place
echo   3. Show you how to test JARVIS
echo.
echo   1. Python cache files পরিষ্কার করবে
echo   2. সব fixes যাচাই করবে
echo   3. JARVIS কিভাবে টেস্ট করবেন দেখাবে
echo.
pause
echo.

echo ================================================================================
echo   STEP 1: CLEANING PYTHON CACHE
echo   ধাপ ১: PYTHON CACHE পরিষ্কার করা হচ্ছে
echo ================================================================================
echo.

if exist "__pycache__" (
    echo Deleting: __pycache__
    rmdir /s /q "__pycache__"
    echo   ✅ Deleted
)

if exist "core\__pycache__" (
    echo Deleting: core\__pycache__
    rmdir /s /q "core\__pycache__"
    echo   ✅ Deleted
)

if exist "engine\__pycache__" (
    echo Deleting: engine\__pycache__
    rmdir /s /q "engine\__pycache__"
    echo   ✅ Deleted
)

if exist "server\__pycache__" (
    echo Deleting: server\__pycache__
    rmdir /s /q "server\__pycache__"
    echo   ✅ Deleted
)

echo.
echo ✅ Cache cleaned!
echo ✅ Cache পরিষ্কার হয়ে গেছে!
echo.
pause

echo.
echo ================================================================================
echo   STEP 2: VERIFYING ALL FIXES
echo   ধাপ ২: সব FIX যাচাই করা হচ্ছে
echo ================================================================================
echo.

python VERIFY_ALL_FIXES.py

echo.
pause

echo.
echo ================================================================================
echo   STEP 3: HOW TO TEST JARVIS
echo   ধাপ ৩: JARVIS কিভাবে টেস্ট করবেন
echo ================================================================================
echo.
echo IMPORTANT INSTRUCTIONS:
echo গুরুত্বপূর্ণ নির্দেশনা:
echo.
echo 1. CLOSE THIS WINDOW
echo    এই WINDOW বন্ধ করুন
echo.
echo 2. If JARVIS is running, CLOSE IT (close the window completely)
echo    যদি JARVIS চালু থাকে, বন্ধ করুন (window সম্পূর্ণ বন্ধ করুন)
echo.
echo 3. START JARVIS by double-clicking one of these:
echo    JARVIS চালু করুন এগুলোর একটিতে double-click করে:
echo    📁 JARVIS.bat
echo    📁 START_JARVIS.bat
echo    📁 JARVIS_START.bat
echo.
echo 4. When JARVIS starts, type one of these commands:
echo    JARVIS চালু হলে, এই commands এর একটি টাইপ করুন:
echo    ✅ HELLO
echo    ✅ 2+2
echo    ✅ help
echo    ✅ open chrome
echo.
echo 5. YOU SHOULD SEE:
echo    আপনি দেখবেন:
echo    [SYSTEM]^> API quota exceeded. Switching to OFFLINE BRAIN...
echo    [JARVIS]^> [OFFLINE] ^<response^>
echo.
echo 6. If you see [OFFLINE] in the response, IT WORKS! ✅
echo    যদি response এ [OFFLINE] দেখেন, তাহলে কাজ করছে! ✅
echo.
echo ================================================================================
echo   TROUBLESHOOTING
echo   সমস্যা সমাধান
echo ================================================================================
echo.
echo If you still see the quota error:
echo যদি এখনও quota error দেখেন:
echo.
echo 1. Make sure you COMPLETELY CLOSED JARVIS before restarting
echo    নিশ্চিত করুন যে JARVIS সম্পূর্ণ বন্ধ করেছেন restart করার আগে
echo.
echo 2. Run this script again: FIX_AND_TEST_EVERYTHING.bat
echo    এই script আবার চালান: FIX_AND_TEST_EVERYTHING.bat
echo.
echo 3. Read the detailed guide: FIX_COMPLETE_GUIDE.txt
echo    বিস্তারিত গাইড পড়ুন: FIX_COMPLETE_GUIDE.txt
echo.
echo 4. Read the quick start: QUICK_START.txt
echo    দ্রুত শুরু পড়ুন: QUICK_START.txt
echo.
echo ================================================================================
echo   📚 HELPFUL FILES
echo   📚 সহায়ক ফাইল
echo ================================================================================
echo.
echo 📁 QUICK_START.txt              - Quick reference
echo 📁 PROBLEM_SOLVED_SUMMARY.txt   - Complete summary
echo 📁 FIX_COMPLETE_GUIDE.txt       - Detailed guide
echo 📁 VERIFY_ALL_FIXES.py          - Verification script
echo 📁 CLEAN_CACHE.bat              - Clean cache only
echo.
echo ================================================================================
echo   🎉 ALL DONE! NOW TEST YOUR JARVIS!
echo   🎉 সব শেষ! এখন আপনার JARVIS টেস্ট করুন!
echo ================================================================================
echo.
pause
