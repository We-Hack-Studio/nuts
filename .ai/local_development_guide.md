# YuFuQuant 量化交易平台 - 本地开发环境搭建指南

本文档将指导您如何在本地搭建 YuFuQuant 量化交易平台的开发环境，并运行前端和后端服务。

## 先决条件

在开始之前，请确保您已经安装了以下软件：

1. **Docker** 和 **Docker Compose**
   - Docker: 推荐 20.10.x 或更高版本
   - Docker Compose: 推荐 1.29.x 或更高版本
   - 安装指南: [Docker 官方安装指南](https://docs.docker.com/get-docker/)

2. **Git**
   - 用于克隆项目代码
   - 安装指南: [Git 官方安装指南](https://git-scm.com/downloads)

## 克隆项目

```bash
# 克隆项目
git clone https://github.com/your-username/yufuquant.git
cd yufuquant
```

## 环境配置

项目使用 Docker Compose 管理开发环境。在项目根目录下，我们发现了 `local.yml` 文件，它定义了本地开发环境的配置。

### 1. 准备环境变量文件

本项目需要设置环境变量来配置各个服务。检查并创建以下目录结构：

```
.envs/
├── .local/
│   ├── .django
│   └── .postgres
```

- 创建 `.envs/.local/.django` 文件:

```
# General
# ------------------------------------------------------------------------------
USE_DOCKER=yes
IPYTHONDIR=/app/.ipython

# Redis
# ------------------------------------------------------------------------------
REDIS_URL=redis://redis:6379/0

# Celery
# ------------------------------------------------------------------------------
CELERY_BROKER_URL=redis://redis:6379/0
```

- 创建 `.envs/.local/.postgres` 文件:

```
# PostgreSQL
# ------------------------------------------------------------------------------
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=yufuquant
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_URL=postgres://postgres:postgres@postgres:5432/yufuquant
```

## 启动本地开发环境

### 重要：先构建自定义镜像

在运行服务之前，必须先构建自定义镜像（django, celeryworker, celerybeat, node）。这是因为这些服务使用了本地 Dockerfile 进行定义，而不是直接使用公共仓库的镜像：

```bash
# 构建所有需要的自定义镜像
docker-compose -f local.yml build
```

### 使用 Docker Compose 启动所有服务

构建完成后，在项目根目录下运行以下命令启动服务：

```bash
docker-compose -f local.yml up
```

这将启动以下服务：

- Django (后端 API 服务): 监听 8000 端口
- PostgreSQL (数据库): 内部端口 5432
- Redis (缓存和消息队列): 内部端口 6379
- Celery Worker (异步任务处理)
- Celery Beat (定时任务)
- Node (前端开发服务): 监听 8080 端口

要在后台运行所有服务，可以使用：

```bash
docker-compose -f local.yml up -d
```

### 分别启动前端和后端（可选）

如果您希望分别启动前后端服务，可以按照以下步骤操作：

#### 仅启动后端

```bash
docker-compose -f local.yml up django postgres redis celeryworker celerybeat
```

#### 仅启动前端

```bash
docker-compose -f local.yml up node
```

## 访问服务

- **Django 后端 API**: http://localhost:8000/api/
- **Vue.js 前端应用**: http://localhost:8080/

## 常用操作

### 检查服务状态

```bash
docker-compose -f local.yml ps
```

### 查看服务日志

查看所有服务的日志：
```bash
docker-compose -f local.yml logs
```

查看特定服务的日志：
```bash
docker-compose -f local.yml logs django
```

跟踪日志输出：
```bash
docker-compose -f local.yml logs -f
```

### 执行 Django 管理命令

```bash
docker-compose -f local.yml exec django python manage.py <command>
```

例如，创建超级用户：
```bash
docker-compose -f local.yml exec django python manage.py createsuperuser
```

应用数据库迁移：
```bash
docker-compose -f local.yml exec django python manage.py migrate
```

### 进入容器 Shell

进入 Django 容器：
```bash
docker-compose -f local.yml exec django bash
```

进入 PostgreSQL 容器：
```bash
docker-compose -f local.yml exec postgres bash
```

### 访问数据库

```bash
docker-compose -f local.yml exec postgres psql -U postgres -d yufuquant
```

### 重建容器

如果您对 Dockerfile 或依赖做了更改，需要重建容器：
```bash
docker-compose -f local.yml build
```

### 停止所有服务

```bash
docker-compose -f local.yml down
```

## 开发流程

### 后端开发（Django）

1. 代码位于 `yufuquant/` 目录下
2. 修改代码后，Django 开发服务器会自动重载
3. 可通过 Django 管理界面 (http://localhost:8000/admin/) 访问后台
4. API 文档（如果已配置）可能位于 http://localhost:8000/api/docs/

### 前端开发（Vue.js）

1. 代码位于 `frontend/` 目录下
2. 修改代码后，Vue 开发服务器会自动重载
3. 前端服务运行在 http://localhost:8080/

## 可能遇到的问题及解决方案

### 镜像拉取错误

如果您看到类似以下错误：

```
WARNING: pull access denied for yufuquant_local_django, repository does not exist or may require 'docker login'
```

这表明 Docker 正在尝试拉取镜像而不是构建它。解决方法：

1. 确保已运行构建命令：
   ```bash
   docker-compose -f local.yml build
   ```

2. 如果问题仍然存在，尝试使用 `--no-cache` 参数重新构建：
   ```bash
   docker-compose -f local.yml build --no-cache
   ```

3. 如果某个特定的服务无法启动，可以单独构建并启动它：
   ```bash
   docker-compose -f local.yml build django
   docker-compose -f local.yml up django
   ```

### 端口冲突

如果 8000 或 8080 端口已被占用，您可以通过以下方式修改：

- 对于前端 (Node)，可以设置环境变量 `PORT`：
  ```bash
  PORT=8081 docker-compose -f local.yml up node
  ```

- 对于后端，需要修改 `local.yml` 文件中的端口映射配置。

### 权限问题

在 Linux 系统上，可能会遇到文件权限问题。尝试以下解决方案：

```bash
sudo chown -R $USER:$USER .
```

### 数据库迁移问题

如果遇到数据库迁移错误，请尝试重置数据库：

```bash
docker-compose -f local.yml down
docker volume rm yufuquant_local_postgres_data
docker-compose -f local.yml up -d
```

然后重新应用迁移：
```bash
docker-compose -f local.yml exec django python manage.py migrate
```

## 结论

恭喜！您现在应该已经成功地在本地运行了 YuFuQuant 量化交易平台的前端和后端服务。开始您的开发工作吧！

如果您在设置过程中遇到任何问题，请查阅项目文档或联系项目维护者。 