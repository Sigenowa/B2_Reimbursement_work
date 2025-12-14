@echo off
echo ========================================
echo   获取本机IP地址
echo ========================================
echo.
echo 正在获取您的IP地址...
echo.

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set ip=%%a
    set ip=!ip:~1!
    echo 您的IP地址: !ip!
    echo.
    echo 其他人可以通过以下地址访问：
    echo   http://!ip!:8000
    echo.
    goto :found
)

:found
echo ========================================
pause




