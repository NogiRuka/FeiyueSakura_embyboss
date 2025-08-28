#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
start命令处理器 - aiogram版本
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot import bot, dp, owner, group, main_group, bot_name, chanel
from bot.func_helper.aiogram_buttons import judge_start_ikb, judge_group_ikb, group_f
from bot.func_helper.msg_utils import sendMessage, editMessage
from bot.func_helper.utils import judge_admins

# 创建路由器
router = Router(name="start")

@router.message(Command("start"))
async def start_command(message: Message):
    """处理 /start 命令"""
    uid = message.from_user.id
    first = message.from_user.first_name or "用户"
    
    # 检查是否在群组中
    if message.chat.type != "private":
        # 在群组中，显示群组入口
        keyboard = judge_group_ikb
        text = f"🌟 **欢迎使用 {bot_name}**\n\n💫 请在私聊中使用机器人功能"
        await message.reply(text, reply_markup=keyboard)
        return
    
    # 私聊中，显示主菜单
    keyboard = judge_start_ikb(uid)
    text = f"🌟 **欢迎使用 {bot_name}**\n\n👋 你好 {first}！\n请选择以下功能："
    
    await message.reply(text, reply_markup=keyboard)

@router.callback_query(F.data == "back_start")
async def back_start_callback(callback: CallbackQuery):
    """返回主菜单"""
    uid = callback.from_user.id
    first = callback.from_user.first_name or "用户"
    
    keyboard = judge_start_ikb(uid)
    text = f"🌟 **{bot_name} 主菜单**\n\n👋 你好 {first}！\n请选择以下功能："
    
    await editMessage(callback, text, keyboard)

@router.callback_query(F.data == "closeit")
async def close_message_callback(callback: CallbackQuery):
    """关闭消息"""
    try:
        await callback.message.delete()
        await callback.answer("✅ 消息已关闭")
    except Exception as e:
        await callback.answer("❌ 无法删除消息")

# 注册路由器
def register_start_router():
    dp.include_router(router)
