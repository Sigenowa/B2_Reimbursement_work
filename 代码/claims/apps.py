from django.apps import AppConfig


class ClaimsConfig(AppConfig):
    """
    报销应用配置类
    定义报销管理应用的配置信息
    """
    default_auto_field = "django.db.models.BigAutoField"  # 默认主键字段类型
    name = "claims"  # 应用名称
