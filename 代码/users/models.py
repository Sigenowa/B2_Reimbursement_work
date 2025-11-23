from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """自定义用户模型，扩展Django默认用户模型，添加角色、学号、部门等字段"""
    
    class Role(models.TextChoices):
        """用户角色枚举"""
        APPLICANT = 'APPLICANT', '普通用户'
        LEAD = 'LEAD', '报销负责人'
        ADMIN = 'ADMIN', '系统管理员'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.APPLICANT, verbose_name='角色')
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='学号')
    college = models.CharField(max_length=100, default='环境学院', verbose_name='学院')
    department = models.CharField(max_length=100, verbose_name='部门')
    organization = models.CharField(max_length=100, blank=True, verbose_name='组织名称')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_lead(self):
        """判断是否为报销负责人"""
        return self.role == self.Role.LEAD
    
    @property
    def is_applicant(self):
        """判断是否为普通用户"""
        return self.role == self.Role.APPLICANT
    
    @property
    def is_admin(self):
        """判断是否为系统管理员"""
        return self.role == self.Role.ADMIN

