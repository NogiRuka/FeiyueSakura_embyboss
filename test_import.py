#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证模块导入是否正常
"""

print("开始测试模块导入...")

try:
    print("1. 测试基础模块导入...")
    from bot import bot, dp
    print("✅ bot和dp导入成功")
    
    print("2. 测试命令模块导入...")
    from bot.modules.commands import routers as command_routers
    print("✅ 命令模块导入成功")
    
    print("3. 测试面板模块导入...")
    from bot.modules.panel import *
    print("✅ 面板模块导入成功")
    
    print("4. 测试其他模块导入...")
    from bot.modules.extra import *
    from bot.modules.callback import *
    print("✅ 其他模块导入成功")
    
    print("\n🎉 所有模块导入测试通过！")
    print(f"Bot Token: {bot.token[:10]}...")
    print(f"路由器数量: {len(command_routers)}")
    
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
