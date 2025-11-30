from django.db import models
from django.conf import settings
from django.utils import timezone

class Reimbursement(models.Model):
    """报销单模型，存储报销申请的基本信息，包括申请人、活动主题、状态等"""
    
    class Status(models.TextChoices):
        """报销单状态枚举"""
        DRAFT = 'DRAFT', '草稿'
        SUBMITTED = 'SUBMITTED', '待处理'
        PACKED = 'PACKED', '已打包'
        REJECTED = 'REJECTED', '已驳回'

    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reimbursements', verbose_name='申请人')
    theme = models.CharField(max_length=200, verbose_name='活动主题')
    description = models.TextField(blank=True, verbose_name='活动主要内容')
    department = models.CharField(max_length=100, verbose_name='所属部门')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name='状态')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='总金额')
    reviewer_note = models.TextField(blank=True, verbose_name='审核备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '报销单'
        verbose_name_plural = '报销单管理'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.theme} - {self.applicant.username} ({self.get_status_display()})"

    def calculate_total(self):
        """计算报销单总金额，遍历所有关联的物品明细，累加金额并更新total_amount字段"""
        total = sum(item.amount for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])

class ReimbursementItem(models.Model):
    """报销明细模型，存储报销单中的物品明细，支持一个报销单包含多个物品"""
    reimbursement = models.ForeignKey(Reimbursement, on_delete=models.CASCADE, related_name='items', verbose_name='报销单')
    name = models.CharField(max_length=100, verbose_name='物品名称')
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额', editable=False)

    class Meta:
        verbose_name = '报销明细'
        verbose_name_plural = '报销明细'

    def save(self, *args, **kwargs):
        """保存时自动计算金额，金额 = 数量 × 单价，计算后保存并触发报销单总金额重新计算"""
        self.amount = self.quantity * self.price
        super().save(*args, **kwargs)
        # 修复bug：之前没有调用calculate_total，导致总金额不更新
        self.reimbursement.calculate_total()

    def delete(self, *args, **kwargs):
        """删除明细后重新计算报销单总金额"""
        reimbursement = self.reimbursement  # 保存引用，因为删除后无法访问
        super().delete(*args, **kwargs)
        reimbursement.calculate_total()

class Invoice(models.Model):
    """发票凭证模型，存储报销单关联的发票文件，支持一个报销单上传多张发票"""
    reimbursement = models.ForeignKey(Reimbursement, on_delete=models.CASCADE, related_name='invoices', verbose_name='报销单')
    file = models.FileField(upload_to='invoices/%Y/%m/%d/', verbose_name='发票文件')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        verbose_name = '发票凭证'
        verbose_name_plural = '发票凭证'
    
    def __str__(self):
        return f"Invoice for {self.reimbursement.theme}"
