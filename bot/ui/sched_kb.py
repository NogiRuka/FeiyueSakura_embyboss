#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiogram.types import InlineKeyboardMarkup

from bot import schedall
from .core_kb import ikb


def sched_buttons() -> InlineKeyboardMarkup:
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


__all__ = ['sched_buttons']


