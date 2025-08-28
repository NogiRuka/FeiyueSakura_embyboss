"""
aiogram按钮工具模块
替代原来的pykeyboard和pyrogram按钮实现
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Tuple, Union
from bot import chanel, main_group, bot_name, extra_emby_libs, tz_id, tz_ad, tz_api, _open, sakura_b, schedall, config
from bot.func_helper import nezha_res
from bot.func_helper.emby import emby
from bot.func_helper.utils import judge_admins, members_info


def create_inline_keyboard(buttons: List[List[Tuple[str, str, str]]]) -> InlineKeyboardMarkup:
    """
    创建内联键盘
    :param buttons: 按钮列表，格式为 [[(text, callback_data, type), ...], ...]
    :return: InlineKeyboardMarkup对象
    """
    keyboard = []
    for row in buttons:
        keyboard_row = []
        for button in row:
            text, callback_data, button_type = button
            if button_type == 'url':
                keyboard_row.append(InlineKeyboardButton(text=text, url=callback_data))
            else:
                keyboard_row.append(InlineKeyboardButton(text=text, callback_data=callback_data))
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def array_chunk(data: List, chunk_size: int) -> List[List]:
    """
    将列表分块
    :param data: 原始列表
    :param chunk_size: 每块大小
    :return: 分块后的列表
    """
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def ikb(buttons: List[List[Union[str, Tuple[str, str]]]]) -> InlineKeyboardMarkup:
    """
    快速创建内联键盘
    :param buttons: 按钮列表，支持多种格式
    :return: InlineKeyboardMarkup对象
    """
    keyboard = []
    for row in buttons:
        keyboard_row = []
        for button in row:
            if isinstance(button, tuple):
                if len(button) == 2:
                    text, callback_data = button
                    keyboard_row.append(InlineKeyboardButton(text=text, callback_data=callback_data))
                elif len(button) == 3:
                    text, callback_data, button_type = button
                    if button_type == 'url':
                        keyboard_row.append(InlineKeyboardButton(text=text, url=callback_data))
                    else:
                        keyboard_row.append(InlineKeyboardButton(text=text, callback_data=callback_data))
            else:
                # 如果只有一个字符串，作为回调数据
                keyboard_row.append(InlineKeyboardButton(text=button, callback_data=button))
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


"""start面板 ↓"""


def judge_start_ikb(uid: int) -> InlineKeyboardMarkup:
    """
    start面板按钮
    :param uid: 用户ID
    :return: 内联键盘
    """
    d = [('️👥 用户功能', 'members'), ('🌐 服务器', 'server'), ('🎟️ 使用注册/续期码', 'exchange')]
    if _open.checkin:
        d.append((f'🎯 签到', 'checkin'))
    lines = array_chunk(d, 2)
    if judge_admins(uid):
        lines.append([('👮🏻‍♂️ admin', 'manage')])
    return ikb(lines)


# un_group_answer
group_f = ikb([[('点击我(●ˇ∀ˇ●)', f't.me/{bot_name}', 'url')]])

# un in group
judge_group_ikb = ikb([[('🌟 频道入口 ', f't.me/{chanel}', 'url'),
                        ('💫 群组入口', f't.me/{main_group}', 'url')],
                       [('❌ 关闭消息', 'closeit')]])

"""members ↓"""


def members_ikb(emby=False) -> InlineKeyboardMarkup:
    """
    判断用户面板
    :param emby: 是否有Emby账户
    :return: 内联键盘
    """
    if emby:
        return ikb([[('🏪 兑换商店', 'storeall'), ('🗑️ 删除账号', 'delme')],
                    [('🎬 显示/隐藏', 'embyblock'), ('⭕ 重置密码', 'reset')],
                    [('🔍 求片中心', 'download_center'), ('♻️ 主界面', 'back_start')]])
    else:
        return ikb(
            [[('👑 创建账户', 'create')], [('⭕ 换绑TG', 'changetg'), ('🔍 绑定TG', 'bindtg')],
             [('♻️ 主界面', 'back_start')]])


back_start_ikb = ikb([[('💫 回到首页', 'back_start')]])
back_members_ikb = ikb([[('💨 返回', 'members')]])
re_create_ikb = ikb([[('🍥 重新输入', 'create'), ('💫 用户主页', 'members')]])
re_changetg_ikb = ikb([[('✨ 换绑TG', 'changetg'), ('💫 用户主页', 'members')]])
re_bindtg_ikb = ikb([[('✨ 绑定TG', 'bindtg'), ('💫 用户主页', 'members')]])
re_delme_ikb = ikb([[('♻️ 重试', 'delme')], [('🔙 返回', 'members')]])
re_reset_ikb = ikb([[('♻️ 重试', 'reset')], [('🔙 返回', 'members')]])
re_exchange_b_ikb = ikb([[('♻️ 重试', 'exchange'), ('❌ 关闭', 'closeit')]])
re_download_center_ikb = ikb([[('🔍 求片', 'download_media'), ('📈 查看下载进度', 'rate')], [('🔙 返回', 'members')]])


def page_request_record_ikb(has_prev: bool, has_next: bool):
    """分页按钮"""
    buttons = []
    if has_prev:
        buttons.append(('◀️ 上一页', 'pre_page_request_record'))
    if has_next:
        buttons.append(('▶️ 下一页', 'next_page_request_record'))
    return ikb([buttons, [('🔙 返回', 'download_center')]])


re_born_ikb = ikb([[('✨ 重输', 'store-reborn'), ('💫 返回', 'storeall')]])


def store_ikb():
    """商店按钮"""
    return ikb([[(f'♾️ 兑换白名单', 'store-whitelist'), (f'🔥 兑换解封禁', 'store-reborn')],
                [(f'🎟️ 兑换注册码', 'store-invite'), (f'🔍 查询注册码', 'store-query')],
                [(f'❌ 取消', 'members')]])


re_store_renew = ikb([[('✨ 重新输入', 'changetg'), ('💫 取消输入', 'storeall')]])


def del_me_ikb(embyid) -> InlineKeyboardMarkup:
    """删除账户确认按钮"""
    return ikb([[('🎯 确定', f'delemby-{embyid}')], [('🔙 取消', 'members')]])


def emby_block_ikb(embyid) -> InlineKeyboardMarkup:
    """Emby显示/隐藏按钮"""
    return ikb(
        [[("✔️️ - 显示", f"emby_unblock-{embyid}"), ("✖️ - 隐藏", f"emby_block-{embyid}")], [("🔙 返回", "members")]])


user_emby_block_ikb = ikb([[('✅ 已隐藏', 'members')]])
user_emby_unblock_ikb = ikb([[('❎ 已显示', 'members')]])

"""server ↓"""


def server_ikb() -> InlineKeyboardMarkup:
    """服务器面板按钮"""
    return ikb([[('📊 服务器状态', 'server_status')],
                [('🎬 媒体库统计', 'media_stats')],
                [('🔙 返回', 'back_start')]])

"""admin ↓"""


def admin_ikb() -> InlineKeyboardMarkup:
    """管理员面板按钮"""
    return ikb([[('👥 用户管理', 'user_manage')],
                [('⚙️ 系统设置', 'system_settings')],
                [('🔙 返回', 'back_start')]])

"""通用按钮"""


def close_button() -> InlineKeyboardMarkup:
    """关闭按钮"""
    return ikb([[('❌ 关闭', 'closeit')]])


def back_button(callback_data: str) -> InlineKeyboardMarkup:
    """返回按钮"""
    return ikb([[('🔙 返回', callback_data)]])


async def cr_kk_ikb(uid, first):
    """
    创建用户信息面板 - 完整版本
    :param uid: 用户ID
    :param first: 用户名字
    :return: (text, keyboard)
    """
    text = ''
    text1 = ''
    keyboard = []
    data = await members_info(uid)
    if data is None:
        text += f'**· 🆔 TG** ：[{first}](tg://user?id={uid}) [`{uid}`]\n数据库中没有此ID。ta 还没有私聊过我'
    else:
        name, lv, ex, us, embyid, pwd2 = data
        if name != '无账户信息':
            ban = "🌟 解除禁用" if lv == "**已禁用**" else '💢 禁用账户'
            keyboard = [[ban, f'user_ban-{uid}'], ['⚠️ 删除账户', f'closeemby-{uid}']]
            if len(extra_emby_libs) > 0:
                success, rep = emby.user(embyid=embyid)
                if success:
                    try:
                        currentblock = rep["Policy"]["BlockedMediaFolders"]
                    except KeyError:
                        currentblock = []
                    # 此处符号用于展示是否开启的状态
                    libs, embyextralib = ['✖️', f'embyextralib_unblock-{uid}'] if set(extra_emby_libs).issubset(
                        set(currentblock)) else ['✔️', f'embyextralib_block-{uid}']
                    keyboard.append([f'{libs} 额外媒体库', embyextralib])
            try:
                rst = await emby.emby_cust_commit(user_id=embyid, days=30)
                last_time = rst[0][0]
                toltime = rst[0][1]
                text1 = f"**· 🔋 上次活动** | {last_time.split('.')[0]}\n" \
                        f"**· 📅 过去30天** | {toltime} min"
            except (TypeError, IndexError, ValueError):
                text1 = f"**· 📅 过去30天未有记录**"
        else:
            keyboard.append(['✨ 赠送资格', f'gift-{uid}'])
        text += f"**· 🍉 TG&名称** | [{first}](tg://user?id={uid})\n" \
                f"**· 🍒 识别のID** | `{uid}`\n" \
                f"**· 🍓 当前状态** | {lv}\n" \
                f"**· 🍥 积分{sakura_b}** | {us[0]} · {us[1]}\n" \
                f"**· 💠 账号名称** | {name}\n" \
                f"**· 🚨 到期时间** | **{ex}**\n"
        text += text1
        keyboard.extend([['🚫 踢出并封禁', f'fuckoff-{uid}'], ['❌ 删除消息', 'closeit']])
        lines = array_chunk(keyboard, 2)
        keyboard = ikb(lines)
    return text, keyboard


# 分页相关函数
async def cr_page_server():
    """翻页服务器面板"""
    sever = nezha_res.sever_info(tz_ad, tz_api, tz_id)
    if not sever:
        return ikb([[('🔙 - 用户', 'members'), ('❌ - 上一级', 'back_start')]]), None
    d = []
    for i in sever:
        d.append([i['name'], f'server:{i["id"]}'])
    lines = array_chunk(d, 3)
    lines.append([['🔙 - 用户', 'members'], ['❌ - 上一级', 'back_start']])
    return ikb(lines), sever


# 管理员面板按钮
gm_ikb_content = ikb([[('⭕ 注册状态', 'open-menu'), ('🎟️ 注册/续期码', 'cr_link')],
                      [('💊 查询注册', 'ch_link'), ('🏬 兑换设置', 'set_renew')],
                      [('👥 用户列表', 'normaluser'), ('👑 白名单列表', 'whitelist')],
                      [('🌏 定时', 'schedall'), ('🕹️ 主界面', 'back_start'), ('其他 🪟', 'back_config')]])


def open_menu_ikb(openstats, timingstats) -> InlineKeyboardMarkup:
    """注册状态菜单"""
    return ikb([[(f'{openstats} 自由注册', 'open_stat'), (f'{timingstats} 定时注册', 'open_timing')],
                [('⭕ 注册限制', 'all_user_limit')], [('🌟 返回上一级', 'manage')]])


back_free_ikb = ikb([[('🔙 返回上一级', 'open-menu')]])
back_open_menu_ikb = ikb([[('🪪 重新定时', 'open_timing'), ('🔙 注册状态', 'open-menu')]])
re_cr_link_ikb = ikb([[('♻️ 继续创建', 'cr_link'), ('🎗️ 返回主页', 'manage')]])
close_it_ikb = ikb([[('❌ - Close', 'closeit')]])


def ch_link_ikb(ls: list) -> InlineKeyboardMarkup:
    """链接查询按钮"""
    lines = array_chunk(ls, 2)
    lines.append([["💫 回到首页", "manage"]])
    return ikb(lines)


def date_ikb(i) -> InlineKeyboardMarkup:
    """日期选择按钮"""
    return ikb([[('🌘 - 月', f'register_mon_{i}'), ('🌗 - 季', f'register_sea_{i}'),
                 ('🌖 - 半年', f'register_half_{i}')],
                [('🌕 - 年', f'register_year_{i}'), ('🎟️ - 已用', f'register_used_{i}')], [('🔙 - 返回', 'ch_link')]])


# 分页按钮函数
async def cr_paginate(i, j, n) -> InlineKeyboardMarkup:
    """通用分页按钮"""
    buttons = []
    # 计算分页
    total_pages = (i + 9) // 10  # 每页10个
    current_page = (j - 1) // 10 + 1
    
    if current_page > 1:
        buttons.append(('◀️ 上一页', f'pagination_keyboard:{current_page-1}-{n}'))
    if current_page < total_pages:
        buttons.append(('▶️ 下一页', f'pagination_keyboard:{current_page+1}-{n}'))
    
    buttons.append(('❌ 关闭', 'closeit'))
    return ikb([buttons])


async def users_iv_button(i, j, tg) -> InlineKeyboardMarkup:
    """用户邀请分页按钮"""
    buttons = []
    total_pages = (i + 9) // 10
    current_page = (j - 1) // 10 + 1
    
    if current_page > 1:
        buttons.append(('◀️ 上一页', f'users_iv:{current_page-1}_{tg}'))
    if current_page < total_pages:
        buttons.append(('▶️ 下一页', f'users_iv:{current_page+1}_{tg}'))
    
    buttons.append(('❌ 关闭', f'closeit_{tg}'))
    return ikb([buttons])


async def plays_list_button(i, j, days) -> InlineKeyboardMarkup:
    """播放列表分页按钮"""
    buttons = []
    total_pages = (i + 9) // 10
    current_page = (j - 1) // 10 + 1
    
    if current_page > 1:
        buttons.append(('◀️ 上一页', f'uranks:{current_page-1}_{days}'))
    if current_page < total_pages:
        buttons.append(('▶️ 下一页', f'uranks:{current_page+1}_{days}'))
    
    buttons.append(('❌ 关闭', 'closeit'))
    return ikb([buttons])


async def store_query_page(i, j) -> InlineKeyboardMarkup:
    """商店查询分页按钮"""
    buttons = []
    total_pages = (i + 9) // 10
    current_page = (j - 1) // 10 + 1
    
    if current_page > 1:
        buttons.append(('◀️ 上一页', f'store-query:{current_page-1}'))
    if current_page < total_pages:
        buttons.append(('▶️ 下一页', f'store-query:{current_page+1}'))
    
    buttons.extend([('❌ 关闭', 'closeit'), ('🔙 返回', 'storeall')])
    return ikb([buttons])


async def whitelist_page_ikb(total_page: int, current_page: int) -> InlineKeyboardMarkup:
    """白名单分页按钮"""
    buttons = []
    if total_page > 5:
        if current_page - 5 >= 1:
            buttons.append(('⏮️ 前进-5', f'whitelist:{current_page - 5}'))
        if current_page + 5 < total_page:
            buttons.append(('⏭️ 后退+5', f'whitelist:{current_page + 5}'))
    
    buttons.append(('🔙 返回', 'manage'))
    return ikb([buttons])


async def normaluser_page_ikb(total_page: int, current_page: int) -> InlineKeyboardMarkup:
    """普通用户分页按钮"""
    buttons = []
    if total_page > 5:
        if current_page - 5 >= 1:
            buttons.append(('⏮️ 前进-5', f'normaluser:{current_page - 5}'))
        if current_page + 5 < total_page:
            buttons.append(('⏭️ 后退+5', f'normaluser:{current_page + 5}'))
    
    buttons.append(('🔙 返回', 'manage'))
    return ikb([buttons])


def cr_renew_ikb():
    """续期设置按钮"""
    checkin = '✔️' if _open.checkin else '❌'
    exchange = '✔️' if _open.exchange else '❌'
    whitelist = '✔️' if _open.whitelist else '❌'
    invite = '✔️' if _open.invite else '❌'
    return ikb([
        [(f'{checkin} 每日签到', 'set_renew-checkin'), (f'{exchange} 自动{sakura_b}续期', 'set_renew-exchange')],
        [(f'{whitelist} 兑换白名单', 'set_renew-whitelist'), (f'{invite} 兑换邀请码', 'set_renew-invite')],
        [('◀ 返回', 'manage')]
    ])


# 配置面板按钮
def config_preparation() -> InlineKeyboardMarkup:
    """配置准备按钮"""
    leave_ban = '✅' if _open.leave_ban else '❎'
    uplays = '✅' if _open.uplays else '❎'
    moviepilot = '✅' if config.moviepilot_open else '❎'
    fuxx_pitao = '✅' if config.fuxx_pitao else '❎'
    return ikb([
        [('📄 导出日志', 'log_out'), ('📌 设置探针', 'set_tz')],
        [('💠 emby线路', 'set_line'), ('🎬 显/隐指定库', 'set_block')],
        [(f'{leave_ban} 退群封禁', 'leave_ban'), (f'{uplays} 自动看片结算', 'set_uplays')],
        [(f'{moviepilot} MP求片', 'set_moviepilot'), (f'{fuxx_pitao} 皮套人过滤功能', 'set_fuxx_pitao')],
        [(f'设置赠送资格天数({config.kk_gift_days}天)', 'set_kk_gift_days')],
        [('🔙 返回', 'manage')]
    ])


back_config_p_ikb = ikb([[("🎮  ️返回主控", "back_config")]])


def back_set_ikb(method) -> InlineKeyboardMarkup:
    """返回设置按钮"""
    return ikb([[("♻️ 重新设置", f"{method}"), ("🔙 返回主页", "back_config")]])


def try_set_buy(ls: list) -> InlineKeyboardMarkup:
    """尝试设置购买按钮"""
    d = [[ls], [("✅ 体验结束返回", "back_config")]]
    return ikb(d)


# 其他按钮
register_code_ikb = ikb([[('🎟️ 注册', 'create'), ('⭕ 取消', 'closeit')]])
dp_g_ikb = ikb([[("🈺 ╰(￣ω￣ｏ)", "t.me/fengzheng58", "url")]])


def cv_user_ip(user_id):
    """用户IP按钮"""
    return ikb([[('🌏 播放查询', f'userip-{user_id}'), ('❌ 关闭', 'closeit')]])


def gog_rester_ikb(link=None) -> InlineKeyboardMarkup:
    """注册链接按钮"""
    link_ikb = ikb([[('🎁 点击领取', link, 'url')]]) if link else ikb([[('👆🏻 点击注册', f't.me/{bot_name}', 'url')]])
    return link_ikb


# 调度面板按钮
def sched_buttons():
    """调度按钮"""
    dayrank = '✅' if schedall.dayrank else '❎'
    weekrank = '✅' if schedall.weekrank else '❎'
    dayplayrank = '✅' if schedall.dayplayrank else '❎'
    weekplayrank = '✅' if schedall.weekplayrank else '❎'
    check_ex = '✅' if schedall.check_ex else '❎'
    low_activity = '✅' if schedall.low_activity else '❎'
    backup_db = '✅' if schedall.backup_db else '❎'
    
    return ikb([
        [(f'{dayrank} 播放日榜', 'sched-dayrank'), (f'{weekrank} 播放周榜', 'sched-weekrank')],
        [(f'{dayplayrank} 看片日榜', 'sched-dayplayrank'), (f'{weekplayrank} 看片周榜', 'sched-weekplayrank')],
        [(f'{check_ex} 到期保号', 'sched-check_ex'), (f'{low_activity} 活跃保号', 'sched-low_activity')],
        [(f'{backup_db} 自动备份数据库', 'sched-backup_db')],
        [('🫧 返回', 'manage')]
    ])
