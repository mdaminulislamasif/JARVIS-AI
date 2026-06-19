@echo off
echo ================================================================================
echo   SETUP CHROME DEVTOOLS AUTOMATION
echo   Chrome DevTools অটোমেশন সেটআপ
echo ================================================================================
echo.

echo Step 1: Installing required packages...
echo ধাপ ১: প্রয়োজনীয় packages ইনস্টল করছি...
pip install selenium pyautogui
echo.

echo Step 2: Checking Chrome installation...
echo ধাপ ২: Chrome ইনস্টলেশন চেক করছি...
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    echo ✅ Chrome found!
    echo ✅ Chrome পাওয়া গেছে!
) else (
    echo ❌ Chrome not found!
    echo ❌ Chrome পাওয়া যায়নি!
    echo Please install Google Chrome first.
    echo প্রথমে Google Chrome ইনস্টল করুন।
)
echo.

echo Step 3: ChromeDriver information...
echo ধাপ ৩: ChromeDriver তথ্য...
echo.
echo ⚠️ IMPORTANT: You need to download ChromeDriver!
echo ⚠️ গুরুত্বপূর্ণ: আপনাকে ChromeDriver ডাউনলোড করতে হবে!
echo.
echo 1. Go to: https://chromedriver.chromium.org/downloads
echo 2. Download ChromeDriver matching your Chrome version
echo 3. Place chromedriver.exe in this folder
echo.
echo 1. যান: https://chromedriver.chromium.org/downloads
echo 2. আপনার Chrome version এর সাথে মিলে এমন ChromeDriver ডাউনলোড করুন
echo 3. chromedriver.exe এই folder এ রাখুন
echo.

echo Step 4: Opening ChromeDriver download page...
echo ধাপ ৪: ChromeDriver ডাউনলোড পেজ খুলছি...
start https://chromedriver.chromium.org/downloads
echo.

echo ================================================================================
echo   SETUP INSTRUCTIONS / সেটআপ নির্দেশাবলী
echo ================================================================================
echo.
echo After downloading ChromeDriver:
echo ChromeDriver ডাউনলোড করার পর:
echo.
echo 1. Extract chromedriver.exe
echo    chromedriver.exe extract করুন
echo.
echo 2. Place it in this folder (C:\Users\PHP\Desktop\ai)
echo    এই folder এ রাখুন (C:\Users\PHP\Desktop\ai)
echo.
echo 3. Run: python jarvis_chrome_devtools.py
echo    চালান: python jarvis_chrome_devtools.py
echo.
echo 4. Chrome will open with DevTools (Ctrl+Shift+I)!
echo    Chrome DevTools সহ খুলবে (Ctrl+Shift+I)!
echo.
echo ================================================================================
pause
