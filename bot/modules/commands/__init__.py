#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令模块初始化文件 - aiogram版本
"""

# 暂时只导入已迁移的模块
from .start import router as start_router

# 收集所有路由器
routers = [
    start_router,
]

# 注册所有路由器
def register_all_routers(dp):
    """注册所有命令路由器"""
    for router in routers:
        dp.include_router(router)
        print(f"✅ 已注册命令路由器: {router.name}")