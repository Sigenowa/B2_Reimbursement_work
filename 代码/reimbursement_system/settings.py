"""
Django项目配置文件 - 服务器部署版本
支持服务器 IP: 101.43.149.245 的公网访问
包含数据库、应用、中间件等所有配置信息
"""

from pathlib import Path
import os

# 项目根目录路径
BASE_DIR = Path(__file__).resolve().parent.parent

# ================================
# 安全配置 - 生产环境必须修改
# ================================

# SECRET_KEY从环境变量读取，如果不存在则使用默认值（仅用于开发环境）
# 生产环境必须设置环境变量：export SECRET_KEY='your-secret-key-here'
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# 调试模式：生产环境必须设为False
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

# 允许访问的主机列表
# 包含服务器IP和可能的域名
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '101.43.149.245',  # 服务器公网IP
    # 如果有域名，在此添加，例如：
    # 'reimbursement.example.com',
]

# CSRF信任源（用于跨域请求）
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://101.43.149.245',
    'http://101.43.149.245:8000',
    'http://101.43.149.245:80',
    # 如果使用HTTPS，添加：
    # 'https://101.43.149.245',
    # 'https://reimbursement.example.com',
]

# ================================
# 应用配置
# ================================

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

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # 安全中间件
    "whitenoise.middleware.WhiteNoiseMiddleware",  # 静态文件服务中间件（生产环境）
    "django.contrib.sessions.middleware.SessionMiddleware",  # 会话管理
    "django.middleware.common.CommonMiddleware",  # 通用功能
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF保护
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # 用户认证
    "django.contrib.messages.middleware.MessageMiddleware",  # 消息处理
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # 点击劫持保护
]

ROOT_URLCONF = "reimbursement_system.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "reimbursement_system.wsgi.application"

# ================================
# 数据库配置
# ================================

# 通过环境变量USE_SQLITE控制数据库类型
if os.environ.get('USE_SQLITE', 'false').lower() in ('true', '1', 'yes'):
    # SQLite配置
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # MySQL配置
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("DB_NAME", "reimbursement_db"),
            "USER": os.environ.get("DB_USER", "reimbursement_user"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "your_password_here"),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }

# ================================
# 密码验证配置
# ================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

# 静态文件URL
STATIC_URL = "/static/"

# 开发环境静态文件目录
STATICFILES_DIRS = [BASE_DIR / "static"]

# 生产环境静态文件收集目录（python manage.py collectstatic）
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise静态文件压缩（生产环境优化）
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 媒体文件配置（用户上传的文件）
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ================================
# 其他配置
# ================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 自定义用户模型
AUTH_USER_MODEL = 'users.User'

# 登录重定向配置
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# ================================
# 安全配置（生产环境建议开启）
# ================================

# 如果使用HTTPS，启用以下配置：
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True

# 会话配置
SESSION_COOKIE_AGE = 86400  # 会话有效期：24小时
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 关闭浏览器不清除会话

# 日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'] if not DEBUG else ['console'],
        'level': 'INFO',
    },
}





