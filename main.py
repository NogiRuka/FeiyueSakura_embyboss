#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
EmbyBot 主程序入口
从Pyrogram框架改为aiogram框架
"""

import asyncio
from bot import bot, dp
# from bot.modules.panel import *  # 面板模块 - 暂时注释，等待迁移
# from bot.modules.commands import routers as command_routers  # 命令模块路由器 - 暂时注释，等待迁移
# from bot.modules.extra import *  # 其他功能模块 - 暂时注释，等待迁移
# from bot.modules.callback import *  # 回调处理模块 - 暂时注释，等待迁移

async def main():
    """主函数 - 启动机器人"""
    
    # 暂时注释掉路由器注册，等待完成迁移
    # for router in command_routers:
    #     dp.include_router(router)
    #     print(f"✅ 已注册路由器: {router.name}")
    
    # 启动机器人
    print("🚀 正在启动 EmbyBot...")
    print("⚠️  注意：目前只启动了基础框架，功能模块尚未迁移完成")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())
