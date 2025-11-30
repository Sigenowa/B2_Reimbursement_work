from django.contrib import admin
from .models import Reimbursement, ReimbursementItem, Invoice

class ReimbursementItemInline(admin.TabularInline):
    """在报销单管理页面中内联显示物品明细"""
    model = ReimbursementItem
    extra = 1

@admin.register(Reimbursement)
class ReimbursementAdmin(admin.ModelAdmin):
    """报销单模型管理类"""
    list_display = ['theme', 'applicant', 'department', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'department', 'created_at']
    search_fields = ['theme', 'applicant__username', 'applicant__first_name']
    inlines = [ReimbursementItemInline]

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """发票模型管理类"""
    list_display = ['reimbursement', 'file', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['reimbursement__theme']


