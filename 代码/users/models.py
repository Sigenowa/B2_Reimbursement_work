"""
用户模型定义
扩展Django内置用户模型，添加角色权限、学号、部门等业务字段
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    自定义用户模型
    继承Django的AbstractUser，保留用户名、密码、邮箱等基础字段
    新增角色、学号、部门等业务相关字段
    """
    
    # 系统支持的三种用户角色，决定用户可访问的功能
    class Role(models.TextChoices):
        APPLICANT = 'APPLICANT', '普通用户'    # 只能提交和管理自己的报销单
        LEAD = 'LEAD', '报销负责人'            # 可以审核本部门报销单、导出数据
        ADMIN = 'ADMIN', '系统管理员'          # 可以管理所有用户、分配角色、封禁账号

    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.APPLICANT,  # 新注册用户默认为普通用户
        verbose_name='角色'
    )
    
    # 学号作为唯一标识，用于区分同名用户
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='学号')
    
    college = models.CharField(max_length=100, default='环境学院', verbose_name='学院')
    
    # 部门字段用于数据隔离：负责人只能看到自己部门的报销单
    department = models.CharField(max_length=100, verbose_name='部门')
    
    # 历史遗留字段，已不再使用
    organization = models.CharField(max_length=100, blank=True, verbose_name='组织名称(已废弃)')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    # 以下三个属性用于在视图中快速判断用户角色
    
    @property
    def is_lead(self):
        """是否为报销负责人"""
        return self.role == self.Role.LEAD
    
    @property
    def is_applicant(self):
        """是否为普通用户"""
        return self.role == self.Role.APPLICANT
    
    @property
    def is_admin(self):
        """是否为系统管理员"""
        return self.role == self.Role.ADMIN
