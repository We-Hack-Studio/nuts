# 1. Title: PRD for YuFuQuant 量化交易平台

<version>1.0.0</version>

## Status: Approved

## Intro

本文档定义了 YuFuQuant 量化交易平台的产品需求。该平台旨在为个人交易者和懂开发的量化交易者提供一套工具，用于连接交易所、开发、测试和执行自动化交易策略。

## Goals

- 提供稳定可靠的交易所连接。
- 支持用户创建、回测和部署自定义交易策略。
- 提供清晰的用户界面来管理机器人、策略和账户。
- 确保系统的安全性和数据准确性。
- (待补充：更具体的目标、衡量标准、KPI)

## Features and Requirements

### 主要功能 / High-Level Features

- **用户与认证 (Users & Authentication):** 用户注册、登录、权限管理。
- **凭证管理 (Credentials Management):** 安全存储和管理交易所 API Key。
- **交易所对接 (Exchange Integration):** 连接和管理多个加密货币或金融交易所。
- **策略开发与管理 (Strategy Development & Management):**
    - 提供策略编写环境或接口。
    - 策略回测功能。
    - 策略部署与版本管理。
- **机器人管理 (Robot Management):**
    - 创建、配置和启动交易机器人。
    - 监控机器人运行状态和日志。
    - 停止和管理机器人实例。
- **数据流处理 (Stream Processing):** 实时市场数据接入和处理。
- **任务调度 (Task Scheduling):** 使用 Celery 处理后台任务（如定时任务、数据同步等）。
- **通知系统 (Notifications):** (可能存在) 交易执行、错误等事件通知。
- **仪表盘与监控 (Dashboard & Monitoring):** (可能存在) 展示账户概览、机器人表现等。

### 非功能性需求 (初步)

- **性能:** 系统需能处理实时高频数据流和交易执行。
- **可靠性:** 保证交易执行的稳定性和数据一致性。
- **安全性:** 保护用户凭证和交易数据安全。
- **可扩展性:** 架构应能支持未来更多的用户、策略和交易所。
- **可维护性:** 代码和架构应清晰、易于维护和迭代。

## Epic List

(待定义，基于后续的功能细化)

## Epic 1: Story List

(待定义，需要根据优先级和功能分解生成详细用户故事)

## Technology Stack

| Technology  | Description                        |
| :---------- | :--------------------------------- |
| Backend     | Django (Python)                    |
| Frontend    | Vue.js 2.x                         |
| Database    | PostgreSQL                         |
| Cache       | Redis                              |
| Async Tasks | Celery                             |
| Web Server  | (待确认，例如 Nginx, Gunicorn)     |
| Deployment  | Docker (基于 compose 文件推测) |

## Reference

(待补充：架构图、流程图等)

## Data Models, API Specs, Schemas, etc...

根据后端代码 (`yufuquant/`) 初步提取的关键数据模型：

*   **`User` (`users.models.User`)**:
    *   继承自 Django `AbstractUser`
    *   字段: `username`, `password`, `email`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `nickname`, `avatar` (ImageField), `avatar_thumbnail` (ImageSpecField)
*   **`Exchange` (`exchanges.models.Exchange`)**:
    *   字段: `code`, `name`, `name_zh`, `logo` (ImageField), `logo_thumbnail` (ImageSpecField), `active`, `rank`
*   **`Credential` (`credentials.models.Credential`)**:
    *   字段: `note`, `api_key` (Encrypted), `secret` (Encrypted), `passphrase` (Encrypted), `test_net`, `exchange` (ForeignKey to `Exchange`), `user` (ForeignKey to `User`)
*   **`Strategy` (`strategies.models.Strategy`)**:
    *   字段: `name`, `brief`, `description`, `specification` (JSONField - 包含策略参数定义等)
*   **`Robot` (`robots.models.Robot`)**:
    *   字段: `name`, `pair`, `market_type` (Choices), `enabled`, `start_time`, `ping_time`, `credential` (ForeignKey to `Credential`), `strategy` (ForeignKey to `Strategy`), `strategy_parameters` (JSONField), `target_currency`, `base_currency`, `quote_currency`, `strategy_store` (JSONField), `position_store` (JSONField), `order_store` (JSONField)
*   **`AssetRecord` (`robots.models.AssetRecord`)**:
    *   字段: `currency`, `total_principal`, `total_balance`, `total_principal_24h_ago`, `total_balance_24h_ago`, `robot` (OneToOneField to `Robot`)
*   **`AssetRecordSnap` (`robots.models.AssetRecordSnap`)**:
    *   字段: `total_principal`, `total_balance`, `period` (Choices: 1h, 1d), `asset_record` (ForeignKey to `AssetRecord`)

(注：这只是初步提取，详细字段类型、约束和关系需进一步分析或参考架构文档。)

## Project Structure

初步分析的项目结构：

```text
.
├── compose/          # Docker Compose 配置 (dev, local, production)
├── config/           # Django 项目配置 (settings, urls)
├── database/         # 数据库相关 (可能是备份或初始化脚本)
├── docs/             # 项目文档
├── frontend/         # 前端 Vue.js 应用
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vue.config.js
├── locale/           # 国际化/本地化文件
├── yufuquant/        # 后端 Django 应用
│   ├── core/         # 核心共享模块 (如 TimeStampedModel)
│   ├── credentials/  # 凭证管理 App
│   ├── exchanges/    # 交易所信息 App
│   ├── robots/       # 机器人核心逻辑 App
│   ├── strategies/   # 策略管理 App
│   ├── streams/      # 数据流处理 App (?)
│   ├── taskapp/      # Celery 任务 App
│   ├── templates/    # Django 模板
│   ├── users/        # 用户管理 App
│   ├── __init__.py
│   └── conftest.py   # Pytest 配置
├── .ai/              # AI 生成的文档
│   └── prd.md
├── manage.py         # Django 管理脚本
├── pyproject.toml    # Python 项目配置 (Poetry)
├── requirements.txt  # (可能存在或由 Poetry 管理)
├── Dockerfile        # (可能在 compose/ 或根目录)
└── ... (其他配置文件 .gitignore, .dockerignore, etc.)
```

(注：此结构基于目录列表推断，可能不完全准确或详细。)

## Change Log

| Change        | Story ID | Description      |
| :------------ | :------- | :--------------- |
| Initial draft | N/A      | Initial PRD draft | 