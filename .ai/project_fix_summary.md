# YuFuQuant 项目运行修复指南

我分析了您在启动项目时遇到的问题，并提供了两个主要修复方案：

## 1. 后端 Django 设置问题

问题：
```
ModuleNotFoundError: No module named 'config.settings.prod'
```

Django 应用正在尝试加载 `config.settings.prod` 模块，但找不到它。

### 快速修复步骤：

1. 修改 `.envs/.local/.django` 文件，添加正确的设置模块路径：

```bash
# 编辑环境变量文件
nano .envs/.local/.django

# 添加或修改以下行
DJANGO_SETTINGS_MODULE=config.settings.local  # 或者 .base 或 .dev
```

2. 如果需要，修改 `compose/local/django/start.sh` 脚本中的设置模块引用。

3. 重启 Django 容器：
```bash
docker-compose -f local.yml stop django
docker-compose -f local.yml up -d django
```

## 2. 前端 SASS 编译错误

问题：
```
Syntax Error: ReferenceError: globalThis is not defined
```

这是 Node.js 版本和 SASS 版本不兼容导致的问题。

### 快速修复步骤：

1. 修改 `compose/local/node/Dockerfile` 使用更新的 Node.js 版本：

```dockerfile
# 将
FROM node:10  # 或当前版本

# 修改为
FROM node:14  # 或更高版本
```

2. 或者修改 `frontend/package.json` 降级 SASS 版本：

```json
"devDependencies": {
  "sass": "~1.32.13",
  "sass-loader": "^10.1.1",
  // ... 其他依赖
}
```

3. 重建并启动前端容器：
```bash
docker-compose -f local.yml stop node
docker-compose -f local.yml build node
docker-compose -f local.yml up -d node
```

## 3. 对于其他服务

在修复上述问题后，您可能还需要重启其他服务：

```bash
# 启动所有服务
docker-compose -f local.yml down
docker-compose -f local.yml up -d
```

## 4. 监控日志

修复应用后，监控日志检查是否还有其他问题：

```bash
# 查看所有容器日志
docker-compose -f local.yml logs -f

# 或查看特定容器日志
docker-compose -f local.yml logs -f django
docker-compose -f local.yml logs -f node
```

如果您需要更详细的解释，请参考我创建的以下文件：
- `.ai/django_settings_fix.md`: Django 设置详细修复指南
- `.ai/frontend_sass_fix.md`: 前端 SASS 问题详细修复指南 