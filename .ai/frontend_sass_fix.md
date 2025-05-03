# 前端 SASS 错误修复指南

## 问题

在启动前端服务时，出现了以下错误：

```
Syntax Error: ReferenceError: globalThis is not defined
```

同时，还有大量 SASS 相关的警告，比如：
- 关于 `lighten()` 函数使用的弃用警告
- 关于 `abs()` 函数和百分比单位的弃用警告
- 关于 `mixed-decls` 的弃用警告
- 关于 `/` 用于除法的弃用警告

这些问题主要是因为：
1. 项目使用的 Node.js 版本可能太旧，不支持 `globalThis`
2. 使用的 SASS 版本与项目中的 Bootstrap SASS 代码不兼容

## 解决方案

### 解决 Node 版本问题

1. 修改 `compose/local/node/Dockerfile` 以使用更新的 Node.js 版本：

```dockerfile
# 原始行
FROM node:10  # 或者什么版本

# 修改为
FROM node:14  # 推荐使用 Node.js 14 或更高版本
```

### 降级 SASS 版本

1. 修改 `frontend/package.json` 中的 SASS 版本：

```json
"devDependencies": {
  // ... 其他依赖
  "sass": "~1.32.13",  // 将版本固定在兼容的版本
  "sass-loader": "^10.1.1",  // 降级 sass-loader
  // ... 其他依赖
}
```

### 应用修改

1. 停止前端容器：
```bash
docker-compose -f local.yml stop node
```

2. 重建前端容器：
```bash
docker-compose -f local.yml build node
```

3. 启动前端服务：
```bash
docker-compose -f local.yml up node
```

### 注意事项

- Bootstrap 4.x 的 SASS 文件使用了一些在新版 SASS 中已弃用的功能，因此降级到兼容版本是更简单的解决方案
- 如果仍有问题，可以进入容器并手动执行 npm 安装命令：
```bash
docker-compose -f local.yml exec node bash
cd /app
npm install sass@~1.32.13 sass-loader@^10.1.1 --save-dev
npm run serve
```

弃用警告通常不会阻止应用运行，除非有语法错误。降级 SASS 版本是简单的权宜之计，长期解决方案应该是更新项目代码以适应最新的 SASS 语法。 