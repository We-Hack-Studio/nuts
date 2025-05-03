强烈推荐使用 [Docker](https://www.docker.com/) 无痛部署渔夫量化系统！

## 部署方式

本系统支持两种部署方式：
- 本地开发环境部署（使用`local.yml`）
- 生产环境部署（使用`production.yml`）

## 准备工作

- 一台可安装 Docker 的计算机，推荐使用云服务器（生产环境）或本地机器（开发环境）。
- 一个域名（生产环境可选）。

!!! attention "注意"
    在非公网访问的环境下部署，可以不用域名。如果在可公网访问的服务器上部署，强烈建议配置域名。配置域名才可开启 HTTPS 安全访问。

!!! hint "云服务器推荐"
    阿里云香港节点轻量云服务器仅需 24元/月，足以运行渔夫量化系统。腾讯云、华为云也有类似产品，购买前可加我微信（terryso）咨询，可获得进一步的折扣优惠。

## 安装 Docker

如果使用阿里云轻量应用服务器，只需依次执行以下命令即可安装 Docker。

1. 更新 apt 包索引
    ```bash
    sudo apt-get update
    ```

2. 安装一些辅助工具
    ```bash
    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common
    ```
3. 添加 Docker 官方 GPG key
    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ```

4. 再次更新 apt 包索引
    ```bash
    sudo apt-get update
    ```

5. 安装 Docker
    ```bash
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    ```

6. 验证 Docker 结果
    ```bash
    sudo docker run hello-world
    ```
    运行不报错说明安装成功。
    
7. 将用户加入 docker 组，注意将 `your-user` 替换为当前系统用户名。
    ```bash
    sudo usermod -aG docker your-user
    ```
    这样就不用在每次执行 docker 命令前加 sudo 了。

!!! hint ""
    其他操作系统安装 Docker 的方式都大同小异，详细步骤可参考下方列出的官方文档：
    
    - [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
    - [Install Docker Engine on CentOS](https://docs.docker.com/engine/install/centos/)
    - [Install Docker Desktop on Windows](https://docs.docker.com/docker-for-windows/install/)
    - [Install Docker Desktop on Mac](https://docs.docker.com/docker-for-mac/install/)

## 安装 Docker Compose

如果使用阿里云轻量应用服务器，只需依次执行以下命令即可安装 Docker Compose。

1. 下载 Docker Compose
    ```bash
    sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```

2. 赋予 docker-compose 可执行权限
    ```bash
    sudo chmod +x /usr/local/bin/docker-compose
    ```

3. 查看 docker-compose 版本号，验证安装结果
    ```bash
    docker-compose -v
    ```

## 下载代码
使用 Git 拉取渔夫量化系统最新代码。

```bash
git clone https://github.com/We-Hack-Studio/nuts
```

## 本地开发环境部署

如果你需要在本地进行开发和测试，可以使用`local.yml`配置进行部署。

### 准备环境变量文件

首先创建必要的环境变量文件：

1. 在项目根目录下创建`.envs/.local/`目录：
   ```bash
   mkdir -p .envs/.local/
   ```

2. 创建`.envs/.local/.django`文件：
   ```
   # General
   USE_DOCKER=yes
   DJANGO_SETTINGS_MODULE=config.settings.local
   IPYTHONDIR=/app/.ipython
   
   # Redis
   REDIS_URL=redis://redis:6379/0
   
   # Celery
   CELERY_BROKER_URL=redis://redis:6379/0
   ```

3. 创建`.envs/.local/.postgres`文件：
   ```
   # PostgreSQL
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   POSTGRES_DB=yufuquant
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   DATABASE_URL=postgres://postgres:postgres@postgres:5432/yufuquant
   ```

### 构建和启动本地开发环境

1. 构建必要的Docker镜像：
   ```bash
   docker-compose -f local.yml build
   ```

2. 启动所有服务：
   ```bash
   docker-compose -f local.yml up -d
   ```

3. 访问服务：
   - 后端API服务：http://localhost:8000/api/
   - 前端应用：http://localhost:8080/

### 本地开发常用命令

查看服务状态：
```bash
docker-compose -f local.yml ps
```

查看服务日志：
```bash
docker-compose -f local.yml logs
```

执行Django管理命令：
```bash
docker-compose -f local.yml exec django python manage.py [command]
```

停止所有服务：
```bash
docker-compose -f local.yml down
```

## 生产环境部署

以下为生产环境部署的步骤：

### 配置 Nginx

!!! hint ""
    如果不配置域名，可直接跳过此步骤。

将 yufuquant/compose/production/nginx/conf.d 目录下的 yufuquant.conf.template 文件复制一份到同级目录，新复制的文件命名为 yufuquant.conf。

yufuquant.conf 配置文件部分内容如下：

```{nginx hl_lines="7" linenums="1"}
upstream django  {
    server django:8000;
}

server {
    listen 80 default_server;
    server_name _;
  	# ...
}
```

将第 7 行的下划线 `_` 改为域名，例如：

```nginx
server_name demo.yufuquant.cc;
```

!!! important "注意"
    请确保已将配置的域名解析到部署渔夫系统的服务器。

### 配置接口地址

配置后端 API 接口请求地址。

将 yufuquant/frontend/dist 目录下的 config.example.js 文件复制一份到同级目录，新复制的文件命名为 config.js。

config.js 配置文件初始内容如下：

```javascript
window.conf = {
    restApiBaseUrl: 'http://127.0.0.1:8000/api/v1',
    websocketApiUri: 'ws://127.0.0.1:8000/ws/v1/streams/'
}
```

请根据不同的部署环境进行修改：

=== "本地部署"
    无需修改。

=== "公网未配置域名"
    将 127.0.0.1 改为公网 ip。

=== "公网配置域名"

    - 将 http://127.0.0.1:8000 改为 https://域名。
    - 将 ws://127.0.0.1:8000 改为 wss://域名。
    
    例如修改后的配置如下：
    ```javascript
    window.conf = {
        restApiBaseUrl: 'https://demo.yufuquant.cc/api/v1',
        websocketApiUri: 'wss://demo.yufuquant.cc/ws/v1/streams/'
    }
    ```

### 配置环境变量

在将项目根目录 yufuquant 下的 .envs 目录下创建一个 .production 文件夹，并在 .production 文件夹下创建 .django 和 .postgres 文件，分别写入如下内容：

**.django**

```
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=yufuquant.ccufmv!jn)82cu*pcry#3xcag**c#nn)=y0j%2k5dulf43_+omhu
DJANGO_ALLOWED_HOSTS=192.168.10.72
SENTRY_DSN=
REDIS_URL=redis://redis:6379/0
```

各配置项说明：

**DJANGO_SECRET_KEY**

系统密钥，切勿泄露。推荐使用这个工具在线生成：[Django Secret Key Creator](https://www.zmrenwu.com/webtools/django-secret-key-creator)。

**DJANGO_ALLOWED_HOSTS**

允许访问的域名。本地环境设为 127.0.0.1；未配置域名设置为服务器公网 ip；配置了域名则设置为域名。

**SENTRY_DSN**

[Sentry](https://sentry.io/) 服务的 DSN 地址，用于接收系统的错误日志，可以不配置。

完整示例：

```
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_SECRET_KEY=yufuquantzb^(0kgc3xf8zd#gwy$4v1o$1-%j1qnl!%&1scb$#
DJANGO_ALLOWED_HOSTS=demo.yufuquant.cc
SENTRY_DSN=https://b72df2cec6924h7962c61c4e463he09q@o199394.ingest.sentry.io/5144483
REDIS_URL=redis://redis:6379/0
```

**.postgres**

```
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=yufuquant
POSTGRES_USER=dbuser
POSTGRES_PASSWORD=dbpwd
```

各配置项说明：

**POSTGRES_DB**

数据库名，可自行更改。

**POSTGRES_USER**

数据库用户名，可自行更改。

**POSTGRES_PASSWORD**

数据库密码，请自行更改为安全的密码。

### 构建 Docker 容器

一切就绪，开始构建 Docker 容器，渔夫系统将运行于构建的容器内。

运行下面的命令构建容器：

```bash
docker-compose -f production.yml build
```

### 启动系统

Nginx 默认 80 和 443 端口：

```bash
docker-compose -f production.yml up -d
```

!!! 注意
    如果 80 和 443 端口已被占用，可在项目根目录创建一个 .env 文件，通过 PORT 和 SECURE_PORT 指定 HTTP 和 HTTPS 访问端口：

    ```
    PORT=4080
    SECURE_PORT=4443
    ```

### 初始化数据库

```bash
docker-compose -f production.yml run --rm django python manage.py runscript yufuquant.scripts.db.init_db
```

### 配置 HTTPS

!!! hint ""
    非公网环境或者未配置域名可跳过。

配置 HTTPS 的命令模板：
```bash
docker exec -it yufuquant_nginx_1 certbot --nginx -n --agree-tos --redirect --email xxx@xxx.com -d your_domain
```

将 --email 后的 xxx@xxx.com 替换为你的邮箱地址。

将 -d 后的 your_domain 替换为配置的域名。

## 常见问题解决

### 镜像拉取错误

如果遇到类似以下错误：

```
WARNING: pull access denied for yufuquant_local_django, repository does not exist or may require 'docker login'
```

请确保已运行构建命令：

```bash
docker-compose -f local.yml build  # 本地环境
```

或

```bash
docker-compose -f production.yml build  # 生产环境
```

### 端口冲突

如果端口已被占用，可以通过环境变量修改端口映射：

- 本地开发环境：
  ```
  PORT=8081 docker-compose -f local.yml up node
  ```

- 生产环境：
  ```
  PORT=4080 SECURE_PORT=4443 docker-compose -f production.yml up -d
  ```

### 数据库迁移问题

如果遇到数据库迁移错误，尝试重置数据库：

```bash
# 本地环境
docker-compose -f local.yml down
docker volume rm nuts_local_postgres_data
docker-compose -f local.yml up -d
```

或

```bash
# 生产环境
docker-compose -f production.yml down
docker volume rm nuts_production_postgres_data
docker-compose -f production.yml up -d
```

## 重启和停止

重启系统：

```bash
docker-compose -f production.yml restart
```

停止：

```bash
docker-compose -f production.yml stop
```

再次启动：

```bash
docker-compose -f production.yml up -d
```

## 更新

首先拉取最新版本的代码：

```bash
git pull
```

重新构建容器：

```bash
docker-compose -f production.yml build
```

启动：

```bash
docker-compose -f production.yml up -d
```