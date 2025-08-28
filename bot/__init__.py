#! /usr/bin/python3
# -*- coding: utf-8 -*-
import contextlib

from .func_helper.logger_config import logu, Now

LOGGER = logu(__name__)

from .schemas import Config

config = Config.load_config()


def save_config():
    config.save_config()


'''从config对象中获取属性值'''
# bot
bot_name = config.bot_name
bot_token = config.bot_token
owner_api = config.owner_api
owner_hash = config.owner_hash
owner = config.owner
group = config.group
main_group = config.main_group
chanel = config.chanel
bot_photo = config.bot_photo
_open = config.open
admins = config.admins
sakura_b = config.money
ranks = config.ranks
prefixes = ['/', '!', '.', '，', '。']
schedall = config.schedall
# emby设置
emby_api = config.emby_api
emby_url = config.emby_url
emby_line = config.emby_line
emby_block = config.emby_block
extra_emby_libs = config.extra_emby_libs
# 数据库配置 - 改为SQLite
db_type = config.db_type
db_path = config.db_path
# 探针
tz_ad = config.tz_ad
tz_api = config.tz_api
tz_id = config.tz_id

w_anti_channel_ids = config.w_anti_channel_ids
kk_gift_days = config.kk_gift_days
moviepilot_open = config.moviepilot_open
moviepilot_username = config.moviepilot_username
moviepilot_password = config.moviepilot_password
moviepilot_url = config.moviepilot_url
moviepilot_access_token = config.moviepilot_access_token
download_cost = config.download_cost
download_log_chatid = config.download_log_chatid
fuxx_pitao = config.fuxx_pitao
save_config()

LOGGER.info("配置文件加载完毕")

# 从aiogram导入BotCommand
from aiogram.types import BotCommand

'''定义不同等级的人使用不同命令'''
user_p = [
    BotCommand(command="start", description="[私聊] 开启用户面板"),
    BotCommand(command="myinfo", description="[用户] 查看状态"),
    BotCommand(command="count", description="[用户] 媒体库数量"),
    BotCommand(command="red", description="[用户/禁言] 发红包"),
    BotCommand(command="srank", description="[用户/禁言] 查看计分")]

# 取消 BotCommand("exchange", "[私聊] 使用注册码")
admin_p = user_p + [
    BotCommand(command="kk", description="管理用户 [管理]"),
    BotCommand(command="score", description="加/减积分 [管理]"),
    BotCommand(command="coins", description=f"加/减{sakura_b} [管理]"),
    BotCommand(command="deleted", description="清理死号 [管理]"),
    BotCommand(command="kick_not_emby", description=f"踢出当前群内无号崽 [管理]"),
    BotCommand(command="renew", description="调整到期时间 [管理]"),
    BotCommand(command="rmemby", description="删除用户[包括非tg] [管理]"),
    BotCommand(command="prouser", description="增加白名单 [管理]"),
    BotCommand(command="revuser", description="减少白名单 [管理]"),
    BotCommand(command="rev_white_channel", description="移除皮套人白名单 [管理]"),
    BotCommand(command="white_channel", description="添加皮套人白名单 [管理]"),
    BotCommand(command="unban_channel", description="解封皮套人 [管理]"),
    BotCommand(command="syncgroupm", description="消灭不在群的人 [管理]"),
    BotCommand(command="syncunbound", description="消灭未绑定bot的emby账户 [管理]"),
    BotCommand(command="low_activity", description="手动运行活跃检测 [管理]"),
    BotCommand(command="check_ex", description="手动到期检测 [管理]"),
    BotCommand(command="uranks", description="召唤观影时长榜，失效时用 [管理]"),
    BotCommand(command="days_ranks", description="召唤播放次数日榜，失效时用 [管理]"),
    BotCommand(command="week_ranks", description="召唤播放次数周榜，失效时用 [管理]"),
    BotCommand(command="embyadmin", description="开启emby控制台权限 [管理]"),
    BotCommand(command="ucr", description="私聊创建非tg的emby用户 [管理]"),
    BotCommand(command="uinfo", description="查询指定用户名 [管理]"),
    BotCommand(command="urm", description="删除指定用户名 [管理]"),
    BotCommand(command="restart", description="重启bot [owner]"),
]

owner_p = admin_p + [
    BotCommand(command="proadmin", description="添加bot管理 [owner]"),
    BotCommand(command="revadmin", description="移除bot管理 [owner]"),
    BotCommand(command="renewall", description="一键派送天数给所有未封禁的用户 [owner]"),
    BotCommand(command="coinsall", description="一键派送币币给所有未封禁的用户 [owner]"),
    BotCommand(command="callall", description="群发消息给每个人 [owner]"),
    BotCommand(command="bindall_id", description="一键更新用户们Embyid [owner]"),
    BotCommand(command="backup_db", description="手动备份数据库[owner]"),
    BotCommand(command='restore_from_db', description='恢复Emby账户[owner]'),
    BotCommand(command="config", description="开启bot高级控制面板 [owner]"),
    BotCommand(command="embylibs_unblockall", description="一键开启所有用户的媒体库 [owner]"),
    BotCommand(command="embylibs_blockall", description="一键关闭所有用户的媒体库 [owner]")
]
if len(extra_emby_libs) > 0:
    owner_p += [BotCommand(command="extraembylibs_blockall", description="一键关闭所有用户的额外媒体库 [owner]"),
                BotCommand(command="extraembylibs_unblockall", description="一键开启所有用户的额外媒体库 [owner]")]

with contextlib.suppress(ImportError):
    import uvloop
    uvloop.install()

# 从aiogram导入Bot和Dispatcher
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# 代理配置
proxy = {} if not config.proxy.scheme else config.proxy.dict()

# 创建aiogram Bot实例 - 使用新的语法
bot = Bot(
    token=bot_token, 
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)

# 创建Dispatcher实例
dp = Dispatcher()

LOGGER.info("aiogram Bot 客户端准备完毕")
