#!/usr/bin/env python
"""
Django命令行工具
使用方法: python manage.py <command>
"""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reimbursement_system.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "无法导入Django。请确认Django已安装并可用。"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()





