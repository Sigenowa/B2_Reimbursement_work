@echo off
chcp 65001 >nul
echo ========================================
echo   MySQL 数据库配置脚本
echo ========================================
echo.

echo 正在检查MySQL是否已安装...
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] MySQL 未安装！
    echo 请先安装MySQL：
    echo 1. 下载：https://dev.mysql.com/downloads/mysql/
    echo 2. 安装时选择 "Developer Default"
    echo 3. 记住设置的root密码
    echo.
    pause
    exit /b 1
)

echo [✓] MySQL 已安装
echo.

echo 正在连接MySQL数据库...
echo 请注意：如果连接失败，请检查：
echo 1. MySQL服务是否正在运行
echo 2. root密码是否正确
echo 3. 防火墙是否阻止了连接
echo.

mysql -u root -p -e "SELECT VERSION();" >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 无法连接到MySQL！
    echo 请检查MySQL服务状态和密码。
    echo.
    echo 启动MySQL服务命令：
    echo net start mysql
    echo.
    pause
    exit /b 1
)

echo [✓] MySQL连接成功
echo.

echo 正在创建数据库和用户...
mysql -u root -p -e "
CREATE DATABASE IF NOT EXISTS reimbursement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'reimbursement_user'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON reimbursement_db.* TO 'reimbursement_user'@'localhost';
FLUSH PRIVILEGES;
SHOW DATABASES;
" >nul 2>&1

if %errorlevel% neq 0 (
    echo [错误] 数据库创建失败！
    echo 请手动运行以下SQL命令：
    echo.
    echo mysql -u root -p
    echo.
    echo CREATE DATABASE reimbursement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    echo CREATE USER 'reimbursement_user'@'localhost' IDENTIFIED BY 'password123';
    echo GRANT ALL PRIVILEGES ON reimbursement_db.* TO 'reimbursement_user'@'localhost';
    echo FLUSH PRIVILEGES;
    echo.
    pause
    exit /b 1
)

echo [✓] 数据库创建成功
echo.
echo 数据库信息：
echo 数据库名：reimbursement_db
echo 用户名：reimbursement_user
echo 密码：password123
echo 主机：localhost
echo 端口：3306
echo.

echo 正在测试数据库连接...
mysql -u reimbursement_user -ppassword123 -e "USE reimbursement_db; SELECT DATABASE();" >nul 2>&1

if %errorlevel% neq 0 (
    echo [错误] 数据库连接测试失败！
    pause
    exit /b 1
)

echo [✓] 数据库连接测试成功
echo.

echo ========================================
echo   MySQL配置完成！
echo ========================================
echo.
echo 接下来运行：
echo python manage.py migrate
echo.
pause
