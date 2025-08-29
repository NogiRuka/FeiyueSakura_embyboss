import os
import asyncio
from bot import bot, owner, LOGGER, db_type, db_path, db_backup_dir, db_backup_maxcount
from bot.storage.backup_db_utils import BackupDBUtils


class DbBackupUtils:
    """数据库备份工具类 - 支持SQLite和MySQL"""
    
    # 数据库相关配置
    db_type = db_type
    db_path = db_path
    backup_dir = db_backup_dir
    max_backup_count = db_backup_maxcount

    @classmethod
    async def backup_db(cls):
        """执行数据库备份"""
        backup_file = None
        
        if cls.db_type == "sqlite":
            # SQLite数据库备份
            backup_file = await BackupDBUtils.backup_sqlite_db(
                db_path=cls.db_path,
                backup_dir=cls.backup_dir,
                max_backup_count=cls.max_backup_count
            )
        else:
            # MySQL数据库备份（保留兼容性）
            from bot import db_host, db_name, db_user, db_pwd, db_port
            backup_file = await BackupDBUtils.backup_mysql_db(
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_pwd,
                database_name=db_name,
                backup_dir=cls.backup_dir,
                max_backup_count=cls.max_backup_count
            )
        
        return backup_file

    @staticmethod
    async def auto_backup_db():
        """自动数据库备份"""
        LOGGER.info("BOT数据库备份开始")
        backup_file = await DbBackupUtils.backup_db()
        
        if backup_file is not None:
            LOGGER.info(f'BOT数据库备份完毕: {backup_file}')
            try:
                # 发送备份文件给owner
                await asyncio.gather(
                    bot.send_document(
                        chat_id=owner,
                        document=backup_file,
                        caption=f'BOT数据库备份完毕',
                        disable_notification=True  # 勿打扰
                    ),
                    bot.send_document(
                        chat_id=owner,
                        document='config.json',
                        caption=f'config备份完毕',
                        disable_notification=True  # 勿打扰
                    )
                )
            except Exception as e:
                LOGGER.info(f'发送到owner失败，文件保存在本地: {e}')
        else:
            LOGGER.error(f'BOT数据库手动备份失败，请尽快检查相关配置')
