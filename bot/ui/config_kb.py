#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiogram.types import InlineKeyboardMarkup

from bot import _open, config
from .core_kb import ikb


def config_preparation() -> InlineKeyboardMarkup:
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
    return ikb([[("♻️ 重新设置", f"{method}"), ("🔙 返回主页", "back_config")]])


def try_set_buy(ls: list) -> InlineKeyboardMarkup:
    d = [[ls], [("✅ 体验结束返回", "back_config")]]
    return ikb(d)


register_code_ikb = ikb([[('🎟️ 注册', 'create'), ('⭕ 取消', 'closeit')]])


__all__ = [
    'config_preparation', 'back_config_p_ikb', 'back_set_ikb', 'try_set_buy', 'register_code_ikb'
]


