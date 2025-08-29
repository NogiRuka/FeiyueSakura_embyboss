#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aiogram 按钮聚合导出（新分层）。

从 ui 子模块聚合公开 API，彻底移除对旧 func_helper 的依赖。
"""

from .core_kb import *
from .start_kb import *
from .members_kb import *
from .admin_kb import *
from .config_kb import *
from .sched_kb import *

