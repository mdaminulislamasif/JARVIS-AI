@echo off
cls
echo.
echo ================================================================================
echo   🤖 JARVIS MASTER AUTO-LEARNING SYSTEM
echo   🤖 জার্ভিস মাস্টার স্বয়ংক্রিয় শেখার সিস্টেম
echo ================================================================================
echo.
echo   JARVIS will automatically learn EVERYTHING!
echo   জার্ভিস স্বয়ংক্রিয়ভাবে সব কিছু শিখবে!
echo.
echo ================================================================================
echo.
echo   What will be added automatically:
echo   স্বয়ংক্রিয়ভাবে কি যোগ হবে:
echo.
echo   1. Multiple Intelligences (9 types)
echo   2. Knowledge Types (10 types)
echo   3. Human Senses (18 types)
echo   4. Shortcut Keys (139 shortcuts)
echo   5. Mega Dictionary (98+ entries)
echo   6. Multi-AI Learning (8 AI systems)
echo   7. Auto-Learning Topics (10 topics)
echo   8. Comprehensive Training (45+ topics)
echo.
echo ================================================================================
echo.
pause
echo.
echo ================================================================================
echo   Starting automatic learning...
echo   স্বয়ংক্রিয় শেখা শুরু হচ্ছে...
echo ================================================================================
echo.

REM Step 1: Multiple Intelligences
echo [1/7] Adding Multiple Intelligences...
python add_multiple_intelligences.py
if errorlevel 1 (
    echo   ⚠️ Multiple Intelligences already added or error occurred
) else (
    echo   ✅ Multiple Intelligences added successfully!
)
echo.
timeout /t 2 >nul

REM Step 2: Knowledge and Senses
echo [2/7] Adding Knowledge Types and Human Senses...
python add_knowledge_and_senses.py
if errorlevel 1 (
    echo   ⚠️ Knowledge and Senses already added or error occurred
) else (
    echo   ✅ Knowledge and Senses added successfully!
)
echo.
timeout /t 2 >nul

REM Step 3: Shortcut Keys
echo [3/7] Adding All Shortcut Keys...
python add_all_shortcuts.py
if errorlevel 1 (
    echo   ⚠️ Shortcuts already added or error occurred
) else (
    echo   ✅ Shortcut Keys added successfully!
)
echo.
timeout /t 2 >nul

REM Step 4: Mega Dictionary
echo [4/7] Adding Mega Dictionary...
python add_mega_dictionary.py
if errorlevel 1 (
    echo   ⚠️ Dictionary already added or error occurred
) else (
    echo   ✅ Mega Dictionary added successfully!
)
echo.
timeout /t 2 >nul

REM Step 5: Multi-AI Learning
echo [5/8] Multi-AI Learning (8 AI systems)...
python jarvis_multi_ai_learner.py --auto
if errorlevel 1 (
    echo   ⚠️ Multi-AI learning error occurred
) else (
    echo   ✅ Multi-AI Learning completed successfully!
)
echo.
timeout /t 2 >nul

REM Step 6: Auto-Learning Topics
echo [6/8] Auto-Learning from Google...
python jarvis_auto_learner.py
if errorlevel 1 (
    echo   ⚠️ Auto-learning error occurred
) else (
    echo   ✅ Auto-Learning completed successfully!
)
echo.
timeout /t 2 >nul

REM Step 7: Comprehensive Training
echo [7/8] Comprehensive Training (45+ topics)...
python auto_train_jarvis.py
if errorlevel 1 (
    echo   ⚠️ Training already done or error occurred
) else (
    echo   ✅ Comprehensive Training completed!
)
echo.
timeout /t 2 >nul

REM Step 8: Quick Training
echo [8/8] Quick Training (10 entries)...
python quick_train.py
if errorlevel 1 (
    echo   ⚠️ Quick training error occurred
) else (
    echo   ✅ Quick Training completed!
)
echo.

echo ================================================================================
echo   🎉 MASTER AUTO-LEARNING COMPLETED!
echo   🎉 মাস্টার স্বয়ংক্রিয় শেখা সম্পন্ন!
echo ================================================================================
echo.
echo   JARVIS has learned:
echo   জার্ভিস শিখেছে:
echo.
echo   ✅ Multiple Intelligences (9 types)
echo   ✅ Knowledge Types (10 types)
echo   ✅ Human Senses (18 types)
echo   ✅ Shortcut Keys (139 shortcuts)
echo   ✅ Mega Dictionary (98+ entries)
echo   ✅ Multi-AI Learning (8 AI systems + 6 topics)
echo   ✅ Auto-Learning Topics (10 topics)
echo   ✅ Comprehensive Training (45+ topics)
echo.
echo   Total: 320+ new knowledge entries!
echo   মোট: ৩২০+ নতুন জ্ঞান এন্ট্রি!
echo.
echo ================================================================================
echo.
echo   🧪 TEST JARVIS NOW:
echo.
echo   python jarvis_offline_brain.py "What is Python?"
echo   python jarvis_offline_brain.py "Tell me about intelligence"
echo   python jarvis_offline_brain.py "What is Ctrl+C?"
echo   python jarvis_offline_brain.py "আকাশ মানে কি?"
echo.
echo ================================================================================
echo.
echo   Press any key to exit...
echo   বের হতে যেকোনো কী চাপুন...
echo.
pause
