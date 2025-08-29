#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
EmbyBot 主程序入口
从Pyrogram框架改为aiogram框架
"""

import asyncio
from aiogram import Dispatcher
from bot import bot, dp
from bot.routers import setup_routers

async def main():
    """主函数 - 启动机器人"""
    
    # 统一注册所有路由
    setup_routers(dp)
    
    # 启动机器人
    print("🚀 正在启动 EmbyBot...")
    print("✅ 基础功能已启动：start命令、用户面板、关闭消息")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())
