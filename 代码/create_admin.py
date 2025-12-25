#!/usr/bin/env python
"""
创建初始管理员账户的脚本
使用方法: python create_admin.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reimbursement_system.settings')
django.setup()

from users.models import User

def create_admin():
    """创建管理员账户"""
    print("=" * 50)
    print("报销神表 - 管理员账户创建工具")
    print("=" * 50)
    
    # 检查是否已存在管理员
    if User.objects.filter(role=User.Role.ADMIN).exists():
        print("已存在管理员账户:")
        for admin in User.objects.filter(role=User.Role.ADMIN):
            print(f"  - {admin.username}")
        
        create_new = input("\n是否创建新的管理员？(y/n): ").strip().lower()
        if create_new != 'y':
            print("已取消")
            return
    
    # 获取管理员信息
    print("\n请输入管理员信息:")
    username = input("用户名: ").strip()
    
    if User.objects.filter(username=username).exists():
        print(f"用户名 '{username}' 已存在！")
        return
    
    password = input("密码: ").strip()
    first_name = input("姓名: ").strip()
    email = input("邮箱 (可选): ").strip()
    student_id = input("学号: ").strip()
    department = input("部门 (默认: 学生会): ").strip() or "学生会"
    
    # 创建管理员
    admin = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        email=email,
        student_id=student_id,
        department=department,
        college="环境学院",
        role=User.Role.ADMIN,
        is_staff=True,
        is_superuser=True
    )
    
    print("\n" + "=" * 50)
    print("✅ 管理员创建成功！")
    print(f"   用户名: {admin.username}")
    print(f"   角色: {admin.get_role_display()}")
    print("=" * 50)
    print("\n您可以通过以下地址访问系统:")
    print("  本地: http://127.0.0.1:8000")
    print("  服务器: http://101.43.149.245")

if __name__ == '__main__':
    create_admin()





