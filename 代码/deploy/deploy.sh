#!/bin/bash
# 服务器部署脚本
# 服务器: ubuntu@101.43.149.245
# 使用方法: bash deploy.sh

set -e  # 遇到错误立即退出

echo "=========================================="
echo "报销神表 - 服务器部署脚本"
echo "服务器: 101.43.149.245"
echo "=========================================="

# 配置变量
PROJECT_DIR="/home/ubuntu/reimbursement"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON="$VENV_DIR/bin/python"
PIP="$VENV_DIR/bin/pip"

# 1. 创建项目目录
echo ""
echo "[1/8] 创建项目目录..."
sudo mkdir -p $PROJECT_DIR
sudo chown ubuntu:ubuntu $PROJECT_DIR
cd $PROJECT_DIR

# 2. 创建Python虚拟环境
echo ""
echo "[2/8] 创建Python虚拟环境..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv $VENV_DIR
fi

# 3. 安装Python依赖
echo ""
echo "[3/8] 安装Python依赖..."
$PIP install --upgrade pip
$PIP install -r requirements.txt

# 4. 创建必要目录
echo ""
echo "[4/8] 创建必要目录..."
mkdir -p media
mkdir -p staticfiles
mkdir -p logs
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown ubuntu:ubuntu /var/log/gunicorn
sudo chown ubuntu:ubuntu /var/run/gunicorn

# 5. 配置环境变量
echo ""
echo "[5/8] 配置环境变量..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "请编辑 .env 文件配置数据库和密钥"
fi

# 6. 数据库迁移
echo ""
echo "[6/8] 执行数据库迁移..."
$PYTHON manage.py migrate

# 7. 收集静态文件
echo ""
echo "[7/8] 收集静态文件..."
$PYTHON manage.py collectstatic --noinput

# 8. 配置systemd服务
echo ""
echo "[8/8] 配置systemd服务..."
sudo cp deploy/reimbursement.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable reimbursement
sudo systemctl restart reimbursement

# 配置Nginx
echo ""
echo "配置Nginx..."
sudo cp deploy/nginx.conf /etc/nginx/sites-available/reimbursement
sudo ln -sf /etc/nginx/sites-available/reimbursement /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

echo ""
echo "=========================================="
echo "✅ 部署完成！"
echo ""
echo "访问地址: http://101.43.149.245"
echo ""
echo "常用命令:"
echo "  查看服务状态: sudo systemctl status reimbursement"
echo "  重启服务: sudo systemctl restart reimbursement"
echo "  查看日志: sudo journalctl -u reimbursement -f"
echo "=========================================="





