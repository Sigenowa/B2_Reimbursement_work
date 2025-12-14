from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import RegisterForm, ProfileEditForm, PasswordChangeForm
from .models import User

def register(request):
    """
    用户注册视图
    处理新用户注册，注册成功后自动登录
    所有新用户默认角色为普通用户，由管理员后续分配角色
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 保存用户并自动登录
            user = form.save()
            login(request, user)
            messages.success(request, f'注册成功！欢迎 {user.first_name or user.username}')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_edit(request):
    """
    个人信息编辑视图
    用户可以修改自己的基本信息（姓名、邮箱、学号、学院、部门）
    同时支持修改密码功能
    """
    if request.method == 'POST':
        # 处理基本信息修改
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '个人信息已更新')
            return redirect('profile_edit')
    else:
        form = ProfileEditForm(instance=request.user)
    
    # 密码修改表单
    password_form = PasswordChangeForm(user=request.user)
    
    # 处理密码修改请求
    if request.method == 'POST' and 'change_password' in request.POST:
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            # 更新session，避免密码修改后需要重新登录
            update_session_auth_hash(request, request.user)
            messages.success(request, '密码已修改')
            return redirect('profile_edit')
    
    return render(request, 'users/profile_edit.html', {
        'form': form,
        'password_form': password_form
    })

@login_required
def user_management(request):
    """
    用户管理视图
    只有系统管理员可以访问
    显示所有用户列表，管理员可以为用户分配角色
    """
    # 权限检查：只有管理员可以访问
    if request.user.role != User.Role.ADMIN:
        messages.error(request, '您没有权限访问此页面')
        return redirect('dashboard')
    
    # 获取所有用户，按注册时间倒序排列
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'users/user_management.html', {'users': users})

@login_required
def assign_role(request, user_id):
    """
    分配用户角色视图
    只有系统管理员可以执行此操作
    支持将用户角色在普通用户、报销负责人、系统管理员之间切换
    """
    # 权限检查：只有管理员可以分配角色
    if request.user.role != User.Role.ADMIN:
        messages.error(request, '您没有权限执行此操作')
        return redirect('dashboard')
    
    target_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        new_role = request.POST.get('role')
        # 验证角色值是否有效
        if new_role in [User.Role.APPLICANT, User.Role.LEAD, User.Role.ADMIN]:
            old_role_display = target_user.get_role_display()
            target_user.role = new_role
            
            # 如果设置为负责人，且没有组织名称，则使用部门作为组织名称
            if new_role == User.Role.LEAD and not target_user.organization:
                target_user.organization = target_user.department
            
            target_user.save()
            messages.success(request, f'已将 {target_user.username} 的角色从 {old_role_display} 变更为 {target_user.get_role_display()}')
        else:
            messages.error(request, '无效的角色')
    
    return redirect('user_management')
