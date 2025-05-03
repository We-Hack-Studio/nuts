# Poetry 安装错误修复指南

您在构建 Docker 镜像时遇到了 Poetry 安装错误，这是因为 Dockerfile 中使用的 Poetry 安装脚本链接已经过时。下面是修复步骤：

## 问题

错误信息：
```
ERROR [celeryworker 4/19] RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | POETRY_PREVIEW=1 python
```

这个错误是因为 Poetry 团队已经更改了安装脚本的位置和方法。

## 解决方案

您需要修改 `compose/local/django/Dockerfile` 文件，将 Poetry 安装命令更新为最新的方法。

### 方法 1: 使用官方推荐的安装脚本

1. 打开 `compose/local/django/Dockerfile` 文件
2. 找到以下行（大约在第 9 行左右）：
   ```dockerfile
   RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | POETRY_PREVIEW=1 python
   ```
3. 替换为新的安装命令：
   ```dockerfile
   RUN curl -sSL https://install.python-poetry.org | python3 -
   ```
4. 保存文件

### 方法 2: 使用 pip 安装（更简单）

或者，您可以使用更简单的 pip 安装方法：

1. 打开 `compose/local/django/Dockerfile` 文件
2. 找到以下行（大约在第 9 行左右）：
   ```dockerfile
   RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | POETRY_PREVIEW=1 python
   ```
3. 替换为 pip 安装命令：
   ```dockerfile
   RUN pip install poetry
   ```
4. 同时删除或注释掉下一行的 PATH 设置（因为 pip 安装会自动添加到 PATH）：
   ```dockerfile
   # 原来的行
   ENV PATH "/root/.poetry/bin:${PATH}"
   
   # 修改为（添加注释或直接删除）
   # ENV PATH "/root/.poetry/bin:${PATH}"
   ```
5. 保存文件

## 应用变更

修改完 Dockerfile 后，再次尝试构建镜像：

```bash
docker-compose -f local.yml build
```

这应该能解决 Poetry 安装错误，并允许构建继续进行。

## 注意

如果还有其他 Dockerfile（例如用于 celeryworker、celerybeat 的单独文件），您可能也需要在这些文件中进行相同的更改。 