@echo off
color 0A
title JARVIS WEB SEARCH TEST
echo ================================================================================
echo   JARVIS OFFLINE BRAIN - WEB SEARCH TEST
echo   JARVIS অফলাইন ব্রেইন - ওয়েব সার্চ টেস্ট
echo ================================================================================
echo.
echo This will test the new web search features!
echo এটা নতুন web search features টেস্ট করবে!
echo.
pause
echo.

echo ================================================================================
echo   TEST 1: Google Search
echo ================================================================================
echo.
echo Testing: search Python tutorial
python -c "from jarvis_offline_brain import OfflineBrain; brain = OfflineBrain(); result = brain.process_command('search Python tutorial'); print(result['response'])"
echo.
echo Did Google open with Python tutorial search? (Y/N)
echo Google খুলেছে Python tutorial search সহ? (Y/N)
pause
echo.

echo ================================================================================
echo   TEST 2: YouTube Search
echo ================================================================================
echo.
echo Testing: search youtube Python
python -c "from jarvis_offline_brain import OfflineBrain; brain = OfflineBrain(); result = brain.process_command('search youtube Python'); print(result['response'])"
echo.
echo Did YouTube open with Python search? (Y/N)
echo YouTube খুলেছে Python search সহ? (Y/N)
pause
echo.

echo ================================================================================
echo   TEST 3: Image Search
echo ================================================================================
echo.
echo Testing: search image cat
python -c "from jarvis_offline_brain import OfflineBrain; brain = OfflineBrain(); result = brain.process_command('search image cat'); print(result['response'])"
echo.
echo Did Google Images open with cat pictures? (Y/N)
echo Google Images খুলেছে cat pictures সহ? (Y/N)
pause
echo.

echo ================================================================================
echo   TEST 4: Wikipedia Search
echo ================================================================================
echo.
echo Testing: search wikipedia Python
python -c "from jarvis_offline_brain import OfflineBrain; brain = OfflineBrain(); result = brain.process_command('search wikipedia Python'); print(result['response'])"
echo.
echo Did Wikipedia open with Python search? (Y/N)
echo Wikipedia খুলেছে Python search সহ? (Y/N)
pause
echo.

echo ================================================================================
echo   TEST 5: GitHub Search
echo ================================================================================
echo.
echo Testing: search github Python
python -c "from jarvis_offline_brain import OfflineBrain; brain = OfflineBrain(); result = brain.process_command('search github Python'); print(result['response'])"
echo.
echo Did GitHub open with Python search? (Y/N)
echo GitHub খুলেছে Python search সহ? (Y/N)
pause
echo.

echo ================================================================================
echo   ALL TESTS COMPLETE!
echo   সব টেস্ট সম্পূর্ণ!
echo ================================================================================
echo.
echo If all tests passed, web search is working! ✅
echo যদি সব টেস্ট পাস করে, তাহলে web search কাজ করছে! ✅
echo.
echo Now you can use these commands in JARVIS:
echo এখন আপনি JARVIS এ এই commands ব্যবহার করতে পারেন:
echo.
echo   search Python tutorial
echo   search youtube Python
echo   search image cat
echo   search wikipedia Python
echo   search github Python
echo   search stackoverflow Python error
echo   search news Bangladesh
echo   search map Dhaka
echo   search amazon laptop
echo.
echo Read WEB_SEARCH_GUIDE.txt for more information!
echo আরো তথ্যের জন্য WEB_SEARCH_GUIDE.txt পড়ুন!
echo.
pause
