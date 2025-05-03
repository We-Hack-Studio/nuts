# Django 设置文件错误修复指南

## 问题

当运行 Django 服务时，出现以下错误：

```
ModuleNotFoundError: No module named 'config.settings.prod'
```

这表明 Django 应用正在尝试加载 `config.settings.prod` 模块，但找不到它。这可能是因为环境变量配置错误或者设置文件路径不正确。

## 解决方案

### 方法 1: 创建缺失的配置文件

1. 创建缺失的 `config/settings/prod.py` 文件：

```bash
mkdir -p config/settings
touch config/settings/prod.py
```

2. 在 `prod.py` 文件中添加基础配置：

```python
from config.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['*']  # 请根据实际情况调整
```

### 方法 2: 修改 Django 设置路径环境变量

在 `.envs/.local/.django` 文件中添加或修改 `DJANGO_SETTINGS_MODULE` 环境变量：

```
# Django 设置模块
DJANGO_SETTINGS_MODULE=config.settings.local
```

如果 `local` 配置文件不存在，请检查项目中现有的设置文件，它可能是:
- `config.settings.base`
- `config.settings.dev`
- `config.settings`

### 方法 3: 修改 start.sh 文件

检查并修改 `compose/local/django/start.sh` 脚本：

```bash
#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# 使用 local 而不是 prod 配置
export DJANGO_SETTINGS_MODULE=config.settings.local

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## 应用更改后的步骤

1. 修改相关配置后，停止并重建 Django 容器：

```bash
docker-compose -f local.yml stop django
docker-compose -f local.yml build django
docker-compose -f local.yml up django
```

2. 如果问题仍然存在，请尝试查看项目文档，了解正确的设置模块路径。 