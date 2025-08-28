# 🚀 EmbyBot 部署指南

## 概述
本项目已从Docker部署方式改造为直接Python运行方式，使用SQLite数据库，部署更加简单。

## 系统要求

### 操作系统
- **Windows**: Windows 10/11
- **Linux**: Ubuntu 18.04+, CentOS 7+, Debian 9+
- **macOS**: macOS 10.14+

### Python环境
- **Python版本**: 3.8 或更高版本
- **推荐版本**: Python 3.10+

## 安装步骤

### 1. 克隆项目
```bash
git clone https://github.com/your-username/FeiyueSakura_embyboss.git
cd FeiyueSakura_embyboss
```

### 2. 安装Python依赖
```bash
# 使用pip安装
pip install -r requirements.txt

# 或者使用pip3（某些系统）
pip3 install -r requirements.txt

# 推荐使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. 配置机器人
1. 复制配置文件模板：
   ```bash
   cp config_example.json config.json
   ```

2. 编辑 `config.json`，填入你的配置：
   ```json
   {
     "bot_name": "你的机器人名称",
     "bot_token": "你的机器人Token",
     "owner_api": 12345,
     "owner_hash": "你的API Hash",
     "owner": 123456789,
     "group": [-1001234567890],
     "main_group": "你的主群组",
     "chanel": "你的频道",
     "db_type": "sqlite",
     "db_path": "./data/embybot.db"
   }
   ```

### 4. 创建必要目录
```bash
mkdir -p data
mkdir -p log
mkdir -p db_backup
```

### 5. 启动机器人
```bash
python main.py
```

## 配置说明

### 数据库配置
- **db_type**: 数据库类型，设置为 "sqlite"
- **db_path**: SQLite数据库文件路径，默认为 "./data/embybot.db"

### 机器人配置
- **bot_token**: 从 @BotFather 获取的机器人Token
- **owner**: 机器人所有者的Telegram用户ID
- **group**: 允许使用机器人的群组ID列表

### Emby配置
- **emby_api**: Emby服务器的API密钥
- **emby_url**: Emby服务器地址
- **emby_line**: Emby服务器域名

## 常见问题

### Q: 如何获取机器人Token？
A: 在Telegram中联系 @BotFather，发送 `/newbot` 命令创建新机器人。

### Q: 如何获取用户ID？
A: 在Telegram中联系 @userinfobot，它会返回你的用户ID。

### Q: 数据库文件在哪里？
A: 数据库文件默认保存在 `./data/embybot.db`，首次运行时会自动创建。

### Q: 如何备份数据库？
A: 数据库会自动备份到 `./db_backup/` 目录，也可以手动复制 `./data/embybot.db` 文件。

## 服务管理

### 使用systemd（Linux）
1. 创建服务文件：
   ```bash
   sudo nano /etc/systemd/system/embybot.service
   ```

2. 添加以下内容：
   ```ini
   [Unit]
   Description=EmbyBot Telegram Bot
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/path/to/FeiyueSakura_embyboss
   ExecStart=/usr/bin/python3 main.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. 启用并启动服务：
   ```bash
   sudo systemctl enable embybot
   sudo systemctl start embybot
   sudo systemctl status embybot
   ```

### 使用PM2（Node.js进程管理器）
1. 安装PM2：
   ```bash
   npm install -g pm2
   ```

2. 启动机器人：
   ```bash
   pm2 start main.py --name embybot --interpreter python3
   pm2 save
   pm2 startup
   ```

## 更新项目
```bash
git pull origin master
pip install -r requirements.txt
# 重启机器人
```

## 故障排除

### 权限问题
确保Python有读写项目目录的权限：
```bash
chmod -R 755 /path/to/FeiyueSakura_embyboss
```

### 端口问题
确保没有其他程序占用相关端口，特别是Emby服务器的端口。

### 数据库问题
如果数据库损坏，可以删除 `./data/embybot.db` 文件，机器人会重新创建数据库。

## 技术支持
如果遇到问题，请：
1. 查看日志文件
2. 检查配置文件
3. 在GitHub上提交Issue
4. 联系项目维护者
