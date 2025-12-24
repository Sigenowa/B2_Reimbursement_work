#!/bin/bash
# docker-deploy.sh - Docker 一键部署脚本
# 使用方法: chmod +x docker-deploy.sh && ./docker-deploy.sh

set -e

echo "=========================================="
echo "   报销系统 Docker 部署脚本"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Docker 是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Docker 未安装，正在安装...${NC}"
        sudo apt-get update
        sudo apt-get install -y docker.io docker-compose
        sudo systemctl start docker
        sudo systemctl enable docker
        sudo usermod -aG docker $USER
        echo -e "${YELLOW}Docker 已安装，请重新登录后再运行此脚本${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker 已安装${NC}"
}

# 检查 docker-compose 是否安装
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}docker-compose 未安装，正在安装...${NC}"
        sudo apt-get install -y docker-compose
    fi
    echo -e "${GREEN}✓ docker-compose 已安装${NC}"
}

# 创建必要目录
create_dirs() {
    echo "创建必要目录..."
    mkdir -p logs media
    echo -e "${GREEN}✓ 目录创建完成${NC}"
}

# 启动服务
start_services() {
    echo ""
    echo "=========================================="
    echo "   启动 Docker 容器"
    echo "=========================================="
    
    # 构建并启动
    docker-compose up -d --build
    
    echo ""
    echo -e "${GREEN}✓ 服务启动完成！${NC}"
}

# 等待数据库就绪
wait_for_db() {
    echo "等待数据库就绪..."
    sleep 10
    echo -e "${GREEN}✓ 数据库已就绪${NC}"
}

# 创建管理员账号
create_admin() {
    echo ""
    echo "=========================================="
    echo "   创建管理员账号"
    echo "=========================================="
    echo -e "${YELLOW}请输入管理员信息：${NC}"
    docker-compose exec web python manage.py createsuperuser
}

# 显示状态
show_status() {
    echo ""
    echo "=========================================="
    echo "   服务状态"
    echo "=========================================="
    docker-compose ps
    
    echo ""
    echo "=========================================="
    echo -e "${GREEN}   部署完成！${NC}"
    echo "=========================================="
    echo ""
    echo "访问地址："
    echo "  - 网站首页: http://$(curl -s ifconfig.me 2>/dev/null || echo 'your-server-ip'):8000"
    echo "  - 管理后台: http://$(curl -s ifconfig.me 2>/dev/null || echo 'your-server-ip'):8000/admin/"
    echo ""
    echo "常用命令："
    echo "  - 查看日志: docker-compose logs -f"
    echo "  - 停止服务: docker-compose down"
    echo "  - 重启服务: docker-compose restart"
    echo "  - 更新部署: docker-compose up -d --build"
    echo ""
}

# 主流程
main() {
    check_docker
    check_docker_compose
    create_dirs
    start_services
    wait_for_db
    
    echo ""
    read -p "是否现在创建管理员账号？(y/n): " create_admin_choice
    if [[ $create_admin_choice == "y" || $create_admin_choice == "Y" ]]; then
        create_admin
    fi
    
    show_status
}

# 运行
main

