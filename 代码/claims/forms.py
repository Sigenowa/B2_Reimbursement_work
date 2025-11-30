from django import forms
from django.forms import inlineformset_factory
from .models import Reimbursement, ReimbursementItem, Invoice

class ReimbursementForm(forms.ModelForm):
    """报销单基本信息表单，用于填写活动主题和活动主要内容"""
    class Meta:
        model = Reimbursement
        fields = ['theme', 'description']
        widgets = {
            'theme': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'theme': '活动主题',
            'description': '活动主要内容',
        }

class ReimbursementItemForm(forms.ModelForm):
    """报销明细表单，用于填写单个物品的信息：名称、数量、单价，金额字段会自动计算"""
    class Meta:
        model = ReimbursementItem
        fields = ['name', 'quantity', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control item-name'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control item-quantity', 'min': 1}),
            'price': forms.NumberInput(attrs={'class': 'form-control item-price', 'step': '0.01'}),
        }
        labels = {
            'name': '物品名称',
            'quantity': '数量',
            'price': '单价',
        }

# 使用inlineformset_factory创建多行表单，允许在一个报销单中添加多个物品明细
ReimbursementItemFormSet = inlineformset_factory(
    Reimbursement, ReimbursementItem, form=ReimbursementItemForm,
    extra=1,
    can_delete=True
)

class MultipleFileInput(forms.ClearableFileInput):
    """自定义文件输入组件，支持同时选择多个文件上传"""
    allow_multiple_selected = True

class InvoiceUploadForm(forms.Form):
    """发票上传表单，支持一次选择多个PDF文件上传"""
    files = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        required=False,
        label='上传发票 (支持多选)'
    )
