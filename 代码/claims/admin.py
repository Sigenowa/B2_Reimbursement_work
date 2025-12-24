from django.contrib import admin
from .models import Reimbursement, ReimbursementItem, Invoice

@admin.register(Reimbursement)
class ReimbursementAdmin(admin.ModelAdmin):
    """报销单模型管理类"""
    list_display = ['theme', 'applicant', 'department', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'department', 'created_at']
    search_fields = ['theme', 'applicant__username', 'applicant__student_id']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']

@admin.register(ReimbursementItem)
class ReimbursementItemAdmin(admin.ModelAdmin):
    """报销明细模型管理类"""
    list_display = ['reimbursement', 'name', 'quantity', 'price', 'amount']
    list_filter = ['reimbursement__status']
    search_fields = ['name', 'reimbursement__theme']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """发票模型管理类"""
    list_display = ['reimbursement', 'file', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['reimbursement__theme']





