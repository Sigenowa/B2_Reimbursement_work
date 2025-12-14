#!/bin/bash
# 本地部署脚本 - Linux/Mac系统

set -e  # 遇到错误立即退出

echo "=========================================="
echo "  报销神表 - 本地部署脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Python
echo -e "${YELLOW}步骤1: 检查Python环境...${NC}"
python3 --version
if [ $? -ne 0 ]; then
    echo -e "${RED}错误: Python3 未安装！${NC}"
    echo "请先安装Python 3.9或更高版本"
    exit 1
fi
echo -e "${GREEN}✓ Python 已安装${NC}"
echo ""

# 安装依赖
echo -e "${YELLOW}步骤2: 安装项目依赖...${NC}"
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if [ $? -ne 0 ]; then
    echo -e "${RED}错误: 依赖安装失败！${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 依赖安装成功${NC}"
echo ""

# 检查MySQL
echo -e "${YELLOW}步骤3: 检查MySQL...${NC}"
mysql --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}错误: MySQL 未安装！${NC}"
    echo "请先安装MySQL："
    echo "Ubuntu/Debian: sudo apt install mysql-server"
    echo "macOS: brew install mysql"
    exit 1
fi
echo -e "${GREEN}✓ MySQL 已安装${NC}"
echo ""

# 创建数据库
echo -e "${YELLOW}步骤4: 创建数据库...${NC}"
mysql -u root -p -e "
CREATE DATABASE IF NOT EXISTS reimbursement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'reimbursement_user'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON reimbursement_db.* TO 'reimbursement_user'@'localhost';
FLUSH PRIVILEGES;
" 2>/dev/null || {
    echo -e "${YELLOW}请手动输入MySQL root密码来创建数据库：${NC}"
    mysql -u root -p -e "
    CREATE DATABASE IF NOT EXISTS reimbursement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    CREATE USER IF NOT EXISTS 'reimbursement_user'@'localhost' IDENTIFIED BY 'password123';
    GRANT ALL PRIVILEGES ON reimbursement_db.* TO 'reimbursement_user'@'localhost';
    FLUSH PRIVILEGES;
    "
}

if [ $? -ne 0 ]; then
    echo -e "${RED}数据库创建失败！${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 数据库创建成功${NC}"
echo ""

# 初始化数据库
echo -e "${YELLOW}步骤5: 初始化数据库...${NC}"
python3 manage.py migrate
if [ $? -ne 0 ]; then
    echo -e "${RED}数据库迁移失败！${NC}"
    exit 1
fi
echo -e "${GREEN}✓ 数据库初始化成功${NC}"
echo ""

# 创建管理员
echo -e "${YELLOW}步骤6: 创建管理员账户...${NC}"
echo "请选择创建管理员的方式："
echo "1. 使用脚本创建（推荐）"
echo "2. 手动创建"
read -p "请选择 (1/2): " choice

if [ "$choice" = "1" ]; then
    python3 create_admin.py
elif [ "$choice" = "2" ]; then
    python3 manage.py createsuperuser
else
    echo "无效选择，使用默认脚本创建"
    python3 create_admin.py
fi

echo ""
echo "=========================================="
echo "  本地部署完成！"
echo "=========================================="
echo ""
echo "启动服务器："
echo "python3 manage.py runserver 0.0.0.0:8000"
echo ""
echo "或运行："
echo "./start_server.sh"
echo ""
