from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from claims import views as claim_views
from django.conf import settings
from django.conf.urls.static import static

# URL路由配置
urlpatterns = [
    path('admin/', admin.site.urls),  # Django管理后台
    path('', claim_views.dashboard, name='dashboard'),  # 首页仪表盘
    path('register/', user_views.register, name='register'),  # 用户注册
    path('login/', user_views.CustomLoginView.as_view(), name='login'),  # 登录（自定义视图，显示错误提示）
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # 登出
    path('profile/', user_views.profile_edit, name='profile_edit'),  # 个人信息
    path('users/', user_views.user_management, name='user_management'),  # 用户管理
    path('users/<int:user_id>/assign-role/', user_views.assign_role, name='assign_role'),  # 分配角色
    path('users/<int:user_id>/toggle-ban/', user_views.toggle_ban, name='toggle_ban'),  # 封禁/解封用户
    path('claims/', include('claims.urls')),  # 报销相关URL
]

# 媒体文件服务（开发环境和Nginx未配置时使用）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


