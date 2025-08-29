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
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        db_name = os.path.splitext(os.path.basename(db_path))[0]
        backup_file = os.path.join(backup_dir, f'{db_name}-{timestamp}.db')

        try:
            shutil.copy2(db_path, backup_file)
            LOGGER.info(f"SQLite数据库备份成功,文件保存为 {backup_file}")

            all_backups = sorted(glob.glob(os.path.join(backup_dir, f'{db_name}-*.db')))

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
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        backup_file = os.path.join(backup_dir, f'{database_name}-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.sql')
        command = f"mysqldump -h{host} -P{port} -u{user} -p'{password}' {database_name} > {backup_file}"

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

        all_backups = sorted(glob.glob(os.path.join(backup_dir, f'{database_name}-*.sql')))

        while len(all_backups) > max_backup_count:
            os.remove(all_backups[0])
            all_backups.pop(0)
            LOGGER.info(f"删除旧备份文件: {all_backups[0]}")

        return backup_file



