# 第4周完整代码文件说明

## 📁 文件结构

```
Week4/代码/
├── manage.py                    # Django管理脚本
├── create_admin.py             # 管理员创建脚本
├── requirements.txt            # 项目依赖
├── run_server.sh              # Linux/Mac启动脚本
├── get_ip.bat                  # Windows IP获取脚本
├── reimbursement_system/       # Django项目配置
│   ├── __init__.py
│   ├── settings.py            # 项目设置（MySQL配置）
│   ├── urls.py                # 主URL配置
│   ├── wsgi.py
│   └── asgi.py
├── users/                      # 用户管理系统应用
│   ├── __init__.py
│   ├── admin.py                # 管理后台配置
│   ├── apps.py
│   ├── forms.py                # 用户表单
│   ├── models.py               # 用户数据模型
│   ├── views.py                # 用户视图逻辑
│   ├── urls.py                 # 用户URL配置
│   ├── migrations/             # 数据库迁移文件
│   └── tests.py
├── claims/                     # 报销管理系统应用
│   ├── __init__.py
│   ├── admin.py                # 报销管理后台
│   ├── apps.py
│   ├── forms.py                # 报销表单
│   ├── models.py               # 报销数据模型
│   ├── views.py                # 报销视图逻辑
│   ├── urls.py                 # 报销URL配置
│   ├── migrations/             # 数据库迁移文件
│   └── tests.py
├── templates/                  # 前端模板文件
│   ├── base.html              # 基础模板（导航栏、样式）
│   ├── users/                 # 用户页面模板
│   │   ├── login.html         # 登录页面
│   │   ├── register.html      # 注册页面
│   │   ├── profile_edit.html  # 个人信息编辑
│   │   └── user_management.html # 用户管理
│   └── claims/                # 报销页面模板
│       └── reimbursement_form.html # 报销申请表单
├── static/                     # 静态文件目录
├── local_deploy.bat           # Windows本地部署脚本
├── local_deploy.sh            # Linux/Mac本地部署脚本
├── start_server.bat          # Windows服务器启动脚本
├── start_server.sh           # Linux/Mac服务器启动脚本
├── mysql_setup.bat            # MySQL配置脚本
├── db_init.py                 # 数据库初始化脚本
├── 本地部署指南.md             # 详细部署说明
├── 局域网访问配置.md           # 网络访问配置指南
└── 快速开始.md                 # 5分钟上手指南
```

## 🎯 第4周完成功能

### 1. 完整用户管理系统
- 用户注册、登录、登出
- 个人信息编辑
- 用户角色管理（管理员功能）
- 多部门支持（文艺部、体育部等）

### 2. 完整报销管理系统
- 报销单创建和编辑
- 动态添加报销明细
- 文件上传（发票凭证）
- 报销单状态管理（草稿、待处理、已打包、已驳回）
- 报销单审核（负责人功能）

### 3. 本地部署和运行
- MySQL数据库支持
- 自动环境配置
- 一键部署脚本
- 局域网访问支持
- 移动设备访问

### 4. 前端界面
- 响应式Bootstrap设计
- 中文界面完全本地化
- 现代化企业级UI
- 移动端友好

## 📝 使用说明

### 快速开始（推荐）
1. 双击 `快速开始.md` 查看详细指南
2. 运行 `local_deploy.bat` 自动部署
3. 运行 `start_server.bat` 启动服务器
4. 在浏览器访问显示的地址

### 手动部署
1. 安装Python 3.9+
2. 运行 `pip install -r requirements.txt`
3. 安装并配置MySQL（或使用SQLite）
4. 运行 `python manage.py migrate`
5. 运行 `python create_admin.py` 创建管理员
6. 运行 `python manage.py runserver 0.0.0.0:8000`

## ✅ 验收标准

- [x] 用户注册登录功能正常
- [x] 报销申请功能完整
- [x] 文件上传下载正常
- [x] 管理员功能正常
- [x] 本地部署成功
- [x] 局域网访问正常
- [x] 移动设备访问正常
- [x] 前端界面美观

## 🔧 技术栈

- **后端**: Django 4.2 (Python Web框架)
- **数据库**: MySQL 8.0 / SQLite (自动切换)
- **前端**: Bootstrap 5.3 + Django Templates
- **部署**: 本地开发服务器 + 局域网访问

## 📞 支持

如遇到问题，请查看：
1. `本地部署指南.md` - 详细部署说明
2. `局域网访问配置.md` - 网络访问配置
3. `快速开始.md` - 5分钟上手指南</content>
</xai:function_call"><xai:function_call name="run_terminal_cmd">
<parameter name="command">cd Week4\代码 && dir /b