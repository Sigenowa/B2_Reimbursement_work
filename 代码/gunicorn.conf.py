# Gunicorn配置文件
# 用于生产环境的WSGI服务器配置

import multiprocessing

# 绑定地址和端口
bind = "127.0.0.1:8000"

# 工作进程数，建议设置为CPU核心数的2-4倍
workers = multiprocessing.cpu_count() * 2 + 1

# 工作模式
worker_class = "sync"

# 每个进程的线程数
threads = 2

# 最大请求数，超过后重启进程（防止内存泄漏）
max_requests = 1000
max_requests_jitter = 50

# 超时时间
timeout = 30
graceful_timeout = 30

# 进程名称
proc_name = "reimbursement_system"

# 日志配置
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# 进程管理
daemon = False
pidfile = "/var/run/gunicorn/reimbursement.pid"

# 安全配置
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190





