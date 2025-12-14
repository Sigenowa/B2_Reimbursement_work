from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    自定义用户模型
    扩展Django默认用户模型，添加角色、学号、部门等字段
    支持三种角色：普通用户、报销负责人、系统管理员
    """
    
    class Role(models.TextChoices):
        """用户角色枚举：普通用户、报销负责人、系统管理员"""
        APPLICANT = 'APPLICANT', '普通用户'  # 可以提交报销单
        LEAD = 'LEAD', '报销负责人'  # 可以审核和导出报销单
        ADMIN = 'ADMIN', '系统管理员'  # 可以管理用户和分配角色

    # 用户角色，默认为普通用户，由管理员分配
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.APPLICANT, verbose_name='角色')
    
    # 学号，作为用户的唯一标识，注册时必填
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='学号')
    
    # 学院，默认为环境学院
    college = models.CharField(max_length=100, default='环境学院', verbose_name='学院')
    
    # 部门，注册时从下拉列表选择
    department = models.CharField(max_length=100, verbose_name='部门')
    
    # 组织名称，负责人角色时使用，用于筛选本组织的报销单
    organization = models.CharField(max_length=100, blank=True, verbose_name='组织名称')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

    def __str__(self):
        """返回用户的字符串表示，显示用户名和角色"""
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_lead(self):
        """判断用户是否为报销负责人"""
        return self.role == self.Role.LEAD
    
    @property
    def is_applicant(self):
        """判断用户是否为普通用户"""
        return self.role == self.Role.APPLICANT
    
    @property
    def is_admin(self):
        """判断用户是否为系统管理员"""
        return self.role == self.Role.ADMIN
