#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
回调模块初始化文件 - aiogram版本
"""

# 暂时只导入已迁移的模块
from .close_it import register_close_it_router

# 注册所有回调路由器
def register_all_callback_routers(dp):
    """注册所有回调路由器"""
    from bot import dp as bot_dp
    register_close_it_router()
    print("✅ 已注册回调路由器: close_it")
