#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
EmbyBot 主程序入口
从Pyrogram框架改为aiogram框架
"""

import asyncio
from bot import bot, dp
from bot.modules.panel import register_all_panel_routers  # 面板模块路由器注册函数
from bot.modules.commands import register_all_routers  # 命令模块路由器注册函数
# from bot.modules.extra import *  # 其他功能模块 - 暂时注释，等待迁移
from bot.modules.callback import register_all_callback_routers  # 回调模块路由器注册函数

async def main():
    """主函数 - 启动机器人"""
    
    # 注册所有命令路由器
    register_all_routers(dp)
    
    # 注册所有面板路由器
    register_all_panel_routers(dp)
    
    # 注册所有回调路由器
    register_all_callback_routers(dp)
    
    # 启动机器人
    print("🚀 正在启动 EmbyBot...")
    print("✅ 基础功能已启动：start命令、用户面板、关闭消息")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())
