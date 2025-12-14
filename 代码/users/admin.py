from django.contrib import admin
from .models import User

# 注册User模型到Django管理后台
# 管理员可以通过后台界面管理用户信息
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """用户模型管理类，配置管理后台的显示和编辑选项"""
    list_display = ['username', 'first_name', 'student_id', 'college', 'department', 'role', 'date_joined']
    list_filter = ['role', 'college', 'department']
    search_fields = ['username', 'first_name', 'student_id', 'email']
    readonly_fields = ['date_joined', 'last_login']
