"""
报销单表单定义
包含活动主题选择、报销单基本信息、物品明细、发票上传等表单
"""
from django import forms
from django.forms import inlineformset_factory
from .models import Reimbursement, ReimbursementItem, Invoice, ActivityTheme


class ReimbursementForm(forms.ModelForm):
    """
    报销单基本信息表单
    活动主题支持下拉选择已有主题或输入新主题
    """
    
    # 活动主题下拉选择（可选）
    existing_theme = forms.ModelChoiceField(
        queryset=ActivityTheme.objects.none(),
        required=False,
        label='选择已有主题',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    class Meta:
        model = Reimbursement
        fields = ['theme', 'description', 'activity_year', 'activity_month', 'activity_day', 
                  'activity_location', 'activity_leader']
        widgets = {
            'theme': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '输入新主题或从上方选择已有主题',
                'id': 'theme-input'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '请描述活动主要内容（选填）'
            }),
            'activity_year': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_activity_year'
            }),
            'activity_month': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_activity_month'
            }),
            'activity_day': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_activity_day'
            }),
            'activity_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入活动地点（必填）'
            }),
            'activity_leader': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入相关负责人姓名（必填）'
            }),
        }
        error_messages = {
            'theme': {'required': '⚠️ 活动主题不能为空！'},
            'activity_year': {'required': '⚠️ 活动年份不能为空！'},
            'activity_month': {'required': '⚠️ 活动月份不能为空！'},
            'activity_day': {'required': '⚠️ 活动日期不能为空！'},
            'activity_location': {'required': '⚠️ 活动地点不能为空！'},
            'activity_leader': {'required': '⚠️ 相关负责人不能为空！'},
        }
    
    def __init__(self, *args, department=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['theme'].required = True
        self.fields['description'].required = False
        self.fields['activity_year'].required = True
        self.fields['activity_month'].required = True
        self.fields['activity_day'].required = True
        self.fields['activity_location'].required = True
        self.fields['activity_leader'].required = True
        
        # 根据部门筛选可选的活动主题
        if department:
            self.fields['existing_theme'].queryset = ActivityTheme.objects.filter(
                department=department
            ).order_by('-created_at')
        
        # 如果编辑已有报销单且关联了主题，使用主题的时间
        if self.instance and self.instance.pk and self.instance.activity_theme:
            # 设置已有主题的初始值
            self.fields['existing_theme'].initial = self.instance.activity_theme
            
            # 如果报销单的时间字段为空，使用主题的时间
            if not self.instance.activity_year and self.instance.activity_theme.activity_year:
                self.instance.activity_year = self.instance.activity_theme.activity_year
            if not self.instance.activity_month and self.instance.activity_theme.activity_month:
                self.instance.activity_month = self.instance.activity_theme.activity_month
            if not self.instance.activity_day and self.instance.activity_theme.activity_day:
                self.instance.activity_day = self.instance.activity_theme.activity_day
        
        # 设置年份选项（根据当前月份动态设置，在模板中通过JavaScript实现）
        from datetime import datetime
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year
        
        # 如果当前是1-6月，可以选择去年和今年；如果是7-12月，只能选择今年
        if current_month <= 6:
            year_choices = [(current_year - 1, str(current_year - 1)), (current_year, str(current_year))]
        else:
            year_choices = [(current_year, str(current_year))]
        
        # 如果编辑已有报销单且关联了主题，确保主题的年份在选项中
        if self.instance and self.instance.pk and self.instance.activity_theme:
            theme_year = self.instance.activity_theme.activity_year
            if theme_year and theme_year not in [y[0] for y in year_choices]:
                year_choices.append((theme_year, str(theme_year)))
                year_choices.sort()  # 按年份排序
        
        # 如果编辑已有报销单且有年份值，确保该年份在选项中
        if self.instance and self.instance.pk and self.instance.activity_year:
            instance_year = self.instance.activity_year
            if instance_year not in [y[0] for y in year_choices]:
                year_choices.append((instance_year, str(instance_year)))
                year_choices.sort()  # 按年份排序
        
        self.fields['activity_year'].widget.choices = [('', '-- 选择年份 --')] + year_choices
        
        # 设置月份选项（1-12月）
        # 注意：不在后端设置disabled属性，由前端JavaScript控制启用/禁用状态
        month_choices = [(i, f'{i}月') for i in range(1, 13)]
        self.fields['activity_month'].widget.choices = [('', '-- 请先选择年份 --')] + month_choices
        # 不在后端设置disabled，让前端JavaScript根据年份值来控制
        
        # 日期选项在JavaScript中动态生成，初始只显示占位符
        # 不预先生成1-31天的选项，避免显示错误的日期（如6月31日）
        # 但如果编辑模式下已有年月值，需要预先生成日期选项
        if (self.instance and self.instance.pk and 
            hasattr(self.instance, 'activity_year') and self.instance.activity_year and
            hasattr(self.instance, 'activity_month') and self.instance.activity_month):
            # 编辑模式下，如果已有年月值，预先生成日期选项
            import calendar
            year = self.instance.activity_year
            month = self.instance.activity_month
            days_in_month = calendar.monthrange(year, month)[1]
            day_choices = [('', '-- 选择日期 --')] + [(i, f'{i}日') for i in range(1, days_in_month + 1)]
            self.fields['activity_day'].widget.choices = day_choices
        else:
            # 新建模式下，只显示占位符
            self.fields['activity_day'].widget.choices = [('', '-- 请先选择年月 --')]
        # 不在后端设置disabled，让前端JavaScript根据年月值来控制
    
    def clean_activity_month(self):
        month = self.cleaned_data.get('activity_month')
        if month and (month < 1 or month > 12):
            raise forms.ValidationError('月份必须在1-12之间')
        return month
    
    def clean_activity_day(self):
        day = self.cleaned_data.get('activity_day')
        year = self.cleaned_data.get('activity_year')
        month = self.cleaned_data.get('activity_month')
        
        if day and year and month:
            # 验证日期是否有效（考虑月份天数和闰年）
            from calendar import monthrange
            max_day = monthrange(year, month)[1]
            if day < 1 or day > max_day:
                raise forms.ValidationError(f'{year}年{month}月只有{max_day}天')
        elif day and (day < 1 or day > 31):
            raise forms.ValidationError('日期必须在1-31之间')
        
        return day


class ReimbursementItemForm(forms.ModelForm):
    """
    报销明细表单（单行）
    包含物品名称、数量、单位、单价
    """
    class Meta:
        model = ReimbursementItem
        fields = ['name', 'quantity', 'unit', 'price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control item-name',
                'placeholder': '物品名称'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control item-quantity',
                'min': 1,
                'placeholder': '数量',
                'style': 'width: 80px'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control item-unit',
                'placeholder': '单位',
                'style': 'width: 60px',
                'value': '个'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control item-price',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '单价'
            }),
        }
        error_messages = {
            'name': {'required': '物品名称不能为空'},
            'quantity': {'required': '数量不能为空'},
            'price': {'required': '单价不能为空'},
        }


# 物品明细表单集
ReimbursementItemFormSet = inlineformset_factory(
    Reimbursement, 
    ReimbursementItem, 
    form=ReimbursementItemForm,
    extra=1,
    can_delete=True
)


class ItemInvoiceForm(forms.ModelForm):
    """
    物品发票上传表单
    每个物品可以上传多张凭证
    """
    class Meta:
        model = Invoice
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-sm',
                'accept': '.pdf,.jpg,.jpeg,.png'
            })
        }


# 发票表单集（与物品明细关联）
ItemInvoiceFormSet = inlineformset_factory(
    ReimbursementItem,
    Invoice,
    form=ItemInvoiceForm,
    extra=1,
    can_delete=True
)
