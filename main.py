#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
EmbyBot 主程序入口
从Pyrogram框架改为aiogram框架
"""

import asyncio
from bot import bot, dp
from bot.modules.panel import *  # 面板模块
from bot.modules.commands import routers as command_routers  # 命令模块路由器
from bot.modules.extra import *  # 其他功能模块
from bot.modules.callback import *  # 回调处理模块

async def main():
    """主函数 - 启动机器人"""
    
    # 注册所有命令路由器
    for router in command_routers:
        dp.include_router(router)
        print(f"✅ 已注册路由器: {router.name}")
    
    # 启动机器人
    print("🚀 正在启动 EmbyBot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())
