@echo off
echo ================================================================================
echo   TESTING ULTIMATE LEARNER
echo   আল্টিমেট শিক্ষার্থী পরীক্ষা
echo ================================================================================
echo.

echo This will:
echo - Open Google Chrome
echo - Search Google automatically
echo - Learn from multiple sources
echo - Save everything to database
echo.

echo Test 1: Learn Python Programming
echo পরীক্ষা ১: Python Programming শিখুন
python jarvis_ultimate_learner.py learn Python
echo.
echo ================================================================================
echo.

pause

echo Test 2: Show all learned knowledge
echo পরীক্ষা ২: সব শেখা জ্ঞান দেখান
python jarvis_ultimate_learner.py list
echo.
echo ================================================================================
echo.

pause

echo Test 3: Show statistics
echo পরীক্ষা ৩: পরিসংখ্যান দেখান
python jarvis_ultimate_learner.py stats
echo.
echo ================================================================================
echo.

echo All tests complete!
echo সব পরীক্ষা সম্পূর্ণ!
echo.
echo Chrome should have opened with Google search!
echo Chrome Google search সহ খোলা উচিত ছিল!
pause
