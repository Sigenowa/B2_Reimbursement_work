"""
报销单数据模型
定义报销系统的核心数据表：活动主题、报销单、报销明细、发票凭证
"""
from django.db import models
from django.conf import settings


class ActivityTheme(models.Model):
    """
    活动主题表
    同部门用户共享主题列表，选择已有主题时自动填充活动时间
    便于同一活动的多个报销单归类到一起导出
    """
    name = models.CharField(max_length=200, verbose_name='活动主题名称')
    department = models.CharField(max_length=100, verbose_name='所属部门')
    
    # 活动时间，同主题共享
    activity_year = models.PositiveIntegerField(verbose_name='活动年份')
    activity_month = models.PositiveIntegerField(verbose_name='活动月份')
    activity_day = models.PositiveIntegerField(verbose_name='活动日期')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '活动主题'
        verbose_name_plural = '活动主题管理'
        unique_together = ['name', 'department']  # 同部门不能有重复主题名
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.department})"
    
    @property
    def activity_date_display(self):
        """格式化显示活动日期"""
        return f"{self.activity_year}年{self.activity_month}月{self.activity_day}日"


class Reimbursement(models.Model):
    """
    报销单主表
    每个用户提交一次报销对应一条记录
    关联到活动主题，便于按主题分组导出
    """
    
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', '草稿'
        SUBMITTED = 'SUBMITTED', '待处理'
        PACKED = 'PACKED', '已打包'
        REJECTED = 'REJECTED', '已驳回'

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='reimbursements',
        verbose_name='申请人'
    )
    
    # 关联活动主题（选择已有或新建）
    activity_theme = models.ForeignKey(
        ActivityTheme,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reimbursements',
        verbose_name='活动主题'
    )
    
    # 冗余存储主题名，防止主题被删除后丢失信息
    theme = models.CharField(max_length=200, verbose_name='活动主题')
    description = models.TextField(blank=True, verbose_name='活动主要内容')
    
    # 活动时间（从活动主题同步，或手动填写）
    activity_year = models.PositiveIntegerField(verbose_name='活动年份', null=True, blank=True)
    activity_month = models.PositiveIntegerField(verbose_name='活动月份', null=True, blank=True)
    activity_day = models.PositiveIntegerField(verbose_name='活动日期', null=True, blank=True)
    
    activity_location = models.CharField(max_length=200, verbose_name='活动地点', blank=True)
    activity_leader = models.CharField(max_length=100, verbose_name='相关负责人', blank=True)
    
    department = models.CharField(max_length=100, verbose_name='所属部门')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name='状态')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='总金额')
    reviewer_note = models.TextField(blank=True, verbose_name='审核备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    @property
    def activity_date_display(self):
        """格式化显示活动日期"""
        if self.activity_year and self.activity_month and self.activity_day:
            return f"{self.activity_year}年{self.activity_month}月{self.activity_day}日"
        return "未填写"

    class Meta:
        verbose_name = '报销单'
        verbose_name_plural = '报销单管理'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.theme} - {self.applicant.username} ({self.get_status_display()})"

    def calculate_total(self):
        """遍历所有明细项，汇总计算报销总金额"""
        total = sum(item.amount for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])


class ReimbursementItem(models.Model):
    """
    报销明细表
    记录每一项物品的名称、数量、单价
    每个物品可以关联多张发票/凭证
    """
    
    reimbursement = models.ForeignKey(
        Reimbursement, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name='报销单'
    )
    name = models.CharField(max_length=200, verbose_name='物品名称')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')
    unit = models.CharField(max_length=20, default='个', verbose_name='单位')  # 量词：个、套、箱等
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额', editable=False)

    class Meta:
        verbose_name = '报销明细'
        verbose_name_plural = '报销明细'

    def save(self, *args, **kwargs):
        """保存前自动计算金额"""
        self.amount = self.quantity * self.price
        super().save(*args, **kwargs)
        self.reimbursement.calculate_total()

    def delete(self, *args, **kwargs):
        """删除后重新汇总"""
        super().delete(*args, **kwargs)
        self.reimbursement.calculate_total()
    
    def __str__(self):
        return f"{self.name} x {self.quantity}{self.unit}"


class Invoice(models.Model):
    """
    发票凭证表
    与物品明细绑定（不再与报销单直接绑定）
    每个物品可以上传多张发票、订单截图等凭证
    """
    
    # 改为关联到物品明细
    item = models.ForeignKey(
        ReimbursementItem,
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name='物品明细'
    )
    
    file = models.FileField(upload_to='invoices/%Y/%m/%d/', verbose_name='凭证文件')
    file_name = models.CharField(max_length=200, blank=True, verbose_name='原始文件名')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        verbose_name = '发票凭证'
        verbose_name_plural = '发票凭证'
    
    def save(self, *args, **kwargs):
        """保存时记录原始文件名"""
        if not self.file_name and self.file:
            self.file_name = self.file.name.split('/')[-1]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.file_name} - {self.item.name}"
