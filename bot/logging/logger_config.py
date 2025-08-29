#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 直接复用原实现（从 bot/func_helper/logger_config.py 移动）

import datetime
from typing import Any

from loguru import logger

Now: datetime.datetime = datetime.datetime.now()

logger.add(
    f"log/log_{Now:%Y%m%d}.txt",
    format="{time} - {name} - {level} - {message}",
    level="INFO",
    rotation="00:00",
    retention="30 days",
)


def logu(name: str):
    """获取带有模块名绑定的 logger。"""
    return logger.bind(name=name)


__all__ = ["logu", "Now", "logger"]


