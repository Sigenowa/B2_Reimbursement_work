"""
创建初始管理员账户的脚本
首次部署时使用此脚本创建第一个系统管理员账户
使用方法: python create_admin.py
"""
import os
import django

# 设置Django环境变量，使脚本可以独立运行
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reimbursement_system.settings')
django.setup()

from users.models import User

def create_admin():
    """
    交互式创建管理员账户
    提示用户输入管理员信息，创建后角色自动设置为系统管理员
    """
    username = input("请输入管理员用户名: ")
    email = input("请输入邮箱: ")
    password = input("请输入密码: ")
    first_name = input("请输入姓名: ")
    student_id = input("请输入学号: ")
    department = input("请输入部门 (如: 文艺部): ")
    
    # 检查用户名是否已存在
    if User.objects.filter(username=username).exists():
        print(f"用户名 {username} 已存在！")
        return
    
    # 创建管理员用户
    # 使用create_user方法会自动对密码进行哈希处理
    admin = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        student_id=student_id,
        college='环境学院',  # 默认学院
        department=department,
        role=User.Role.ADMIN  # 设置为系统管理员角色
    )
    print(f"\n管理员账户创建成功！")
    print(f"用户名: {admin.username}")
    print(f"角色: {admin.get_role_display()}")

if __name__ == '__main__':
    create_admin()
