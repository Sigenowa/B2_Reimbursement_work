"""
WSGI配置文件
用于Gunicorn等WSGI服务器部署
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reimbursement_system.settings")

application = get_wsgi_application()





