#!/bin/bash
# Linux/Mac 启动脚本（允许外部访问）

echo "========================================"
echo "  报销神表 - 服务器启动"
echo "========================================"
echo ""
echo "正在启动服务器..."
echo ""
echo "服务器将在以下地址可用："
echo "  本地访问: http://127.0.0.1:8000"
echo "  局域网访问: http://$(hostname -I | awk '{print $1}'):8000"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "========================================"
echo ""

python manage.py runserver 0.0.0.0:8000




