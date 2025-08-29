#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
回调模块初始化文件 - aiogram版本

职责：提供统一的回调路由注册入口。
"""

from aiogram import Dispatcher

# 暂时只导入已迁移的模块
from .close_it import register_close_it_router

# 注册所有回调路由器
def register_all_callback_routers(dispatcher: Dispatcher) -> None:
    """注册所有回调路由器。

    参数：
    - dispatcher: aiogram 的 `Dispatcher` 实例
    """
    register_close_it_router(dispatcher)
    print("✅ 已注册回调路由器: close_it")
