@echo off
echo ================================================================================
echo   TESTING INTERNET LEARNER
echo   ইন্টারনেট শিক্ষার্থী পরীক্ষা
echo ================================================================================
echo.

echo Test 1: Learn about Python
echo পরীক্ষা ১: Python সম্পর্কে শিখুন
python jarvis_internet_learner.py learn Python
echo.
echo ================================================================================
echo.

echo Test 2: Learn about Artificial Intelligence
echo পরীক্ষা ২: Artificial Intelligence সম্পর্কে শিখুন
python jarvis_internet_learner.py learn "Artificial Intelligence"
echo.
echo ================================================================================
echo.

echo Test 3: List learned topics
echo পরীক্ষা ৩: শেখা বিষয়ের তালিকা
python jarvis_internet_learner.py list
echo.
echo ================================================================================
echo.

echo Test 4: Search learned knowledge
echo পরীক্ষা ৪: শেখা জ্ঞান খুঁজুন
python jarvis_internet_learner.py search Python
echo.
echo ================================================================================
echo.

echo Test 5: Show statistics
echo পরীক্ষা ৫: পরিসংখ্যান দেখান
python jarvis_internet_learner.py stats
echo.
echo ================================================================================
echo.

echo All tests complete!
echo সব পরীক্ষা সম্পূর্ণ!
pause
