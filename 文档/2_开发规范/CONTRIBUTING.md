# 🤝 贡献指南

## 📋 开发流程

### 1. 创建功能分支

```bash
# 从develop分支创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# 或者修复分支
git checkout -b bugfix/issue-description
```

### 2. 提交代码

```bash
# 添加文件
git add .

# 提交（遵循规范）
git commit -m "feat: 添加新功能

- 详细描述变更内容
- 列出主要修改点

Closes #123"
```

### 3. 推送分支

```bash
git push origin feature/your-feature-name
```

### 4. 创建Pull Request

在GitHub上创建PR，目标分支为 `develop`

## 📝 Commit消息规范

### 格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建工具变动

### 示例
```
feat(users): 添加用户注册功能

- 实现用户注册表单
- 添加邮箱验证
- 集成角色分配逻辑

Closes #42
```

```
fix(claims): 修复报销单计算错误

修正了明细金额累加时的浮点数精度问题，
确保计算结果准确性。
```

## 🔀 分支管理

### 主分支
- `main`: 生产环境代码
- `develop`: 开发主分支

### 功能分支
- `feature/*`: 新功能开发
- `bugfix/*`: bug修复
- `hotfix/*`: 紧急修复
- `release/*`: 发布准备

### 工作流程
1. 从 `develop` 创建功能分支
2. 在功能分支上开发
3. 提交PR到 `develop`
4. 测试通过后合并
5. 定期从 `develop` 合并到 `main` 发布

## 🧪 测试要求

- 新功能必须包含单元测试
- 修改现有功能需要更新相关测试
- 所有测试必须通过
- 代码覆盖率不低于80%

## 📚 代码规范

- 遵循PEP 8 Python代码规范
- 使用有意义的变量和函数名
- 添加必要的注释
- 保持代码简洁可读






