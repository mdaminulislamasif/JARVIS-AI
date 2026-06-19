@echo off
echo ================================================================
echo    Personal Data Checker - Before GitHub Upload
echo ================================================================
echo.
echo Checking your project for sensitive information...
echo.

python CHECK_PERSONAL_DATA.py

echo.
echo ================================================================
echo    Check Complete!
echo ================================================================
echo.
echo If no issues found, you can safely upload to GitHub.
echo.
echo Next step:
echo   Double-click: SECURE_UPLOAD_TO_GITHUB.bat
echo.
pause
