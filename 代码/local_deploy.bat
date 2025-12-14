@echo off
chcp 65001 >nul
echo ========================================
echo   报销神表 - 本地部署脚本
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] Python 未安装！
    echo 请先安装Python 3.9或更高版本
    echo 下载地址：https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [✓] Python 已安装
echo.

echo 正在安装项目依赖...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败！
    echo 请检查网络连接或尝试不使用镜像源
    echo.
    pause
    exit /b 1
)

echo [✓] 依赖安装成功
echo.

echo 正在配置MySQL数据库...
call mysql_setup.bat
if %errorlevel% neq 0 (
    echo [警告] MySQL配置可能有问题，请手动检查
    echo.
)

echo 正在初始化数据库...
python manage.py migrate
if %errorlevel% neq 0 (
    echo [错误] 数据库迁移失败！
    echo 请检查数据库配置和连接
    echo.
    pause
    exit /b 1
)

echo [✓] 数据库初始化成功
echo.

echo 正在创建管理员账户...
echo 请按提示输入管理员信息：
echo.
python create_admin.py

echo.
echo ========================================
echo   本地部署完成！
echo ========================================
echo.
echo 启动服务器命令：
echo python manage.py runserver 0.0.0.0:8000
echo.
echo 或运行 start_server.bat
echo.
pause
