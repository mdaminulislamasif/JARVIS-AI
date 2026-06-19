@echo off
echo ================================================================================
echo   CLEANING PYTHON CACHE
echo   PYTHON CACHE পরিষ্কার করা হচ্ছে
echo ================================================================================
echo.
echo This will delete Python cache files to ensure fixes take effect.
echo এটা Python cache files মুছে ফেলবে যাতে fixes কাজ করে।
echo.
echo Deleting cache directories...
echo Cache directories মুছে ফেলা হচ্ছে...
echo.

if exist "__pycache__" (
    echo Deleting: __pycache__
    rmdir /s /q "__pycache__"
    echo   ✅ Deleted
) else (
    echo   ⚠️ Not found: __pycache__
)

if exist "core\__pycache__" (
    echo Deleting: core\__pycache__
    rmdir /s /q "core\__pycache__"
    echo   ✅ Deleted
) else (
    echo   ⚠️ Not found: core\__pycache__
)

if exist "engine\__pycache__" (
    echo Deleting: engine\__pycache__
    rmdir /s /q "engine\__pycache__"
    echo   ✅ Deleted
) else (
    echo   ⚠️ Not found: engine\__pycache__
)

if exist "server\__pycache__" (
    echo Deleting: server\__pycache__
    rmdir /s /q "server\__pycache__"
    echo   ✅ Deleted
) else (
    echo   ⚠️ Not found: server\__pycache__
)

echo.
echo ================================================================================
echo   CACHE CLEANED!
echo   CACHE পরিষ্কার হয়ে গেছে!
echo ================================================================================
echo.
echo Now you can start JARVIS:
echo এখন আপনি JARVIS চালু করতে পারেন:
echo   - Double-click JARVIS.bat
echo   - OR START_JARVIS.bat
echo.
pause
