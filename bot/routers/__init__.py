#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一路由注册模块

职责：集中收口 commands / panel / callback 的路由注册，
由入口处调用一次，便于后续扩展与维护。
"""

from typing import Any

from aiogram import Dispatcher


def setup_routers(dispatcher: Dispatcher) -> None:
    """聚合注册所有路由。

    - commands: 文本命令类处理
    - panel:    面板交互类处理
    - callback: 回调按钮类处理
    """
    # 命令路由
    from bot.modules.commands import register_all_routers as register_commands
    register_commands(dispatcher)

    # 面板路由
    from bot.modules.panel import register_all_panel_routers as register_panels
    register_panels(dispatcher)

    # 回调路由
    from bot.modules.callback import register_all_callback_routers as register_callbacks
    register_callbacks(dispatcher)

    print("✅ 已完成统一路由注册")


