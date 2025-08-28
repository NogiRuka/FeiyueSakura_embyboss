#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
面板模块初始化文件 - aiogram版本
"""

# 暂时只导入已迁移的模块
from .member_panel import register_member_panel_router

# 注册所有面板路由器
def register_all_panel_routers(dp):
    """注册所有面板路由器"""
    from bot import dp as bot_dp
    register_member_panel_router()
    print("✅ 已注册面板路由器: member_panel")
