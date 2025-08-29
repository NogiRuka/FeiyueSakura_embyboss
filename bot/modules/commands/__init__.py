#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令模块初始化文件 - aiogram版本

职责：提供统一的命令路由注册入口。
"""

# 暂时只导入已迁移的模块
from .start import router as start_router

from typing import List
from aiogram import Dispatcher

# 收集所有路由器
routers: List = [start_router]

# 注册所有路由器
def register_all_routers(dispatcher: Dispatcher) -> None:
    """注册所有命令路由器。

    参数：
    - dispatcher: aiogram 的 `Dispatcher` 实例
    """
    for router in routers:
        dispatcher.include_router(router)
        print(f"✅ 已注册命令路由器: {router.name}")