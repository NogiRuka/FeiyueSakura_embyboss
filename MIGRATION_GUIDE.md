# EmbyBot 项目改造指南

## 概述
本项目已从 Pyrogram 框架改造为 aiogram 框架，数据库从 MySQL 改为 SQLite，并添加了详细的中文注释。

## 主要改动

### 1. 框架替换
- **原框架**: Pyrogram (Telegram Bot API 的 Python 库)
- **新框架**: aiogram (更现代的 Telegram Bot API 异步库)

### 2. 数据库替换
- **原数据库**: MySQL (需要服务器配置)
- **新数据库**: SQLite (文件型数据库，无需额外配置)

### 3. 依赖更新
```bash
# 安装新依赖
pip install -r requirements.txt
```

### 4. 配置文件更新
- 移除了 MySQL 相关配置
- 添加了 SQLite 数据库路径配置
- 简化了数据库配置项

## 项目结构说明

### 核心文件
- `main.py` - 主程序入口
- `bot/__init__.py` - 机器人初始化配置
- `bot/sql_helper/__init__.py` - 数据库连接配置
- `bot/schemas/schemas.py` - 配置数据模型

### 模块结构
- `bot/modules/commands/` - 命令处理模块
- `bot/modules/panel/` - 面板管理模块
- `bot/modules/callback/` - 回调处理模块
- `bot/modules/extra/` - 额外功能模块

## 学习路径

### 第一步：了解配置系统
1. 查看 `config.json` 了解配置结构
2. 阅读 `bot/schemas/schemas.py` 了解配置验证
3. 理解 `bot/__init__.py` 中的配置加载过程

### 第二步：理解数据库系统
1. 查看 `bot/sql_helper/__init__.py` 了解数据库连接
2. 阅读 `bot/sql_helper/sql_request_record.py` 了解数据模型
3. 理解 SQLAlchemy ORM 的使用方式

### 第三步：学习命令处理
1. 查看 `bot/modules/commands/start.py` 了解命令处理流程
2. 理解 aiogram 的路由器系统
3. 学习如何注册和处理命令

### 第四步：了解消息处理
1. 查看 `bot/func_helper/msg_utils.py` 了解消息工具函数
2. 理解 aiogram 的消息类型和处理方式
3. 学习按钮和回调查询的处理

## 关键概念

### aiogram 路由器系统
```python
from aiogram import Router, F
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    # 处理 /start 命令
    pass
```

### SQLite 数据库
```python
# 数据库连接字符串
database_url = f"sqlite:///{db_path}"

# 创建引擎
engine = create_engine(
    database_url, 
    echo=False,
    connect_args={"check_same_thread": False}
)
```

### 配置管理
```python
# 加载配置
config = Config.load_config()

# 获取配置值
bot_token = config.bot_token
db_path = config.db_path
```

## 运行项目

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置机器人
1. 复制 `config_example.json` 为 `config.json`
2. 填入你的 bot token 和其他配置
3. 确保 `data/` 目录存在

### 3. 启动机器人
```bash
python main.py
```

## 常见问题

### Q: 为什么选择 aiogram 而不是 Pyrogram？
A: aiogram 是更现代的异步库，有更好的类型提示、更清晰的 API 设计，并且社区支持更好。

### Q: SQLite 相比 MySQL 有什么优势？
A: SQLite 是文件型数据库，无需额外服务器配置，部署更简单，适合中小型项目。

### Q: 如何添加新的命令？
A: 在 `bot/modules/commands/` 目录下创建新的 Python 文件，定义路由器，然后在 `__init__.py` 中注册。

## 下一步学习建议

1. **深入学习 aiogram**: 阅读官方文档，了解更多高级特性
2. **数据库设计**: 学习 SQLAlchemy 的更多用法，设计更复杂的数据模型
3. **异步编程**: 深入理解 Python 的 async/await 语法
4. **项目扩展**: 尝试添加新的功能模块，如用户管理、权限控制等

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 许可证

本项目遵循原项目的许可证条款。
