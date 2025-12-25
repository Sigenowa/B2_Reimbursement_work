"""
用户管理视图函数
处理用户注册、登录、个人信息编辑、角色分配、账号封禁等功能
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from .forms import RegisterForm, ProfileEditForm, PasswordChangeForm
from .models import User


class CustomLoginView(LoginView):
    """
    自定义登录视图
    登录失败时显示明确的错误提示
    """
    template_name = 'users/login.html'
    
    def form_invalid(self, form):
        """
        登录表单验证失败时调用
        显示用户名或密码错误提示
        """
        messages.error(self.request, '用户名或密码错误，请重新输入')
        return super().form_invalid(form)


def register(request):
    """
    用户注册
    注册成功后自动登录并跳转到仪表盘
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 注册后自动登录
            messages.success(request, f'注册成功！欢迎 {user.first_name or user.username}')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_edit(request):
    """
    个人信息编辑
    支持修改基本信息和修改密码两个功能
    修改密码后自动更新session，避免被踢出登录
    """
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '个人信息已更新')
            return redirect('profile_edit')
    else:
        form = ProfileEditForm(instance=request.user)
    
    password_form = PasswordChangeForm(user=request.user)
    
    # 处理修改密码的POST请求（通过隐藏字段区分）
    if request.method == 'POST' and 'change_password' in request.POST:
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, request.user)  # 保持登录状态
            messages.success(request, '密码已修改')
            return redirect('profile_edit')
    
    return render(request, 'users/profile_edit.html', {
        'form': form,
        'password_form': password_form
    })


@login_required
def user_management(request):
    """
    用户管理列表页（仅管理员可访问）
    显示所有用户，支持角色分配和账号封禁操作
    """
    # 权限检查：非管理员无法访问
    if request.user.role != User.Role.ADMIN:
        messages.error(request, '您没有权限访问此页面')
        return redirect('dashboard')
    
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'users/user_management.html', {'users': users})


@login_required
def assign_role(request, user_id):
    """
    分配用户角色（仅管理员可操作）
    可将用户设置为普通用户、报销负责人或系统管理员
    """
    if request.user.role != User.Role.ADMIN:
        messages.error(request, '您没有权限执行此操作')
        return redirect('dashboard')
    
    target_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        new_role = request.POST.get('role')
        
        # 验证角色值有效性
        if new_role in [User.Role.APPLICANT, User.Role.LEAD, User.Role.ADMIN]:
            old_role_display = target_user.get_role_display()
            target_user.role = new_role
            
            # 设为负责人时自动填充organization字段（兼容旧逻辑）
            if new_role == User.Role.LEAD and not target_user.organization:
                target_user.organization = target_user.department
            
            target_user.save()
            messages.success(request, f'已将 {target_user.username} 的角色从 {old_role_display} 变更为 {target_user.get_role_display()}')
        else:
            messages.error(request, '无效的角色')
    
    return redirect('user_management')


@login_required
def toggle_ban(request, user_id):
    """
    封禁/解封用户（仅管理员可操作）
    被封禁的用户无法登录系统
    通过切换is_active字段实现，Django内置登录会检查此字段
    """
    if request.user.role != User.Role.ADMIN:
        messages.error(request, '您没有权限执行此操作')
        return redirect('dashboard')
    
    target_user = get_object_or_404(User, id=user_id)
    
    # 安全检查：不能封禁自己
    if target_user == request.user:
        messages.error(request, '您不能封禁自己')
        return redirect('user_management')
    
    if request.method == 'POST':
        # 切换激活状态
        target_user.is_active = not target_user.is_active
        target_user.save()
        
        if target_user.is_active:
            messages.success(request, f'已解封用户 {target_user.username}')
        else:
            messages.warning(request, f'已封禁用户 {target_user.username}，该用户将无法登录')
    
    return redirect('user_management')
