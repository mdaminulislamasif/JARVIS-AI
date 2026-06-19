@echo off
echo ================================================================================
echo   TESTING WEB SEARCH BUTTON FEATURE
echo   ওয়েব সার্চ বাটন ফিচার পরীক্ষা
echo ================================================================================
echo.

echo Starting JARVIS Panel...
echo JARVIS Panel শুরু করছি...
echo.

echo INSTRUCTIONS / নির্দেশাবলী:
echo ================================
echo.
echo 1. Wait for JARVIS Panel to open
echo    JARVIS Panel খোলার জন্য অপেক্ষা করুন
echo.
echo 2. Look for the green "🔍 WEB" button at the bottom
echo    নিচে সবুজ "🔍 WEB" বাটন খুঁজুন
echo.
echo 3. Type something in the chat box, for example:
echo    চ্যাট বক্সে কিছু টাইপ করুন, উদাহরণ:
echo    - "Python programming"
echo    - "youtube funny videos"
echo    - "github Python projects"
echo.
echo 4. Click the "🔍 WEB" button
echo    "🔍 WEB" বাটনে ক্লিক করুন
echo.
echo 5. Check if:
echo    পরীক্ষা করুন:
echo    ✅ Browser opens with search results
echo    ✅ JARVIS logs the search action
echo    ✅ JARVIS explains what it understood
echo    ✅ Chat box clears after search
echo.
echo ================================================================================
echo.

python jarvis_panel.py

echo.
echo ================================================================================
echo   TEST COMPLETE
echo   পরীক্ষা সম্পূর্ণ
echo ================================================================================
pause
