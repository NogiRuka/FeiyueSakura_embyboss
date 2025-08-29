#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试脚本 - 验证基本功能
"""

print("开始简单测试...")

try:
    print("1. 测试基础配置导入...")
    from bot import bot, dp
    print("✅ bot和dp导入成功")
    
    print("2. 测试按钮模块导入...")
    from bot.ui.aiogram_buttons import judge_start_ikb, group_f
    print("✅ 按钮模块导入成功")
    
    print("3. 测试消息工具模块导入...")
    from bot.messaging.msg_utils import sendMessage, editMessage
    print("✅ 消息工具模块导入成功")
    
    print("\n🎉 基本功能测试通过！")
    print(f"Bot Token: {bot.token[:10]}...")
    
    # 测试按钮创建
    keyboard = judge_start_ikb(123456789)
    print(f"按钮创建成功: {type(keyboard)}")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
