#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import sys
from typing import Any

from loguru import logger

# 确保日志目录存在
os.makedirs("log", exist_ok=True)

Now: datetime.datetime = datetime.datetime.now()

# 移除默认处理器
logger.remove()

# 添加控制台输出处理器，显示彩色日志
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True,
)

# 添加文件处理器，按日期轮换
logger.add(
    f"log/log_{Now:%Y%m%d}.txt",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name} | {function}:{line} - {message}",
    level="DEBUG",  # 文件中记录更详细的日志级别
    rotation="00:00",
    retention="30 days",
    compression="zip",  # 压缩旧日志文件
    backtrace=True,     # 异常时显示完整堆栈跟踪
    diagnose=True,      # 显示变量值
)

# 添加错误日志专用文件
logger.add(
    f"log/error_{Now:%Y%m%d}.txt",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name} | {function}:{line} - {message}",
    level="ERROR",  # 只记录错误及以上级别
    rotation="00:00",
    retention="60 days",  # 错误日志保留更长时间
    compression="zip",
    backtrace=True,
    diagnose=True,
)


def logu(name: str):
    """获取带有模块名绑定的 logger。"""
    return logger.bind(name=name)


__all__ = ["logu", "Now", "logger"]


