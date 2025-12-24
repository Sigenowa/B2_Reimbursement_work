-- MySQL数据库初始化脚本
-- 在MySQL中执行此脚本创建数据库和用户

-- 创建数据库
CREATE DATABASE IF NOT EXISTS reimbursement_db 
    DEFAULT CHARACTER SET utf8mb4 
    DEFAULT COLLATE utf8mb4_unicode_ci;

-- 创建用户（修改密码！）
CREATE USER IF NOT EXISTS 'reimbursement_user'@'localhost' 
    IDENTIFIED BY 'your-secure-password-here';

-- 授予权限
GRANT ALL PRIVILEGES ON reimbursement_db.* 
    TO 'reimbursement_user'@'localhost';

-- 刷新权限
FLUSH PRIVILEGES;

-- 验证
SHOW DATABASES LIKE 'reimbursement_db';
SELECT User, Host FROM mysql.user WHERE User = 'reimbursement_user';





