from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# 预定义的部门列表
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
    """用户注册表单，扩展Django默认注册表单，添加学号、部门等字段"""
    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='部门',
        help_text='请选择您所在的部门'
    )
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
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = '姓名'
        self.fields['first_name'].required = True
    
    def save(self, commit=True):
        """保存用户时自动设置默认值：学院为环境学院，角色为普通用户"""
        user = super().save(commit=False)
        user.college = '环境学院'  # 默认学院，根据需求文档
        user.department = self.cleaned_data['department']
        user.student_id = self.cleaned_data['student_id']
        user.role = User.Role.APPLICANT  # 默认角色，后续由管理员分配
        if commit:
            user.save()
        return user

class ProfileEditForm(forms.ModelForm):
    """个人信息编辑表单，用户可以修改姓名、邮箱、学号、学院、部门"""
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
    """密码修改表单，用户需要输入当前密码和新密码进行验证"""
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='当前密码'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='新密码',
        min_length=8
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='确认新密码'
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_old_password(self):
        """验证当前密码是否正确"""
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('当前密码不正确')
        return old_password
    
    def clean_new_password2(self):
        """验证两次输入的新密码是否一致"""
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('两次输入的密码不一致')
        return password2
    
    def save(self):
        """保存新密码"""
        self.user.set_password(self.cleaned_data['new_password1'])
        self.user.save()


