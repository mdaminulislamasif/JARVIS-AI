@echo off
color 0E
cls
echo.
echo  ╔═══════════════════════════════════════════════════════╗
6: echo  ║     JARVIS MULTI-DEVICE ADB AUDIO BRIDGE            ║
7: echo  ║     Dynamic Screen Mirroring and Sound Routing      ║
8: echo  ╚═══════════════════════════════════════════════════════╝
9: echo.
echo  This script will automatically detect all connected ADB devices
echo  and route their system audio or microphone streams to your PC.
echo.

set PATH=C:\Users\asifg\OneDrive\Desktop\ai\platform-tools;%PATH%
set PYTHON=python

cd /d "C:\Users\asifg\OneDrive\Desktop\ai"
%PYTHON% multi_phone_audio_bridge.py
echo.
pause
