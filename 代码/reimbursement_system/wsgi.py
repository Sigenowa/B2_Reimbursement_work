"""
WSGI配置文件
WSGI (Web Server Gateway Interface) 是Python Web应用与Web服务器之间的标准接口
生产环境使用Gunicorn等WSGI服务器运行Django应用时会使用此配置
更多信息: https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 设置Django设置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reimbursement_system.settings")

# WSGI应用对象，Web服务器通过此对象与Django应用通信
application = get_wsgi_application()
