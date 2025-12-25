# 📋 报销神表 - 服务器部署版本

> 一个支持多用户协作的在线报销单管理系统

## 🌟 功能特性

- **用户管理**：注册、登录、角色分配（普通用户/报销负责人/系统管理员）
- **报销申请**：创建、编辑、提交报销单，支持物品明细和发票上传
- **审核流程**：负责人审核报销单，支持通过/驳回
- **数据导出**：将报销单导出为Excel + Word + 发票ZIP包
- **多端访问**：支持PC和移动端浏览器访问

## 🖥️ 服务器信息

| 配置 | 值 |
|------|-----|
| **服务器IP** | 101.43.149.245 |
| **访问地址** | http://101.43.149.245 |
| **用户名** | ubuntu |

## 📁 项目结构

```
Week5/代码/
├── claims/                 # 报销管理应用
│   ├── models.py          # 报销单、明细、发票模型
│   ├── views.py           # 视图函数
│   ├── forms.py           # 表单类
│   └── urls.py            # URL路由
├── users/                  # 用户管理应用
│   ├── models.py          # 自定义用户模型
│   ├── views.py           # 注册、登录、用户管理视图
│   └── forms.py           # 注册、编辑表单
├── reimbursement_system/   # 项目配置
│   ├── settings.py        # Django设置（支持服务器部署）
│   ├── urls.py            # 主URL路由
│   └── wsgi.py            # WSGI入口
├── templates/              # HTML模板
│   ├── base.html          # 基础模板
│   ├── dashboard.html     # 仪表盘
│   ├── claims/            # 报销相关模板
│   └── users/             # 用户相关模板
├── deploy/                 # 部署配置
│   ├── nginx.conf         # Nginx配置
│   ├── reimbursement.service  # systemd服务
│   ├── deploy.sh          # 自动部署脚本
│   └── mysql_setup.sql    # 数据库初始化
├── manage.py              # Django管理脚本
├── requirements.txt       # Python依赖
├── gunicorn.conf.py       # Gunicorn配置
└── 服务器部署指南.md       # 详细部署文档
```

## 🚀 快速开始

### 本地开发

```bash
# 1. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. 安装依赖
pip install -r requirements.txt

# 3. 使用SQLite进行开发
export USE_SQLITE=true
export DEBUG=true

# 4. 数据库迁移
python manage.py migrate

# 5. 创建管理员
python create_admin.py

# 6. 启动开发服务器
python manage.py runserver 0.0.0.0:8000
```

### 服务器部署

详见 [服务器部署指南.md](服务器部署指南.md)

```bash
# SSH连接服务器
ssh ubuntu@101.43.149.245

# 运行部署脚本
bash deploy/deploy.sh
```

## 🔧 技术栈

| 组件 | 技术 |
|------|------|
| **后端** | Django 4.2 |
| **数据库** | MySQL (生产) / SQLite (开发) |
| **Web服务器** | Nginx + Gunicorn |
| **前端** | Bootstrap 5 + Bootstrap Icons |
| **进程管理** | systemd |

## 👥 用户角色

| 角色 | 权限 |
|------|------|
| **普通用户** | 创建、编辑、查看自己的报销单 |
| **报销负责人** | 审核本部门报销单、导出报销数据 |
| **系统管理员** | 管理用户、分配角色 |

## 📝 API端点

| 路径 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 仪表盘（需登录） |
| `/login/` | GET/POST | 用户登录 |
| `/register/` | GET/POST | 用户注册 |
| `/claims/create/` | GET/POST | 创建报销单 |
| `/claims/edit/<id>/` | GET/POST | 编辑报销单 |
| `/claims/detail/<id>/` | GET | 查看报销单详情 |
| `/claims/review/<id>/` | POST | 审核报销单 |
| `/claims/export/` | GET | 导出报销数据 |
| `/users/` | GET | 用户管理（管理员） |

## 🔒 安全配置

- SECRET_KEY 从环境变量读取
- 生产环境 DEBUG=False
- CSRF 保护已启用
- 密码经过哈希处理
- 会话超时设置为24小时

## 📞 联系方式

如有问题，请联系项目维护人员。

---

**版本**: Week 5 - 服务器部署版本  
**最后更新**: 2025年1月
