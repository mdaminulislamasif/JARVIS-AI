@echo off
echo ================================================================================
echo   BUILDING PORTABLE JARVIS.EXE
echo   পোর্টেবল JARVIS.exe তৈরি করা হচ্ছে
echo ================================================================================
echo.

echo [1/3] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo     Done

echo.
echo [2/3] Building JARVIS.exe with PyInstaller...
pyinstaller --clean --onefile --console jarvis_launcher.py --name JARVIS
echo     Done

echo.
echo [3/3] Creating portable package...
if not exist "JARVIS_Portable" mkdir "JARVIS_Portable"
copy dist\JARVIS.exe "JARVIS_Portable\"
xcopy /E /I /Y core "JARVIS_Portable\core"
xcopy /E /I /Y engine "JARVIS_Portable\engine"
copy jarvis_memory.db.fixed-* "JARVIS_Portable\jarvis_memory.db" 2>nul
copy jarvis_config.txt "JARVIS_Portable\" 2>nul
echo     Done

echo.
echo ================================================================================
echo   BUILD COMPLETE!
echo   তৈরি সম্পন্ন!
echo ================================================================================
echo.
echo Portable JARVIS created in: JARVIS_Portable\
echo.
echo You can now:
echo   1. Copy the entire JARVIS_Portable folder to any Windows computer
echo   2. Run JARVIS.exe
echo   3. No installation needed!
echo.
echo আপনি এখন:
echo   1. JARVIS_Portable ফোল্ডারটি যেকোনো Windows কম্পিউটারে কপি করুন
echo   2. JARVIS.exe চালান
echo   3. কোনো ইনস্টলেশন লাগবে না!
echo.
pause
