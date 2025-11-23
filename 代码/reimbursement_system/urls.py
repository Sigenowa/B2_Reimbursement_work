from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from claims import views as claim_views
from django.conf import settings
from django.conf.urls.static import static

# URL路由配置，定义所有URL路径和对应的视图函数
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', claim_views.dashboard, name='dashboard'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', user_views.profile_edit, name='profile_edit'),
    path('users/', user_views.user_management, name='user_management'),
    path('users/<int:user_id>/assign-role/', user_views.assign_role, name='assign_role'),
    path('claims/', include('claims.urls')),
]

# 开发环境配置：提供媒体文件服务，生产环境应使用Nginx等Web服务器
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

