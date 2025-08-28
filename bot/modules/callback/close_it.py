#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关闭消息回调处理器 - aiogram版本
"""

from aiogram import Router, F
from aiogram.types import CallbackQuery

# 创建路由器
router = Router(name="close_it")

@router.callback_query(F.data == "closeit")
async def close_message_callback(callback: CallbackQuery):
    """关闭消息"""
    try:
        await callback.message.delete()
        await callback.answer("✅ 消息已关闭")
    except Exception as e:
        await callback.answer("❌ 无法删除消息")

# 注册路由器
def register_close_it_router():
    from bot import dp
    dp.include_router(router)
