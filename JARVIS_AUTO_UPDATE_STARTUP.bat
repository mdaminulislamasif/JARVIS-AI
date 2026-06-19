@echo off
REM JARVIS Auto-Updater - Runs on Windows Startup
REM জার্ভিস স্বয়ংক্রিয় আপডেটার - Windows চালু হলে চলে

cd /d "%~dp0"

REM Run auto-updater once
python jarvis_auto_updater.py

REM Exit silently
exit
