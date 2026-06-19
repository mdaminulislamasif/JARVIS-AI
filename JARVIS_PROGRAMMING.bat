@echo off
title JARVIS PROGRAMMING MASTER
color 0E

cls
echo ========================================
echo    JARVIS PROGRAMMING MASTER
echo    Knows ALL Programming Languages
echo ========================================
echo.
echo JARVIS knows 30+ programming languages:
echo  * Popular: Python, JavaScript, Java, C++, etc.
echo  * Windows: C#, PowerShell, Visual Basic, etc.
echo  * Classic: COBOL, Fortran, Pascal, Lisp, etc.
echo  * Niche: Haskell, Scala, Dart, etc.
echo.
echo ========================================
echo.

echo Installing packages...
pip install SpeechRecognition pyttsx3 pyaudio --quiet

echo.
echo Starting JARVIS Programming Master...
echo.

python jarvis_programming_master.py

pause
