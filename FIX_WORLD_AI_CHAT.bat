@echo off
chcp 65001 >nul
echo ================================================================
echo 🔧 WORLD AI CHAT FIX
echo ================================================================
echo.

echo Step 1: Testing World AI Chat...
python TEST_WORLD_AI_CHAT_DEBUG.py
echo.

echo Step 2: Running fix script...
python FIX_WORLD_AI_CHAT.py
echo.

echo ================================================================
echo ✅ FIX COMPLETE
echo ================================================================
echo.
echo Now you can use World AI Chat from JARVIS panel!
echo এখন JARVIS panel থেকে World AI Chat ব্যবহার করতে পারবেন!
echo.
echo To start JARVIS:
echo    python jarvis_panel.py
echo.
pause
