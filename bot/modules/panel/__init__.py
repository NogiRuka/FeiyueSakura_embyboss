#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
面板模块初始化文件 - aiogram版本

职责：提供统一的面板路由注册入口。
"""

from typing import Iterable

from aiogram import Dispatcher

# 暂时只导入已迁移的模块
from .member_panel import register_member_panel_router

# 注册所有面板路由器
def register_all_panel_routers(dispatcher: Dispatcher) -> None:
    """注册所有面板路由器。

    参数：
    - dispatcher: aiogram 的 `Dispatcher` 实例
    """
    register_member_panel_router(dispatcher)
    print("✅ 已注册面板路由器: member_panel")
