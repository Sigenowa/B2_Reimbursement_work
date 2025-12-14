@echo off
chcp 65001 >nul
echo ========================================
echo   报销神表 - 服务器启动
echo ========================================
echo.

echo 正在获取本机IP地址...
echo.

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set ip=%%a
    set ip=!ip:~1!
    goto :found
)

:found
echo 您的IP地址: !ip!
echo.
echo ========================================
echo.
echo 服务器将在以下地址可用：
echo   本地访问: http://127.0.0.1:8000
echo   局域网访问: http://!ip!:8000
echo.
echo 其他设备可以通过 http://!ip!:8000 访问
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

python manage.py runserver 0.0.0.0:8000
