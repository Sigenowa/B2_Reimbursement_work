# Git提交优化指南

## 为什么提交更改时间这么长？

### 主要原因

1. **大文件问题**
   - `media/invoices/` 目录下的PDF文件（用户上传的发票）
   - `需求规格说明书-报销神表.doc`（Word文档）
   - `Week2.zip`（压缩文件）
   - `db.sqlite3`（数据库文件，可能很大）

2. **不应该提交的文件**
   - `__pycache__/` 目录（Python缓存文件）
   - `*.pyc` 文件（编译后的Python文件）
   - `db.sqlite3`（数据库文件，包含用户数据）
   - `media/` 目录（用户上传的文件）

3. **网络问题**
   - GitHub服务器访问速度慢
   - 大文件上传需要很长时间

---

## 解决方案

### 方案1：使用.gitignore排除文件（推荐）

我已经为您创建了 `.gitignore` 文件，它会自动排除以下文件：

- ✅ Python缓存文件（`__pycache__/`）
- ✅ 数据库文件（`db.sqlite3`）
- ✅ 用户上传的文件（`media/`）
- ✅ 大文件（`.doc`, `.pdf`, `.zip`等）
- ✅ 虚拟环境（`venv/`）
- ✅ IDE配置文件

**使用方法**：

```bash
# 1. 如果已经提交了这些文件，需要从Git中移除（但保留本地文件）
git rm -r --cached __pycache__/
git rm --cached db.sqlite3
git rm -r --cached media/
git rm --cached "需求规格说明书-报销神表.doc"
git rm --cached Week2.zip

# 2. 提交.gitignore和这些更改
git add .gitignore
git commit -m "chore: 添加.gitignore，排除不需要提交的文件"

# 3. 推送到远程
git push origin main
```

### 方案2：分批提交

如果文件已经很大，可以分批提交：

```bash
# 只提交代码文件
git add *.py
git add templates/
git add static/
git commit -m "feat: 提交代码文件"

# 然后提交文档（如果必须提交）
git add *.md
git commit -m "docs: 提交文档"

# 最后推送
git push origin main
```

### 方案3：使用Git LFS（大文件存储）

如果必须提交大文件，可以使用Git LFS：

```bash
# 安装Git LFS
git lfs install

# 跟踪大文件类型
git lfs track "*.pdf"
git lfs track "*.doc"
git lfs track "*.zip"

# 提交
git add .gitattributes
git commit -m "chore: 配置Git LFS"
```

---

## 最佳实践

### 1. 不应该提交到Git的文件

- ❌ 数据库文件（`db.sqlite3`）
- ❌ 用户上传的文件（`media/`）
- ❌ Python缓存（`__pycache__/`）
- ❌ 虚拟环境（`venv/`）
- ❌ 环境变量文件（`.env`）
- ❌ 大文件（文档、压缩包等）

### 2. 应该提交的文件

- ✅ 源代码（`.py`文件）
- ✅ 模板文件（`templates/`）
- ✅ 静态文件（`static/`）
- ✅ 配置文件（`settings.py`，但不包含敏感信息）
- ✅ 文档（`.md`文件）
- ✅ 依赖文件（`requirements.txt`）

### 3. 数据库处理

**开发环境**：
- 使用SQLite，但不要提交`db.sqlite3`
- 提交数据库迁移文件（`migrations/`）

**生产环境**：
- 使用MySQL或PostgreSQL
- 数据库配置通过环境变量管理

### 4. 用户上传文件处理

- 不要提交`media/`目录到Git
- 在生产环境单独配置文件存储
- 使用云存储（如OSS、S3）或服务器本地存储

---

## 快速检查命令

### 查看仓库大小

```bash
# 查看Git仓库大小
git count-objects -vH

# 查看最大的文件
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | awk '/^blob/ {print substr($0,6)}' | sort --numeric-sort --key=2 | tail -10
```

### 查看未跟踪的文件

```bash
git status
```

### 查看.gitignore是否生效

```bash
# 检查哪些文件会被忽略
git status --ignored
```

---

## 如果已经提交了大文件怎么办？

### 从Git历史中移除大文件

```bash
# 1. 使用git filter-branch（不推荐，复杂）

# 2. 使用BFG Repo-Cleaner（推荐）
# 下载：https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files 大文件名
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 3. 强制推送（注意：会重写历史）
git push origin main --force
```

**警告**：如果已经推送到远程，移除大文件需要强制推送，可能会影响其他协作者。

---

## 推荐操作步骤

1. **立即操作**：
   ```bash
   # 添加.gitignore
   git add .gitignore
   git commit -m "chore: 添加.gitignore文件"
   
   # 从Git中移除不应该提交的文件
   git rm -r --cached __pycache__/
   git rm --cached db.sqlite3
   git rm -r --cached media/
   git commit -m "chore: 移除不应该提交的文件"
   
   # 推送
   git push origin main
   ```

2. **后续开发**：
   - 使用`.gitignore`自动排除文件
   - 只提交源代码和必要文件
   - 定期检查仓库大小

---

## 总结

提交慢的主要原因是：
1. ✅ **大文件**：PDF、Word、ZIP等
2. ✅ **不应该提交的文件**：数据库、缓存、用户上传文件
3. ✅ **网络问题**：GitHub访问速度

**解决方案**：
- ✅ 使用`.gitignore`排除文件
- ✅ 从Git中移除已提交的大文件
- ✅ 只提交必要的源代码文件

**文档创建时间**: 2025-11-24









