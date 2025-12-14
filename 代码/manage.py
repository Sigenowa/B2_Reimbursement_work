#!/usr/bin/env python
"""
Django命令行工具
用于执行Django管理任务，如运行服务器、创建迁移、执行迁移等
使用方法: python manage.py <command>
"""
import os
import sys


def main():
    """
    主函数
    设置Django环境并执行命令行参数指定的管理任务
    """
    # 设置Django设置模块，告诉Django使用哪个配置文件
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reimbursement_system.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "无法导入Django。请确认Django已安装并可用。"
            "是否忘记激活虚拟环境？"
        ) from exc
    # 执行命令行参数指定的Django管理命令
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
