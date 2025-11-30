# 报销神表 - 第二周代码

## 📋 代码说明

本文件夹包含第二周开发的所有代码，是在第一周代码基础上的扩充。

---

## 🔧 主要修改

### 1. 修复SECRET_KEY安全问题
- **文件**: `reimbursement_system/settings.py`
- **修改**: 移除硬编码的SECRET_KEY，改为从环境变量读取
- **说明**: 提高安全性，符合代码规范要求

### 2. 新增报销申请功能
- **新增应用**: `claims` 应用
- **主要文件**:
  - `claims/models.py`: 报销单、明细、发票数据模型
  - `claims/forms.py`: 报销表单和文件上传表单
  - `claims/views.py`: 报销单创建、编辑、查看视图
  - `claims/urls.py`: 报销相关URL路由
  - `claims/admin.py`: Django管理后台配置

### 3. Bug修复
- 修复报销单总金额不更新问题
- 修复删除明细后总金额未更新
- 修复负责人无法查看本部门报销单
- 修复已驳回报销单无法编辑
- 修复报销单详情权限检查错误
- 配置文件上传大小限制

---

## 📁 文件结构

```
Week2/代码/
├── reimbursement_system/
│   ├── settings.py          # 配置文件（已修复SECRET_KEY）
│   └── urls.py              # URL路由配置
├── users/                   # 用户应用（第一周代码）
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── admin.py
├── claims/                  # 报销应用（第二周新增）
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── create_admin.py          # 创建管理员脚本
└── requirements.txt         # 依赖包列表
```

---

## 🚀 使用方法

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量（可选）
```bash
# Windows PowerShell
$env:SECRET_KEY="your-secret-key-here"
$env:DB_NAME="reimbursement_db"
$env:DB_USER="root"
$env:DB_PASSWORD="your-password"

# Linux/Mac
export SECRET_KEY="your-secret-key-here"
export DB_NAME="reimbursement_db"
export DB_USER="root"
export DB_PASSWORD="your-password"
```

### 3. 初始化数据库
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建管理员
```bash
python create_admin.py
```

### 5. 启动服务器
```bash
python manage.py runserver
```

---

## 📝 功能清单

### ✅ 已实现功能
- [x] 用户注册、登录、登出
- [x] 个人信息编辑
- [x] 用户角色管理（管理员功能）
- [x] 创建报销单
- [x] 编辑报销单（草稿/已驳回）
- [x] 查看报销单详情
- [x] 报销单列表（仪表盘）
- [x] 暂存功能
- [x] 多文件上传

### 🚧 待开发功能（第三周）
- [ ] 报销负责人审核功能
- [ ] Excel导出功能
- [ ] Word导出功能
- [ ] 发票打包下载

---

## 🐛 已知Bug修复

详细Bug记录请查看 `Week2/文档/Bug记录.md`

主要修复的Bug：
1. ✅ 报销单总金额不更新（Bug #005）
2. ✅ 删除明细后总金额未更新（Bug #006）
3. ✅ 负责人无法查看本部门报销单（Bug #007）
4. ✅ 已驳回报销单无法编辑（Bug #008）
5. ✅ 报销单详情权限检查错误（Bug #009）
6. ✅ 文件上传大小限制未配置（Bug #010）

---

## 📚 相关文档

- **功能说明**: `Week2/文档/功能说明.md`
- **Bug记录**: `Week2/文档/Bug记录.md`
- **API说明**: `Week2/文档/API说明.md`
- **Git规范**: `Week2/文档/Git分支管理和Commit规范.md`

---

## ⚠️ 注意事项

1. **SECRET_KEY**: 生产环境必须设置环境变量，不要使用默认值
2. **数据库密码**: 开发环境可以硬编码，生产环境应使用环境变量
3. **文件上传**: 单文件限制10MB，建议上传PDF格式
4. **权限控制**: 确保只有有权限的用户才能访问相应功能

---

## 🔄 与第一周代码的差异

1. **新增claims应用**: 完整的报销申请功能
2. **修复SECRET_KEY**: 改为从环境变量读取
3. **修复多个Bug**: 详见Bug记录文档
4. **添加文件上传限制**: 在settings.py中配置
5. **完善权限检查**: 修复多个权限相关问题

---

## 📞 问题反馈

如遇到问题，请查看：
1. Bug记录文档
2. API说明文档
3. 功能说明文档

或联系开发团队。
