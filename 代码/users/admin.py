from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """用户模型管理类"""
    list_display = ['username', 'first_name', 'student_id', 'college', 'department', 'role', 'date_joined']
    list_filter = ['role', 'college', 'department']
    search_fields = ['username', 'first_name', 'student_id', 'email']
    readonly_fields = ['date_joined', 'last_login']





