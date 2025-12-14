"""
ASGI配置文件
ASGI (Asynchronous Server Gateway Interface) 支持异步Web应用
用于WebSocket、HTTP/2等异步功能
更多信息: https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# 设置Django设置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reimbursement_system.settings")

# ASGI应用对象，异步服务器通过此对象与Django应用通信
application = get_asgi_application()
