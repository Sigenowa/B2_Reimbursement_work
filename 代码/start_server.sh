#!/bin/bash
# Linux/Mac 启动脚本（允许外部访问）

echo "========================================"
echo "  报销神表 - 服务器启动"
echo "========================================"
echo ""

# 获取IP地址
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -n1 | awk '{print $2}')
else
    # Linux
    IP=$(hostname -I | awk '{print $1}')
fi

echo "服务器将在以下地址可用："
echo "  本地访问: http://127.0.0.1:8000"
echo "  局域网访问: http://$IP:8000"
echo ""
echo "其他设备可以通过 http://$IP:8000 访问"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "========================================"
echo ""

python3 manage.py runserver 0.0.0.0:8000
