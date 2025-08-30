import pytz

from bot import bot, _open, save_config, owner, admins, bot_name, ranks, schedall, group
from bot.sql_helper.sql_code import sql_add_code
from bot.sql_helper.sql_emby import sql_get_emby
from cacheout import Cache

cache = Cache()


def judge_admins(uid):
    """
    判断是否admin
    :param uid: tg_id
    :return: bool
    """
    if uid != owner and uid not in admins and uid not in group:
        return False
    else:
        return True


async def user_in_group_filter(message_or_callback) -> bool:
    """
    检查用户是否在指定群组中
    :param bot: aiogram 的 Bot 实例
    :param user_id: 用户 ID
    :param chat_id: 群聊 ID
    :return: bool
    """
    try:
        user_id = message_or_callback.from_user.id
        member = await bot.get_chat_member('@lustfulboy', user_id)
        # 如果能拿到状态就说明在群里
        return member.status in {"member", "administrator", "creator"}
    except Exception as e:
        # 如果报错，大多数情况是用户不在群里或者群不存在
        from bot import LOGGER
        LOGGER.warning(f"⚠️ 检查群组成员失败: {e}")
        return False


async def user_in_group_filte(message_or_callback):
    """
    检查用户是否在授权群组中
    :param message_or_callback: Message 或 CallbackQuery 对象
    :return: bool
    """
    try:
        # 获取用户ID
        if hasattr(message_or_callback, 'from_user'):
            user_id = message_or_callback.from_user.id
            user_username = getattr(message_or_callback.from_user, 'username', 'Unknown')
        else:
            user_id = message_or_callback.from_user.id
            user_username = getattr(message_or_callback.from_user, 'username', 'Unknown')
        
        # 获取聊天信息
        chat_id = None
        chat_type = None
        if hasattr(message_or_callback, 'message') and message_or_callback.message:
            chat_id = message_or_callback.message.chat.id
            chat_type = message_or_callback.message.chat.type
        
        # 详细日志
        from bot import LOGGER
        LOGGER.info(f"🔍 用户群组检查 - 用户ID: {user_id}, 用户名: @{user_username}")
        LOGGER.info(f"🔍 聊天信息 - 聊天ID: {chat_id}, 聊天类型: {chat_type}")
        LOGGER.info(f"🔍 授权群组列表: {group}")
        LOGGER.info(f"🔍 授权群组类型: {type(group)}")
        LOGGER.info(f"🔍 用户ID类型: {type(user_id)}")
        LOGGER.info(f"🔍 用户是否在授权群组中: {user_id in group}")
        
        # 检查用户是否在授权群组中
        result = user_id in group
        LOGGER.info(f"🔍 检查结果: {result}")
        
        # 额外调试信息
        if not result:
            LOGGER.warning(f"⚠️ 用户 {user_id} 不在授权群组中")
            LOGGER.warning(f"⚠️ 授权群组内容: {group}")
            LOGGER.warning(f"⚠️ 用户ID: {user_id}")
        
        return result
    except Exception as e:
        from bot import LOGGER
        LOGGER.error(f"❌ 用户群组检查出错: {e}")
        return False


async def members_info(tg=None, name=None):
    if tg is None:
        tg = name
    data = sql_get_emby(tg)
    if data is None:
        return None
    else:
        name = data.name or '无账户信息'
        pwd2 = data.pwd2
        embyid = data.embyid
        us = [data.us, data.iv]
        lv_dict = {'a': '白名单', 'b': '**正常**', 'c': '**已禁用**', 'd': '未注册'}
        lv = lv_dict.get(data.lv, '未知')
        if lv == '白名单':
            ex = '+ ∞'
        elif data.name is not None and schedall.low_activity and not schedall.check_ex:
            ex = '__若21天无观看将封禁__'
        elif data.name is not None and not schedall.low_activity and not schedall.check_ex:
            ex = ' __无需保号，放心食用__'
        else:
            ex = data.ex or '无账户信息'
        return name, lv, ex, us, embyid, pwd2


async def open_check():
    open_stats = _open.stat
    all_user = _open.all_user
    tem = _open.tem
    timing = _open.timing
    return open_stats, all_user, tem, timing


async def tem_alluser():
    _open.tem = _open.tem + 1
    if _open.tem >= _open.all_user:
        _open.stat = False
    save_config()


from random import choice
import string


async def pwd_create(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])


async def cr_link_one(tg: int, times, count, days: int, method: str):
    links = ''
    code_list = []
    i = 1
    if method == 'code':
        while i <= count:
            p = await pwd_create(10)
            uid = f'{ranks.logo}-{times}-Register_{p}'
            code_list.append(uid)
            link = f'`{uid}`\n'
            links += link
            i += 1
    elif method == 'link':
        while i <= count:
            p = await pwd_create(10)
            uid = f'{ranks.logo}-{times}-Register_{p}'
            code_list.append(uid)
            link = f't.me/{bot_name}?start={uid}\n'
            links += link
            i += 1
    if sql_add_code(code_list, tg, days) is False:
        return None
    return links


async def rn_link_one(tg: int, times, count, days: int, method: str):
    links = ''
    code_list = []
    i = 1
    if method == 'code':
        while i <= count:
            p = await pwd_create(10)
            uid = f'{ranks.logo}-{times}-Renew_{p}'
            code_list.append(uid)
            link = f'`{uid}`\n'
            links += link
            i += 1
    elif method == 'link':
        while i <= count:
            p = await pwd_create(10)
            uid = f'{ranks.logo}-{times}-Renew_{p}'
            code_list.append(uid)
            link = f't.me/{bot_name}?start={uid}\n'
            links += link
            i += 1
    if sql_add_code(code_list, tg, days) is False:
        return None
    return links


async def cr_link_two(tg: int, for_tg, days: int):
    code_list = []
    invite_code = await pwd_create(11)
    uid = f'{for_tg}-{invite_code}'
    code_list.append(uid)
    link = f't.me/{bot_name}?start={uid}'
    if sql_add_code(code_list, tg, days) is False:
        return None
    return link


from datetime import datetime, timedelta


async def convert_s(seconds: int):
    duration = timedelta(seconds=seconds)
    days = duration.days
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    days = '' if days == 0 else f'{days} 天'
    hours = '' if hours == 0 else f'{hours} 小时'
    return f"{days} {hours} {minutes} 分钟"


def convert_runtime(RunTimeTicks: int):
    seconds = RunTimeTicks // 10000000
    duration = timedelta(seconds=seconds)
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    hours = '' if hours == 0 else f'{hours} 小时'
    return f"{hours} {minutes} 分钟"


def convert_to_beijing_time(original_date):
    original_date = original_date.split(".")[0].replace('T', ' ')
    dt = datetime.strptime(original_date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)
    beijing_tz = pytz.timezone("Asia/Shanghai")
    dt = beijing_tz.localize(dt)
    return dt


@cache.memoize(ttl=300)
async def get_users():
    members_dict = {}
    async for member in bot.get_chat_members(group[0]):
        try:
            members_dict[member.user.id] = member.user.first_name
        except Exception as e:
            print(f'{e} 某名bug {member}')
    return members_dict


__all__ = [
    'judge_admins', 'user_in_group_filter', 'members_info', 'open_check', 'tem_alluser', 'pwd_create',
    'cr_link_one', 'rn_link_one', 'cr_link_two', 'convert_s', 'convert_runtime', 'convert_to_beijing_time',
    'get_users', 'cache'
]


