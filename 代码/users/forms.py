from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# 预定义的部门列表，用户注册时从下拉列表选择
# 可根据实际情况修改部门选项
DEPARTMENT_CHOICES = [
    ('文艺部', '文艺部'),
    ('体育部', '体育部'),
    ('学习部', '学习部'),
    ('宣传部', '宣传部'),
    ('组织部', '组织部'),
    ('外联部', '外联部'),
    ('生活部', '生活部'),
    ('其他', '其他'),
]

class RegisterForm(UserCreationForm):
    """
    用户注册表单
    扩展Django默认注册表单，添加学号、部门等字段
    所有新用户默认角色为普通用户，学院默认为环境学院
    """
    # 部门选择字段，从预定义列表中选择
    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='部门',
        help_text='请选择您所在的部门'
    )
    
    # 学号字段，作为用户的唯一标识，注册时必填
    student_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='学号',
        required=True,
        help_text='学号将作为您的唯一标识'
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'student_id', 'department', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        """初始化表单，设置姓名字段为必填"""
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = '姓名'
        self.fields['first_name'].required = True
    
    def save(self, commit=True):
        """
        保存用户时自动设置默认值
        设置学院为环境学院，角色为普通用户
        """
        user = super().save(commit=False)
        user.college = '环境学院'  # 默认学院
        user.department = self.cleaned_data['department']
        user.student_id = self.cleaned_data['student_id']
        user.role = User.Role.APPLICANT  # 默认角色为普通用户，由管理员后续分配
        if commit:
            user.save()
        return user

class ProfileEditForm(forms.ModelForm):
    """
    个人信息编辑表单
    用户可以修改姓名、邮箱、学号、学院、部门
    部门字段使用下拉选择，保持与注册时一致
    """
    class Meta:
        model = User
        fields = ('first_name', 'email', 'student_id', 'college', 'department')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control'}),
            'college': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(choices=DEPARTMENT_CHOICES, attrs={'class': 'form-select'}),
        }
        labels = {
            'first_name': '姓名',
            'email': '邮箱',
            'student_id': '学号',
            'college': '学院',
            'department': '部门',
        }

class PasswordChangeForm(forms.Form):
    """
    密码修改表单
    用户需要输入当前密码和新密码进行验证
    确保密码修改的安全性
    """
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='当前密码'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='新密码',
        min_length=8  # 密码最小长度为8位
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='确认新密码'
    )
    
    def __init__(self, user, *args, **kwargs):
        """初始化表单，保存用户对象用于密码验证"""
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_old_password(self):
        """
        验证当前密码是否正确
        防止未授权用户修改他人密码
        """
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('当前密码不正确')
        return old_password
    
    def clean_new_password2(self):
        """
        验证两次输入的新密码是否一致
        确保用户输入的密码没有错误
        """
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('两次输入的密码不一致')
        return password2
    
    def save(self):
        """
        保存新密码
        使用Django的set_password方法进行密码哈希处理
        """
        self.user.set_password(self.cleaned_data['new_password1'])
        self.user.save()
