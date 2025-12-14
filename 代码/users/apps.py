from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    用户应用配置类
    定义用户管理应用的配置信息
    """
    default_auto_field = "django.db.models.BigAutoField"  # 默认主键字段类型
    name = "users"  # 应用名称
