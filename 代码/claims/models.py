from django.db import models
from django.conf import settings
from django.utils import timezone

class Reimbursement(models.Model):
    """
    报销单模型
    存储报销申请的基本信息，包括申请人、活动主题、状态等
    """
    
    class Status(models.TextChoices):
        """报销单状态枚举：草稿、待处理、已打包、已驳回"""
        DRAFT = 'DRAFT', '草稿'  # 用户暂存，未提交
        SUBMITTED = 'SUBMITTED', '待处理'  # 已提交，等待负责人审核
        PACKED = 'PACKED', '已打包'  # 审核通过，已完成打包
        REJECTED = 'REJECTED', '已驳回'  # 审核驳回，可以修改后重新提交

    # 关联到用户模型，删除用户时级联删除其所有报销单
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reimbursements', verbose_name='申请人')
    
    # 活动主题，用于标识报销单的主要内容
    theme = models.CharField(max_length=200, verbose_name='活动主题')
    
    # 活动详细描述，支持多行文本
    description = models.TextField(blank=True, verbose_name='活动主要内容')
    
    # 所属部门，用于负责人筛选本部门的报销单
    department = models.CharField(max_length=100, verbose_name='所属部门')
    
    # 报销单状态，默认为草稿状态
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name='状态')
    
    # 总金额，由所有物品明细自动计算得出
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='总金额')
    
    # 审核备注，负责人审核时填写的意见
    reviewer_note = models.TextField(blank=True, verbose_name='审核备注')
    
    # 创建时间，自动记录报销单创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    # 更新时间，每次保存时自动更新
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '报销单'
        verbose_name_plural = '报销单管理'
        # 按创建时间倒序排列，最新的在前
        ordering = ['-created_at']

    def __str__(self):
        """返回报销单的字符串表示，用于管理后台显示"""
        return f"{self.theme} - {self.applicant.username} ({self.get_status_display()})"

    def calculate_total(self):
        """
        计算报销单总金额
        遍历所有关联的物品明细，累加金额并更新total_amount字段
        """
        total = sum(item.amount for item in self.items.all())
        self.total_amount = total
        # 只更新total_amount字段，避免触发其他字段的自动更新
        self.save(update_fields=['total_amount'])

class ReimbursementItem(models.Model):
    """
    报销明细模型
    存储报销单中的物品明细，支持一个报销单包含多个物品
    """
    
    # 关联到报销单，删除报销单时级联删除所有明细
    reimbursement = models.ForeignKey(Reimbursement, on_delete=models.CASCADE, related_name='items', verbose_name='报销单')
    
    # 物品名称
    name = models.CharField(max_length=100, verbose_name='物品名称')
    
    # 数量，必须为正整数
    quantity = models.PositiveIntegerField(default=1, verbose_name='数量')
    
    # 单价，使用Decimal确保金额精度
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价')
    
    # 金额，由数量×单价自动计算，不允许手动编辑
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额', editable=False)

    class Meta:
        verbose_name = '报销明细'
        verbose_name_plural = '报销明细'

    def save(self, *args, **kwargs):
        """
        保存时自动计算金额
        金额 = 数量 × 单价，计算后保存并触发报销单总金额重新计算
        """
        self.amount = self.quantity * self.price
        super().save(*args, **kwargs)
        # 保存后更新关联报销单的总金额
        self.reimbursement.calculate_total()

    def delete(self, *args, **kwargs):
        """
        删除明细后重新计算报销单总金额
        确保删除物品后总金额保持准确
        """
        super().delete(*args, **kwargs)
        # 删除后需要重新计算总金额
        self.reimbursement.calculate_total()

class Invoice(models.Model):
    """
    发票凭证模型
    存储报销单关联的发票文件，支持一个报销单上传多张发票
    """
    
    # 关联到报销单，删除报销单时级联删除所有发票
    reimbursement = models.ForeignKey(Reimbursement, on_delete=models.CASCADE, related_name='invoices', verbose_name='报销单')
    
    # 发票文件，按年月日自动分类存储，便于管理
    file = models.FileField(upload_to='invoices/%Y/%m/%d/', verbose_name='发票文件')
    
    # 上传时间，自动记录文件上传时间
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        verbose_name = '发票凭证'
        verbose_name_plural = '发票凭证'
    
    def __str__(self):
        """返回发票的字符串表示"""
        return f"Invoice for {self.reimbursement.theme}"
