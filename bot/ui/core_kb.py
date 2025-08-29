#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
核心按键构造工具：通用的 ikb 与辅助函数。
"""

from typing import List, Tuple, Union
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_inline_keyboard(buttons: List[List[Tuple[str, str, str]]]) -> InlineKeyboardMarkup:
    keyboard: List[List[InlineKeyboardButton]] = []
    for row in buttons:
        keyboard_row: List[InlineKeyboardButton] = []
        for button in row:
            text, callback_data, button_type = button
            if button_type == 'url':
                keyboard_row.append(InlineKeyboardButton(text=text, url=callback_data))
            else:
                keyboard_row.append(InlineKeyboardButton(text=text, callback_data=callback_data))
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def array_chunk(data: List, chunk_size: int) -> List[List]:
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def ikb(buttons: List[List[Union[str, Tuple[str, str]]]]) -> InlineKeyboardMarkup:
    keyboard: List[List[InlineKeyboardButton]] = []
    for row in buttons:
        keyboard_row: List[InlineKeyboardButton] = []
        for button in row:
            if isinstance(button, tuple):
                if len(button) == 2:
                    text, callback_data = button
                    keyboard_row.append(InlineKeyboardButton(text=text, callback_data=callback_data))
                elif len(button) == 3:
                    text, callback_data, button_type = button
                    if button_type == 'url':
                        keyboard_row.append(InlineKeyboardButton(text=text, url=callback_data))
                    else:
                        keyboard_row.append(InlineKeyboardButton(text=text, callback_data=callback_data))
            else:
                keyboard_row.append(InlineKeyboardButton(text=button, callback_data=button))
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


__all__ = ["create_inline_keyboard", "array_chunk", "ikb"]


