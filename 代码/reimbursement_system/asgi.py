"""
ASGI配置文件
用于异步服务器部署（如Daphne、Uvicorn）
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reimbursement_system.settings")

application = get_asgi_application()





