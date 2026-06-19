@echo off
title TEST OFFLINE COMMANDS
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║              TESTING OFFLINE BRAIN COMMANDS                      ║
echo ║          অফলাইন ব্রেইন কমান্ড পরীক্ষা                            ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo Testing various commands with offline brain...
echo অফলাইন ব্রেইন দিয়ে বিভিন্ন কমান্ড পরীক্ষা করছি...
echo.

echo ═══════════════════════════════════════════════════════════════════
echo TEST 1: Name Question (Bengali)
echo পরীক্ষা ১: নাম জিজ্ঞাসা (বাংলা)
echo ═══════════════════════════════════════════════════════════════════
python -c "from jarvis_offline_brain import OfflineBrain; brain = OfflineBrain(); result = brain.process_command('TOMR NAM KI'); print(result['response'])"
echo.
pause

echo ═══════════════════════════════════════════════════════════════════
echo TEST 2: Create PC Boost Panel
echo পরীক্ষা ২: PC Boost Panel তৈরি
echo ═══════════════════════════════════════════════════════════════════
python -c "from jarvis_offline_brain import OfflineBrain; brain = OfflineBrain(); result = brain.process_command('CREATE PC BOOST PANEL'); print(result['response'])"
echo.
pause

echo ═══════════════════════════════════════════════════════════════════
echo TEST 3: Create Flashlight Application
echo পরীক্ষা ৩: Flashlight Application তৈরি
echo ═══════════════════════════════════════════════════════════════════
python -c "from jarvis_offline_brain import OfflineBrain; brain = OfflineBrain(); result = brain.process_command('CREATE FLASH LITE APPLICATION'); print(result['response'])"
echo.
pause

echo ═══════════════════════════════════════════════════════════════════
echo TEST 4: Location Question (Bengali)
echo পরীক্ষা ৪: অবস্থান জিজ্ঞাসা (বাংলা)
echo ═══════════════════════════════════════════════════════════════════
python -c "from jarvis_offline_brain import OfflineBrain; brain = OfflineBrain(); result = brain.process_command('INDIA TA KOLKATA KOTHI OBOSTITO'); print(result['response'])"
echo.
pause

echo ═══════════════════════════════════════════════════════════════════
echo TEST 5: Greeting
echo পরীক্ষা ৫: শুভেচ্ছা
echo ═══════════════════════════════════════════════════════════════════
python -c "from jarvis_offline_brain import OfflineBrain; brain = OfflineBrain(); result = brain.process_command('HI'); print(result['response'])"
echo.
pause

echo.
echo ═══════════════════════════════════════════════════════════════════
echo All tests complete!
echo সব পরীক্ষা সম্পূর্ণ!
echo ═══════════════════════════════════════════════════════════════════
echo.
pause
