# MySQL数据库配置说明

## 📋 数据库配置

项目已配置为使用MySQL数据库。

## 🔧 安装MySQL

### Windows系统

1. **下载MySQL**
   - 访问：https://dev.mysql.com/downloads/mysql/
   - 下载MySQL Installer for Windows
   - 安装时选择"Developer Default"或"Server only"

2. **安装MySQL客户端库**
   ```bash
   # 方法1：使用pip安装（需要先安装MySQL客户端）
   pip install mysqlclient
   
   # 如果安装失败，先安装MySQL Connector/C
   # 下载：https://dev.mysql.com/downloads/connector/c/
   ```

### Linux系统（Ubuntu/Debian）

```bash
# 安装MySQL服务器
sudo apt update
sudo apt install mysql-server -y

# 安装MySQL开发库（mysqlclient需要）
sudo apt install default-libmysqlclient-dev build-essential pkg-config -y

# 安装Python MySQL客户端
pip install mysqlclient
```

### Linux系统（CentOS）

```bash
# 安装MySQL服务器
sudo yum install mysql-server -y

# 安装MySQL开发库
sudo yum install mysql-devel gcc python3-devel -y

# 安装Python MySQL客户端
pip install mysqlclient
```

## 🗄️ 创建数据库

### 方法1：使用MySQL命令行

```bash
# 登录MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE reimbursement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 创建用户（可选，推荐）
CREATE USER 'reimbursement_user'@'localhost' IDENTIFIED BY '您的密码';
GRANT ALL PRIVILEGES ON reimbursement_db.* TO 'reimbursement_user'@'localhost';
FLUSH PRIVILEGES;

# 退出
EXIT;
```

### 方法2：使用phpMyAdmin（如果有）

1. 登录phpMyAdmin
2. 创建新数据库：`reimbursement_db`
3. 字符集选择：`utf8mb4`
4. 排序规则选择：`utf8mb4_unicode_ci`

## ⚙️ 配置数据库连接

### 方法1：使用环境变量（推荐）

创建 `.env` 文件（在项目根目录）：
```env
DB_NAME=reimbursement_db
DB_USER=root
DB_PASSWORD=您的MySQL密码
DB_HOST=localhost
DB_PORT=3306
```

然后在 `settings.py` 中加载（需要安装python-dotenv）：
```python
from dotenv import load_dotenv
load_dotenv()
```

### 方法2：直接修改settings.py

编辑 `reimbursement_system/settings.py`，修改数据库配置：
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "reimbursement_db",
        "USER": "root",
        "PASSWORD": "您的密码",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

## 🚀 初始化数据库

```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建管理员（如果需要）
python create_admin.py
```

## 🔍 验证连接

```bash
# 测试数据库连接
python manage.py dbshell

# 如果成功进入MySQL命令行，说明连接正常
```

## ⚠️ 常见问题

### 问题1：mysqlclient安装失败

**Windows解决方案：**
1. 下载预编译的wheel文件：https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
2. 下载对应Python版本的wheel文件
3. 安装：`pip install mysqlclient‑1.4.6‑cp39‑cp39‑win_amd64.whl`

**Linux解决方案：**
```bash
# 确保安装了开发库
sudo apt install default-libmysqlclient-dev  # Ubuntu
sudo yum install mysql-devel  # CentOS
```

### 问题2：字符编码问题

确保数据库使用utf8mb4字符集：
```sql
ALTER DATABASE reimbursement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 问题3：连接被拒绝

检查：
1. MySQL服务是否运行：`sudo systemctl status mysql`
2. 用户权限是否正确
3. 防火墙是否阻止3306端口

## 📝 从SQLite迁移到MySQL

如果之前使用SQLite，需要：

1. **导出数据（可选）**
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **修改数据库配置**（已完成）

3. **重新创建数据库**
   ```bash
   python manage.py migrate
   ```

4. **导入数据（如果有）**
   ```bash
   python manage.py loaddata backup.json
   ```

## 🔐 安全建议

1. **生产环境**：使用专用数据库用户，不要使用root
2. **密码安全**：使用强密码
3. **远程访问**：生产环境建议只允许本地连接
4. **定期备份**：配置自动备份策略


