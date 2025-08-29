#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiogram.types import InlineKeyboardMarkup

from bot import extra_emby_libs, sakura_b, tz_id, tz_ad, tz_api, schedall, config
from bot.integrations import nezha_res
from bot.integrations.emby import emby
from bot.common.utils import members_info
from .core_kb import ikb, array_chunk


def members_ikb(emby: bool = False) -> InlineKeyboardMarkup:
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
    buttons = []
    if has_prev:
        buttons.append(('◀️ 上一页', 'pre_page_request_record'))
    if has_next:
        buttons.append(('▶️ 下一页', 'next_page_request_record'))
    return ikb([buttons, [('🔙 返回', 'download_center')]])


re_born_ikb = ikb([[('✨ 重输', 'store-reborn'), ('💫 返回', 'storeall')]])


def store_ikb():
    return ikb([[(f'♾️ 兑换白名单', 'store-whitelist'), (f'🔥 兑换解封禁', 'store-reborn')],
                [(f'🎟️ 兑换注册码', 'store-invite'), (f'🔍 查询注册码', 'store-query')],
                [(f'❌ 取消', 'members')]])


re_store_renew = ikb([[('✨ 重新输入', 'changetg'), ('💫 取消输入', 'storeall')]])


def del_me_ikb(embyid) -> InlineKeyboardMarkup:
    return ikb([[('🎯 确定', f'delemby-{embyid}')], [('🔙 取消', 'members')]])


def emby_block_ikb(embyid) -> InlineKeyboardMarkup:
    return ikb(
        [[("✔️️ - 显示", f"emby_unblock-{embyid}"), ("✖️ - 隐藏", f"emby_block-{embyid}")], [("🔙 返回", "members")]])


user_emby_block_ikb = ikb([[('✅ 已隐藏', 'members')]])
user_emby_unblock_ikb = ikb([[('❎ 已显示', 'members')]])


__all__ = [
    'members_ikb', 'back_start_ikb', 'back_members_ikb', 're_create_ikb', 're_changetg_ikb', 're_bindtg_ikb',
    're_delme_ikb', 're_reset_ikb', 're_exchange_b_ikb', 're_download_center_ikb', 'page_request_record_ikb',
    're_born_ikb', 'store_ikb', 're_store_renew', 'del_me_ikb', 'emby_block_ikb', 'user_emby_block_ikb',
    'user_emby_unblock_ikb'
]


