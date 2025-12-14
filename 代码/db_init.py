#!/usr/bin/env python
"""
数据库初始化脚本
用于创建数据库表结构和初始数据
"""

import os
import sys
import django
from pathlib import Path

# 添加项目根目录到Python路径
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reimbursement_system.settings')
django.setup()

from django.core.management import execute_from_command_line

def init_database():
    """初始化数据库"""
    print("正在初始化数据库...")

    # 运行数据库迁移
    print("1. 运行数据库迁移...")
    execute_from_command_line(['manage.py', 'migrate', '--verbosity=1'])

    # 创建初始数据（可选）
    print("2. 创建初始数据...")

    from users.models import User

    # 检查是否已有管理员账户
    if not User.objects.filter(is_superuser=True).exists():
        print("   创建默认管理员账户...")
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='管理员',
            role=User.Role.ADMIN
        )
        print("   默认管理员账户创建成功")
        print("   用户名: admin")
        print("   密码: admin123")
    else:
        print("   管理员账户已存在")

    print("数据库初始化完成！")

if __name__ == '__main__':
    init_database()
