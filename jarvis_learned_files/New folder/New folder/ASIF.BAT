@echo off
setlocal enabledelayedexpansion
color 02
title ASIF GK HACKER EDITION - asifgk.hacker@gmail.com

:menu
cls
echo ==========================================================
echo               ASIF GK HACKER EDITION
echo       Contact: asifgk.hacker@gmail.com
echo       Admin: %USERNAME% ^| Date: %DATE%
echo ==========================================================
echo  [1] Generate Random Passwords (PASS.TEXT)
echo  [2] Generate Phone Numbers (PHONENUMBER.TEXT)
echo  [3] Generate Numbers (NUMBER.TEXT)
echo  [4] Exit
echo ==========================================================
set /p "choice=Select option [1-4]: "

if "%choice%"=="1" goto password
if "%choice%"=="2" goto phone
if "%choice%"=="3" goto 8digit
if "%choice%"=="4" exit
goto menu

:password
cls
echo [ RANDOM PASSWORD GENERATOR ]
set /p "count=Kota password lagbe?: "
set /p "len=Password doirgho (length)?: "
set "char=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$%^&*"

set "charCount=0"
set "temp=%char%"
:loop_count
if defined temp (set "temp=%temp:~1%" & set /a charCount+=1 & goto loop_count)

echo Log by Admin: %USERNAME% on %DATE% %TIME% > PASS.TEXT
echo ------------------------------------------- >> PASS.TEXT

for /l %%k in (1, 1, %count%) do (
    set "pass="
    for /l %%i in (1, 1, %len%) do (
        set /a "rand=!random! %% %charCount%"
        for /f "delims=" %%j in ("!rand!") do (set "pass=!pass!!char:~%%j,1!")
    )
    echo [!TIME!] PASS: !pass!
    echo !pass! >> PASS.TEXT
)
echo ------------------------------
echo Done! Saved to PASS.TEXT
pause
goto menu

:phone
cls
echo [ PHONE NUMBER GENERATOR (7-DIGIT) ]
set /p "startNumber=Start number?: "
set /p "count=How many?: "
set "prefix=%startNumber:~0,-7%"
set "suffix=%startNumber:~-7%"

echo Log by Admin: %USERNAME% on %DATE% %TIME% > PHONENUMBER.TEXT
echo ------------------------------------------- >> PHONENUMBER.TEXT

for /l %%i in (1, 1, %count%) do (
    set /a "suffix+=1"
    set "padded=0000000!suffix!"
    set "padded=!padded:~-7!"
    echo [!TIME!] PHONE: !prefix!!padded!
    echo !prefix!!padded! >> PHONENUMBER.TEXT
)
echo ------------------------------
echo Done! Saved to PHONENUMBER.TEXT
pause
goto menu

:8digit
cls
echo [ 8-DIGIT NUMBER GENERATOR ]
set /p "startNumber=Start number?: "
set /p "count=How many?: "
set "prefix=%startNumber:~0,-8%"
set "suffix=%startNumber:~-8%"

echo Log by Admin: %USERNAME% on %DATE% %TIME% > NUMBER.TEXT
echo ------------------------------------------- >> NUMBER.TEXT

for /l %%i in (1, 1, %count%) do (
    set /a "suffix+=1"
    set "padded=00000000!suffix!"
    set "padded=!padded:~-8!"
    echo [!TIME!] NUMBER: !prefix!!padded!
    echo !prefix!!padded! >> NUMBER.TEXT
)
echo ------------------------------
echo Done! Saved to NUMBER.TEXT
pause
goto menu
