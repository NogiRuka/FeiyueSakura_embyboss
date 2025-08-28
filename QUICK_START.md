# 🚀 EmbyBot 快速启动指南

## ⚡ 5分钟快速启动

### 第一步：安装依赖
**Windows用户：**
```bash
# 双击运行
install_dependencies.bat
```

**Linux/macOS用户：**
```bash
# 运行安装脚本
bash install_dependencies.sh
```

### 第二步：配置机器人
1. 复制配置文件：
   ```bash
   cp config_example.json config.json
   ```

2. 编辑 `config.json`，填入你的配置：
   ```json
   {
     "bot_token": "你的机器人Token",
     "owner": 你的用户ID,
     "db_type": "sqlite",
     "db_path": "./data/embybot.db"
   }
   ```

### 第三步：启动机器人
```bash
python main.py
```

## 🔧 常见问题解决

### 问题1：ModuleNotFoundError: No module named 'cacheout'
**解决方案：**
```bash
pip install cacheout
```

### 问题2：ModuleNotFoundError: No module named 'loguru'
**解决方案：**
```bash
pip install loguru
```

### 问题3：ModuleNotFoundError: No module named 'pydantic'
**解决方案：**
```bash
pip install pydantic
```

### 问题4：ModuleNotFoundError: No module named 'aiogram'
**解决方案：**
```bash
pip install aiogram
```

### 问题5：ModuleNotFoundError: No module named 'pykeyboard'
**解决方案：**
```bash
# 已修复，使用aiogram内置按钮功能
# 无需安装pykeyboard
```

## 📱 获取机器人Token

1. 在Telegram中联系 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot` 命令
3. 按提示设置机器人名称
4. 获取Token（类似：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）

## 🆔 获取用户ID

1. 在Telegram中联系 [@userinfobot](https://t.me/userinfobot)
2. 发送任意消息
3. 机器人会返回你的用户ID

## 📁 项目结构

```
FeiyueSakura_embyboss/
├── main.py                 # 主程序入口
├── config.json            # 配置文件
├── requirements.txt        # 依赖列表
├── install_dependencies.bat  # Windows安装脚本
├── install_dependencies.sh   # Linux/macOS安装脚本
├── bot/                    # 机器人核心代码
├── data/                   # 数据库文件
└── log/                    # 日志文件
```

## 🎯 下一步

启动成功后，你可以：
1. 在Telegram中搜索你的机器人
2. 发送 `/start` 命令
3. 按照 `MIGRATION_GUIDE.md` 学习项目架构
4. 参考 `DEPLOYMENT.md` 了解详细部署

## 🆘 需要帮助？

- 查看 `MIGRATION_GUIDE.md` 了解项目改造详情
- 查看 `DEPLOYMENT.md` 了解详细部署步骤
- 在GitHub上提交Issue
- 联系项目维护者
