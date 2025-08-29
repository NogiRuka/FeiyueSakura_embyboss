#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aiogram.types import InlineKeyboardMarkup

from bot import chanel, main_group, bot_name, _open
from bot.common.utils import judge_admins
from .core_kb import ikb, array_chunk


def judge_start_ikb(uid: int) -> InlineKeyboardMarkup:
    d = [('️👥 用户功能', 'members'), ('🌐 服务器', 'server'), ('🎟️ 使用注册/续期码', 'exchange')]
    if _open.checkin:
        d.append((f'🎯 签到', 'checkin'))
    lines = array_chunk(d, 2)
    if judge_admins(uid):
        lines.append([('👮🏻‍♂️ admin', 'manage')])
    return ikb(lines)


group_f = ikb([[('点击我(●ˇ∀ˇ●)', f't.me/{bot_name}', 'url')]])

judge_group_ikb = ikb([[('🌟 频道入口 ', f't.me/{chanel}', 'url'),
                        ('💫 群组入口', f't.me/{main_group}', 'url')],
                       [('❌ 关闭消息', 'closeit')]])


__all__ = ["judge_start_ikb", "group_f", "judge_group_ikb"]


