[TOC]

# 渔夫数字货币交易系统

专注于主流交易所、主流数字货币的量化交易，为量化交易者打造一个开源免费的基础平台。

## 系统架构

![](./screenshots/yufu系统架构.png)

## 技术栈

Python3、Django、Vue.js。

## 基于 Docker 快速部署

> 如果部署过程遇到问题，欢迎加入下方的用户体验群获取指导帮助。

**Step1**

克隆或者下载代码到本机或者服务器。

```bash
$ git clone https://github.com/zmrenwu/yufuquant.cc.git
# 输出如下
Cloning into 'yufuquant.cc'...
remote: Enumerating objects: 599, done.
remote: Counting objects: 100% (599/599), done.
remote: Compressing objects: 100% (384/384), done.
remote: Total 599 (delta 321), reused 480 (delta 202), pack-reused 0
Receiving objects: 100% (599/599), 2.19 MiB | 1.63 MiB/s, done.
Resolving deltas: 100% (321/321), done.
```

**Step2**

打开命令行，进入到项目根目录，安装必要的依赖（推荐使用 Python 虚拟环境）：

```bash
$ cd yufuquant.cc
$ pip install -r requirements.txt
```

**Step3**

生成并初始化数据：

```bash
# 初始化数据库
$ python manage.py migrate
$ python manage.py runscript yufu.scripts.init_db
```

**Step4**

进入 frontend/dist目录，复制 config.example.js 文件，重命名为 config.js，将 config.js 文件中的 127.0.0.1 改为本机或者服务器 ip。

**Step5**

进入到 compose/nginx/conf.d/ 目录，复制 yufu.conf.template 文件，重命名为 yufu.conf。

**Step6**

回到项目根目录，复制 yufu.example.env 文件，命名为 yufu.env，按注释修改各项内容：

```
# 系统密钥，设置一个随机字符串
DJANGO_SECRET_KEY=yufuquant.ccufmv!jn)82cu*pcry#3xcag**c#nn)=y0j%2k5dulf43_+omhu
# 修改为本机或者服务器的 ip 地址
DJANGO_ALLOWED_HOSTS=127.0.0.1
# sentry 服务 DSN 地址，可不填
SENTRY_DSN=
```

**Step7**

启动 Docker 容器。

```bash
$ docker-compose up --build -d
```

**Step8**

访问 http://ip:8080，其中 ip 为你本机或者服务器公网 ip，使用默认账户登录（用户名yufu，密码yufu123456）。

## 运行策略机器人

当前系统提供了一套网格策略机器人，可以在 Bybit 交易所的模拟盘或者实盘运行。后续版本我们会陆续添加主流交易所主流币的实盘策略，并开放 API 和发布 SDK 供第三方策略机器人的开发和接入。

**Step1**

点击导航条的 **接入**，绑定交易所凭据。

**Step2**

点击导航条的 **机器人**，创建一个新的机器人。

**Step3**

克隆或者直接下载机器人代码到本机或者服务器。

**Step4**

settings.py

**Step5**

创建网格

**Step6**

启动机器人

## 用户体验群

加入用户体验群获取指导和帮助以及和开发者一起决定未来的产品形态和功能。

## 后续开发计划

- [ ] 火币、币安、OKEx 现货、合约实盘策略
- [ ] ETH、EOS 等更多的主流币支持

## 联系开发者

Email：zmrenwu@gmail.com

微信：zmrenwu

## 附录

### Bybit 测试网使用方法

测试网入口：https://testnet.bybit.com/

先注册账户，然后在资产页面，点击充值，可领取测试用 BTC、ETH。最容易领取的是 ETH，然后可以使用 Bybit 的兑换功能将 ETH 兑换为 BTC。

创建 API，接入渔夫数字货币交易系统：

![](./screenshots/Bybit交易界面.png)