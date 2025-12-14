from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from claims import views as claim_views
from django.conf import settings
from django.conf.urls.static import static

# URL路由配置
# 定义所有URL路径和对应的视图函数
urlpatterns = [
    path('admin/', admin.site.urls),  # Django管理后台
    path('', claim_views.dashboard, name='dashboard'),  # 首页，显示仪表盘
    path('register/', user_views.register, name='register'),  # 用户注册
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),  # 用户登录
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # 用户登出
    path('profile/', user_views.profile_edit, name='profile_edit'),  # 个人信息编辑
    path('users/', user_views.user_management, name='user_management'),  # 用户管理（仅管理员）
    path('users/<int:user_id>/assign-role/', user_views.assign_role, name='assign_role'),  # 分配用户角色
    path('claims/', include('claims.urls')),  # 报销相关URL，包含在claims应用的urls.py中
]

# 开发环境配置：提供媒体文件服务
# 生产环境应使用Nginx等Web服务器提供静态文件和媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
