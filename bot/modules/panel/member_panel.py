#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户面板模块 - aiogram版本
"""

from aiogram import Router, F, Dispatcher
from aiogram.types import CallbackQuery
from bot.ui.aiogram_buttons import (
    members_ikb, back_start_ikb, back_members_ikb,
    re_create_ikb, re_changetg_ikb, re_bindtg_ikb
)
from bot.messaging.msg_utils import editMessage
from bot.common.utils import user_in_group_filter

# 创建路由器
router = Router(name="member_panel")

@router.callback_query(F.data == "members")
async def members_panel_callback(callback: CallbackQuery):
    """用户面板"""
    # 添加详细日志
    from bot import LOGGER
    LOGGER.info(f"🎯 用户面板回调 - 用户ID: {callback.from_user.id}, 用户名: @{callback.from_user.username}")
    LOGGER.info(f"🎯 回调数据: {callback.data}")
    
    if not await user_in_group_filter(callback):
        LOGGER.warning(f"⚠️ 用户 {callback.from_user.id} 不在授权群组中")
        await callback.answer("❌ 您不在授权群组中")
        return
    
    # TODO: 检查用户是否有Emby账户
    has_emby = False  # 暂时设为False，后续实现数据库检查
    
    keyboard = members_ikb(has_emby)
    text = "👥 **用户功能面板**\n\n请选择您需要的功能："
    
    await editMessage(callback, text, keyboard)

@router.callback_query(F.data == "create")
async def create_account_callback(callback: CallbackQuery):
    """创建账户"""
    if not await user_in_group_filter(callback):
        await callback.answer("❌ 您不在授权群组中")
        return
    
    text = "👑 **创建Emby账户**\n\n请输入您想要的用户名："
    keyboard = re_create_ikb
    
    await editMessage(callback, text, keyboard)

@router.callback_query(F.data == "changetg")
async def change_tg_callback(callback: CallbackQuery):
    """换绑TG"""
    if not await user_in_group_filter(callback):
        await callback.answer("❌ 您不在授权群组中")
        return
    
    text = "⭕ **换绑Telegram账户**\n\n此功能暂未实现，请等待更新"
    keyboard = re_changetg_ikb
    
    await editMessage(callback, text, keyboard)

@router.callback_query(F.data == "bindtg")
async def bind_tg_callback(callback: CallbackQuery):
    """绑定TG"""
    if not await user_in_group_filter(callback):
        await callback.answer("❌ 您不在授权群组中")
        return
    
    text = "🔍 **绑定Telegram账户**\n\n此功能暂未实现，请等待更新"
    keyboard = re_bindtg_ikb
    
    await editMessage(callback, text, keyboard)

# 注册路由器
def register_member_panel_router(dispatcher: Dispatcher) -> None:
    """注册用户面板路由到指定 `dispatcher`。"""
    dispatcher.include_router(router)