"""
Django项目配置文件
包含数据库、应用、中间件等所有配置信息
"""

from pathlib import Path
import os

# 项目根目录路径，用于构建其他路径
BASE_DIR = Path(__file__).resolve().parent.parent


# 安全警告：生产环境必须修改SECRET_KEY并妥善保管
# 生产环境建议从环境变量读取，不要硬编码在代码中
SECRET_KEY = "django-insecure-6jeho9o4pm3-@5vu%sffr*373h7l@h7uxksr$9ta8@)qkw2qo("

# 调试模式：开发环境为True，生产环境必须设为False
# True时会显示详细错误信息，False时只显示通用错误页面
DEBUG = True

# 允许访问的主机列表
# ['*'] 表示允许所有主机（仅开发环境）
# 生产环境应指定具体的域名或IP地址
ALLOWED_HOSTS = ['*']


# 已安装的应用列表
# Django内置应用提供认证、会话、消息等功能
# users和claims是项目自定义应用
INSTALLED_APPS = [
    "django.contrib.admin",  # 管理后台
    "django.contrib.auth",  # 认证系统
    "django.contrib.contenttypes",  # 内容类型框架
    "django.contrib.sessions",  # 会话框架
    "django.contrib.messages",  # 消息框架
    "django.contrib.staticfiles",  # 静态文件管理
    "users",  # 用户管理应用
    "claims",  # 报销管理应用
]

# 中间件列表
# 按顺序执行，处理请求和响应的各个阶段
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # 安全相关中间件
    "django.contrib.sessions.middleware.SessionMiddleware",  # 会话管理
    "django.middleware.common.CommonMiddleware",  # 通用功能
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF保护
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # 用户认证
    "django.contrib.messages.middleware.MessageMiddleware",  # 消息处理
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # 点击劫持保护
]

# 根URL配置模块
ROOT_URLCONF = "reimbursement_system.urls"

# 模板配置
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],  # 模板文件目录
        "APP_DIRS": True,  # 允许从应用目录查找模板
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",  # 请求上下文
                "django.contrib.auth.context_processors.auth",  # 用户上下文
                "django.contrib.messages.context_processors.messages",  # 消息上下文
            ],
        },
    },
]

# WSGI应用配置
WSGI_APPLICATION = "reimbursement_system.wsgi.application"


# 数据库配置
# 开发环境使用SQLite，生产环境使用MySQL
# 通过环境变量USE_SQLITE控制数据库类型
if os.environ.get('USE_SQLITE', 'true').lower() in ('true', '1', 'yes'):
    # SQLite配置 - 开发环境推荐
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",  # SQLite数据库引擎
            "NAME": BASE_DIR / "db.sqlite3",  # 数据库文件路径
        }
    }
else:
    # MySQL配置 - 生产环境使用
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",  # MySQL数据库引擎
            "NAME": os.environ.get("DB_NAME", "reimbursement_db"),  # 数据库名称
            "USER": os.environ.get("DB_USER", "root"),  # 数据库用户名
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),  # 数据库密码
            "HOST": os.environ.get("DB_HOST", "localhost"),  # 数据库主机
            "PORT": os.environ.get("DB_PORT", "3306"),  # 数据库端口
            "OPTIONS": {
                "charset": "utf8mb4",  # 使用utf8mb4字符集，支持中文和emoji
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",  # 启用严格模式
            },
        }
    }


# 密码验证器配置
# 用于验证用户密码的强度和安全性
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # 检查密码与用户信息相似度
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # 检查密码最小长度
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # 检查是否为常见密码
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # 检查是否全为数字
    },
]


# 国际化配置
LANGUAGE_CODE = "zh-hans"  # 界面语言：简体中文
TIME_ZONE = "Asia/Shanghai"  # 时区：中国时区
USE_I18N = True  # 启用国际化
USE_TZ = True  # 使用时区


# 静态文件配置
# 静态文件（CSS、JavaScript、图片等）的URL和存储位置
STATIC_URL = "static/"  # 静态文件URL前缀
STATICFILES_DIRS = [BASE_DIR / "static"]  # 静态文件源目录

# 媒体文件配置
# 用户上传的文件（发票等）的URL和存储位置
MEDIA_URL = '/media/'  # 媒体文件URL前缀
MEDIA_ROOT = BASE_DIR / 'media'  # 媒体文件存储目录

# 主键字段类型
# Django 3.2+默认使用BigAutoField作为主键
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 自定义用户模型
# 使用users应用中的User模型替代Django默认用户模型
AUTH_USER_MODEL = 'users.User'

# 登录重定向配置
LOGIN_URL = 'login'  # 未登录用户访问受保护页面时重定向到登录页
LOGIN_REDIRECT_URL = 'dashboard'  # 登录成功后重定向到仪表盘
LOGOUT_REDIRECT_URL = 'login'  # 登出后重定向到登录页
