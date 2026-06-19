@echo off
title JARVIS COMPLETE SETUP
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          🚀 JARVIS COMPLETE SYSTEM SETUP 🚀                       ║
echo ║                                                                  ║
echo ║        🚀 JARVIS সম্পূর্ণ সিস্টেম সেটআপ 🚀                       ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo This will setup JARVIS to be fully self-sufficient!
echo এটি JARVIS কে সম্পূর্ণভাবে self-sufficient করবে!
echo.
echo What will be done:
echo কি করা হবে:
echo   ✅ Install all dependencies
echo   ✅ Download required files
echo   ✅ Setup offline capabilities
echo   ✅ Connect to online resources
echo   ✅ Verify installation
echo.
pause

echo.
echo ═══════════════════════════════════════════════════════════════════
echo STEP 1: Running Complete System Setup
echo ধাপ ১: সম্পূর্ণ সিস্টেম সেটআপ চালাচ্ছি
echo ═══════════════════════════════════════════════════════════════════
echo.
python jarvis_complete_system.py setup

echo.
echo ═══════════════════════════════════════════════════════════════════
echo STEP 2: Downloading Everything
echo ধাপ ২: সব কিছু ডাউনলোড করছি
echo ═══════════════════════════════════════════════════════════════════
echo.
python jarvis_complete_system.py download

echo.
echo ═══════════════════════════════════════════════════════════════════
echo STEP 3: Checking Online Connections
echo ধাপ ৩: অনলাইন সংযোগ চেক করছি
echo ═══════════════════════════════════════════════════════════════════
echo.
python jarvis_complete_system.py connect

echo.
echo ═══════════════════════════════════════════════════════════════════
echo STEP 4: Verifying Installation
echo ধাপ ৪: ইনস্টলেশন যাচাই করছি
echo ═══════════════════════════════════════════════════════════════════
echo.
python jarvis_complete_system.py status

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║          ✅ JARVIS COMPLETE SETUP FINISHED! ✅                    ║
echo ║                                                                  ║
echo ║        ✅ JARVIS সম্পূর্ণ সেটআপ শেষ! ✅                          ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo JARVIS is now fully self-sufficient and connected!
echo JARVIS এখন সম্পূর্ণভাবে self-sufficient এবং connected!
echo.
echo You can now run JARVIS:
echo আপনি এখন JARVIS চালাতে পারেন:
echo   python jarvis_panel.py
echo.
pause
