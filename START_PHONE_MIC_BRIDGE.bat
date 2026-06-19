@echo off
color 0B
cls
echo.
echo  ╔═══════════════════════════════════════════════════════╗
echo  ║     JARVIS PHONE AUDIO BRIDGE - ATOM 5 SETUP          ║
echo  ║     Phone Mic ^-^> PC   ^|   Phone Audio ^-^> PC Speakers   ║
echo  ╚═══════════════════════════════════════════════════════╝
echo.
echo  What this does:
echo  -------------------------------------------------------
echo  [1] Routes your ATOM 5 phone's MICROPHONE to your PC
echo      So JARVIS can hear you through your PHONE'S mic
echo.
echo  [2] Routes your ATOM 5 phone's AUDIO to your PC SPEAKERS
echo      So your phone's sound plays on your PC speakers
echo  -------------------------------------------------------
echo.

set ADB=C:\Users\asifg\OneDrive\Desktop\ai\platform-tools\adb.exe
set SCRCPY=C:\Users\asifg\OneDrive\Desktop\ai\scrcpy\scrcpy-win64-v2.4\scrcpy.exe
set PYTHON=python
set PATH=C:\Users\asifg\OneDrive\Desktop\ai\platform-tools;%PATH%

echo  Checking phone connection...
"%ADB%" devices
echo.

echo  Granting microphone permission to scrcpy on phone...
"%ADB%" -s BD354558452086043 shell pm grant com.genymobile.scrcpy android.permission.RECORD_AUDIO
echo.

echo  Boosting phone mic and speaker volume...
"%ADB%" -s BD354558452086043 shell media volume --stream 0 --set 15 2>nul
"%ADB%" -s BD354558452086043 shell "for i in 1 2 3 4 5 6 7 8 9 10; do input keyevent 24; done"
echo.

echo  -------------------------------------------------------
echo  Starting Phone SYSTEM AUDIO ^-^> PC Speakers...
echo  (Your phone's music/calls will play on PC)
echo  -------------------------------------------------------
start "PHONE AUDIO" "%SCRCPY%" -s BD354558452086043 --audio-source=output --window-title "ATOM 5 Audio" --always-on-top --turn-screen-off --stay-awake
timeout /t 3 /nobreak >nul

echo.
echo  -------------------------------------------------------  
echo  Starting Phone MICROPHONE ^-^> PC...
echo  (JARVIS will hear you through your phone's mic)
echo  -------------------------------------------------------
start "PHONE MIC" "%SCRCPY%" -s BD354558452086043 --audio-source=mic --no-video --window-title "PHONE MIC ACTIVE"
timeout /t 2 /nobreak >nul

echo.
echo  -------------------------------------------------------
echo  Saving mic config for JARVIS...
echo  -------------------------------------------------------
%PYTHON% -c "import json; data={'phone_mic_index': 5, 'serial': 'BD354558452086043', 'active': True}; json.dump(data, open('jarvis_mic_config.json','w'), indent=2); print('[OK] Config saved')"

echo.
echo  ╔═══════════════════════════════════════════════════════╗
echo  ║  AUDIO BRIDGE IS NOW ACTIVE!                          ║
echo  ║                                                        ║
echo  ║  Phone Mic    ---^>  PC Input  (JARVIS listens)        ║
echo  ║  Phone Audio  ---^>  PC Speakers (phone sounds play)  ║
echo  ║                                                        ║
echo  ║  Now start JARVIS - it will use your phone mic!        ║
echo  ╚═══════════════════════════════════════════════════════╝
echo.
echo  Press any key to also start JARVIS Conversational AI...
pause >nul

%PYTHON% C:\Users\asifg\OneDrive\Desktop\ai\jarvis_conversational.py
