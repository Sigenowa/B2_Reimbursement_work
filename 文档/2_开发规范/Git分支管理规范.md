# 🌳 Git分支管理规范

## 📋 分支策略

采用 [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/) 工作流：

```
main (主分支)
├── develop (开发分支)
│   ├── feature/user-auth (功能分支)
│   ├── feature/claims-mgmt (功能分支)
│   ├── bugfix/validation (修复分支)
│   └── release/v1.0 (发布分支)
```

## 🔀 分支说明

### 永久分支

#### main
- **用途**: 生产环境代码
- **保护**: 只能通过PR合并
- **部署**: 自动部署到生产环境

#### develop
- **用途**: 开发主分支
- **状态**: 包含所有已完成的开发内容
- **合并**: 从feature分支合并

### 临时分支

#### feature/*
- **命名**: `feature/功能名称`
- **用途**: 新功能开发
- **来源**: develop分支
- **目标**: develop分支
- **示例**:
  - `feature/user-management`
  - `feature/claims-system`
  - `feature/deployment`

#### bugfix/*
- **命名**: `bugfix/问题描述`
- **用途**: bug修复
- **来源**: develop分支
- **目标**: develop分支
- **示例**:
  - `bugfix/login-validation`
  - `bugfix/amount-calculation`

#### hotfix/*
- **命名**: `hotfix/紧急修复`
- **用途**: 生产环境紧急修复
- **来源**: main分支
- **目标**: main和develop分支

#### release/*
- **命名**: `release/v版本号`
- **用途**: 发布准备
- **来源**: develop分支
- **目标**: main分支

## 🚀 工作流程

### 开发新功能

```bash
# 1. 从develop创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# 2. 开发功能
# ... 编写代码

# 3. 提交代码（遵循commit规范）
git add .
git commit -m "feat: 实现新功能

- 功能描述
- 实现细节

Closes #123"

# 4. 推送分支
git push origin feature/new-feature

# 5. 创建Pull Request
# 在GitHub上创建PR，目标分支为develop
```

### 修复Bug

```bash
# 1. 创建修复分支
git checkout develop
git checkout -b bugfix/issue-description

# 2. 修复问题
# ... 修复代码

# 3. 提交修复
git add .
git commit -m "fix: 修复XXX问题

- 问题描述
- 修复方案

Fixes #456"

# 4. 创建PR
git push origin bugfix/issue-description
```

### 发布版本

```bash
# 1. 从develop创建release分支
git checkout develop
git checkout -b release/v1.0

# 2. 最终测试和调整
# ... 版本号更新、文档更新等

# 3. 合并到main
git checkout main
git merge release/v1.0

# 4. 打标签
git tag -a v1.0 -m "Release version 1.0"

# 5. 推送
git push origin main --tags

# 6. 合并回develop
git checkout develop
git merge release/v1.0

# 7. 删除release分支
git branch -d release/v1.0
```

## 📝 Commit规范

### 格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 工具配置

### 示例
```
feat(auth): 实现JWT用户认证

- 添加JWT token生成和验证
- 集成用户登录接口
- 更新API文档

Closes #123
```

## 🛡️ 分支保护

### main分支保护规则
- 需要PR审批
- 需要CI通过
- 不允许直接推送
- 需要至少1个审查者

### develop分支保护规则
- 需要PR审批
- 需要CI通过
- 允许直接推送（开发者）

## 🔍 代码审查

### PR要求
- [ ] 遵循commit规范
- [ ] 包含测试代码
- [ ] 更新相关文档
- [ ] 通过CI检查
- [ ] 有意义的PR描述

### 审查要点
- 代码质量和规范
- 功能完整性
- 测试覆盖率
- 文档更新
- 安全考虑

## 📊 分支命名规范

### 功能分支
```
feature/login-system
feature/user-profile
feature/claims-workflow
```

### Bug修复分支
```
bugfix/validation-error
bugfix/permission-check
bugfix/amount-calculation
```

### 发布分支
```
release/v1.0.0
release/v1.1.0
```

## 🎯 最佳实践

1. **保持分支简洁**: 每个分支只做一件事
2. **及时同步**: 定期从develop拉取最新代码
3. **小步提交**: 频繁提交，避免大块变更
4. **清晰描述**: PR和commit信息要清晰明了
5. **代码审查**: 所有代码都需要审查
6. **自动化测试**: 确保CI/CD正常工作

## 📞 常见问题

### Q: 什么时候创建feature分支？
A: 当开始开发新功能或进行较大重构时

### Q: bugfix和hotfix的区别？
A: bugfix用于开发中的bug，hotfix用于生产环境的紧急修复

### Q: 如何处理冲突？
A: 先拉取最新代码，解决冲突后再提交

### Q: 谁来合并到main？
A: 项目负责人或指定的人员






