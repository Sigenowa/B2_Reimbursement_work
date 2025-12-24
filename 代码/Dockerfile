# Dockerfile - 构建报销系统 Django 应用镜像
# 使用方法: docker build -t reimbursement-app .

# 基础镜像：Python 3.12 精简版
FROM python:3.12-slim

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 设置工作目录
WORKDIR /app

# 安装系统依赖（MySQL 客户端、编译工具等）
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 创建必要的目录
RUN mkdir -p logs media staticfiles

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 8000

# 默认启动命令（使用 gunicorn 生产级服务器）
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "reimbursement_system.wsgi:application"]

