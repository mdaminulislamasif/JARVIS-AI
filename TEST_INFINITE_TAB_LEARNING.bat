@echo off
echo ========================================
echo TESTING INFINITE TAB LEARNING
echo ========================================
echo.
echo This will test:
echo 1. Infinite Tab Learner
echo 2. Auto Learning Bug Fix
echo 3. All Learning Systems
echo.
echo WARNING: This will open MANY browser tabs!
echo Press Ctrl+C to stop anytime
echo.
pause

python -c "from jarvis_infinite_tab_learner import InfiniteTabLearner; learner = InfiniteTabLearner(); learner.start_infinite_learning('Python programming')"

pause
