from django import forms
from django.forms import inlineformset_factory
from .models import Reimbursement, ReimbursementItem, Invoice

class ReimbursementForm(forms.ModelForm):
    """
    报销单基本信息表单
    用于填写活动主题和活动主要内容
    """
    class Meta:
        model = Reimbursement
        fields = ['theme', 'description']
        widgets = {
            'theme': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ReimbursementItemForm(forms.ModelForm):
    """
    报销明细表单
    用于填写单个物品的信息：名称、数量、单价
    金额字段会自动计算，不需要用户填写
    """
    class Meta:
        model = ReimbursementItem
        fields = ['name', 'quantity', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control item-name'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control item-quantity', 'min': 1}),
            'price': forms.NumberInput(attrs={'class': 'form-control item-price', 'step': '0.01'}),
        }

# 使用inlineformset_factory创建多行表单
# 允许在一个报销单中添加多个物品明细，支持动态添加和删除
ReimbursementItemFormSet = inlineformset_factory(
    Reimbursement, ReimbursementItem, form=ReimbursementItemForm,
    extra=1,  # 默认显示1个空行
    can_delete=True  # 允许删除已存在的明细
)

class MultipleFileInput(forms.ClearableFileInput):
    """
    自定义文件输入组件
    支持同时选择多个文件上传
    Django默认的FileInput不支持multiple属性，需要自定义
    """
    allow_multiple_selected = True

class InvoiceUploadForm(forms.Form):
    """
    发票上传表单
    支持一次选择多个PDF文件上传
    文件大小和格式限制在视图层或settings中配置
    """
    files = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        required=False,  # 发票不是必填项
        label='上传发票 (支持多选)'
    )
