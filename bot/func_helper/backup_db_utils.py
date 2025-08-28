import asyncio
import glob
import os
import shutil
from datetime import datetime

from bot import LOGGER


class BackupDBUtils:
    """数据库备份工具类 - 支持SQLite和MySQL"""

    @staticmethod
    async def backup_sqlite_db(db_path, backup_dir, max_backup_count):
        """SQLite数据库备份"""
        # 如果文件夹不存在，就创建它
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # 根据时间创建当前备份文件
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        db_name = os.path.splitext(os.path.basename(db_path))[0]
        backup_file = os.path.join(backup_dir, f'{db_name}-{timestamp}.db')
        
        try:
            # 复制SQLite数据库文件
            shutil.copy2(db_path, backup_file)
            LOGGER.info(f"SQLite数据库备份成功,文件保存为 {backup_file}")
            
            # 获取所有备份文件，并且通过时间进行排序
            all_backups = sorted(glob.glob(os.path.join(backup_dir, f'{db_name}-*.db')))
            
            # 如果超过了当前的备份最大数量，则删除最久的一个
            while len(all_backups) > max_backup_count:
                os.remove(all_backups[0])
                all_backups.pop(0)
                LOGGER.info(f"删除旧备份文件: {all_backups[0]}")
            
            return backup_file
            
        except Exception as e:
            LOGGER.error(f"SQLite数据库备份失败, error: {str(e)}")
            return None

    @staticmethod
    async def backup_mysql_db(host, port, user, password, database_name, backup_dir, max_backup_count):
        """MySQL数据库备份(直装/本机)"""
        # 如果文件夹不存在，就创建它
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # 根据时间创建当前备份文件
        backup_file = os.path.join(backup_dir, f'{database_name}-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.sql')
        command = f"mysqldump -h{host} -P{port} -u{user} -p\'{password}\' {database_name} > {backup_file}"
        
        process = await asyncio.create_subprocess_shell(command)
        try:
            await process.communicate()
        except Exception as e:
            LOGGER.error(f"MySQL数据库备份失败, error: {str(e)}")
            return None
            
        if process.returncode != 0:
            LOGGER.error(f"MySQL数据库备份失败, error code: {process.returncode}")
            return None
            
        LOGGER.info(f"MySQL数据库备份成功,文件保存为 {backup_file}")
        
        # 获取所有备份文件，并且通过时间进行排序
        all_backups = sorted(glob.glob(os.path.join(backup_dir, f'{database_name}-*.sql')))
        
        # 如果超过了当前的备份最大数量，则删除最久的一个
        while len(all_backups) > max_backup_count:
            os.remove(all_backups[0])
            all_backups.pop(0)
            LOGGER.info(f"删除旧备份文件: {all_backups[0]}")
            
        return backup_file
