#!/bin/bash
# 快速启动脚本（开发/测试用）
# 使用方法: bash quick_start.sh

echo "=========================================="
echo "报销神表 - 快速启动"
echo "=========================================="

# 设置环境变量
export USE_SQLITE=true
export DEBUG=true

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 创建必要目录
mkdir -p media
mkdir -p staticfiles
mkdir -p logs

# 数据库迁移
echo "执行数据库迁移..."
python manage.py migrate

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 检查是否需要创建管理员
if ! python -c "import django; django.setup(); from users.models import User; exit(0 if User.objects.filter(role='ADMIN').exists() else 1)" 2>/dev/null; then
    echo ""
    echo "未检测到管理员账户，是否创建？(y/n)"
    read create_admin
    if [ "$create_admin" = "y" ]; then
        python create_admin.py
    fi
fi

echo ""
echo "=========================================="
echo "启动开发服务器..."
echo "访问地址: http://127.0.0.1:8000"
echo "外部访问: http://101.43.149.245:8000"
echo "按 Ctrl+C 停止服务器"
echo "=========================================="

# 启动服务器，监听所有地址
python manage.py runserver 0.0.0.0:8000





