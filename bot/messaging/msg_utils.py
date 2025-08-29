#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 从 bot/func_helper/msg_utils.py 迁移的实现（已带类型注解），保留对外 API 不变

import asyncio
from typing import Optional, Union

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message
from bot import LOGGER, group, bot


class ListenerTimeout(Exception):
    """监听超时异常"""
    pass


async def sendMessage(
    message: Union[Message, CallbackQuery],
    text: str,
    buttons=None,
    timer: Optional[int] = None,
    send: bool = False,
    chat_id: Optional[int] = None,
):
    if isinstance(message, CallbackQuery):
        message = message.message
    try:
        if send is True:
            if chat_id is None:
                chat_id = group[0]
            return await bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons)
        send_msg = await message.reply(text=text, quote=True, disable_web_page_preview=True, reply_markup=buttons)
        if timer is not None:
            return await deleteMessage(send_msg, timer)
        return True
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)


async def editMessage(
    message: Union[Message, CallbackQuery],
    text: str,
    buttons=None,
    timer: Optional[int] = None,
):
    if isinstance(message, CallbackQuery):
        message = message.message
    try:
        edt = await message.edit_text(text=text, disable_web_page_preview=True, reply_markup=buttons)
        if timer is not None:
            return await deleteMessage(edt, timer)
        return True
    except TelegramBadRequest as e:
        if 'BUTTON_URL_INVALID' in str(e):
            return False
        if "MESSAGE_NOT_MODIFIED" in str(e) or 'MESSAGE_ID_INVALID' in str(e):
            return False
        else:
            LOGGER.warning(e)
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)


async def sendFile(
    message: Union[Message, CallbackQuery],
    file,
    file_name: str,
    caption: Optional[str] = None,
    buttons=None,
):
    if isinstance(message, CallbackQuery):
        message = message.message
    try:
        await message.reply_document(document=file, caption=caption, reply_markup=buttons)
        return True
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)


async def sendPhoto(
    message: Union[Message, CallbackQuery],
    photo,
    caption: Optional[str] = None,
    buttons=None,
    timer: Optional[int] = None,
    send: bool = False,
    chat_id: Optional[int] = None,
):
    if isinstance(message, CallbackQuery):
        message = message.message
    try:
        if send is True:
            if chat_id is None:
                chat_id = group[0]
            return await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=buttons)
        send_msg = await message.reply_photo(photo=photo, caption=caption, reply_markup=buttons)
        if timer is not None:
            return await deleteMessage(send_msg, timer)
        return True
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)


async def deleteMessage(message: Union[Message, CallbackQuery], timer: Optional[int] = None):
    if timer is not None:
        await asyncio.sleep(timer)
    if isinstance(message, CallbackQuery):
        try:
            await message.message.delete()
            return await callAnswer(message, '✔️ Done!')
        except Exception as e:
            LOGGER.error(e)
            return str(e)
    else:
        try:
            await message.delete()
            return True
        except Exception as e:
            LOGGER.warning(e)
            await message.reply(f'⚠️ **错误！**检查群组 `{message.chat.id}` 权限 【删除消息】')
        except Exception as e:
            LOGGER.error(e)
            return str(e)


async def callAnswer(callbackquery: CallbackQuery, query: str, show_alert: bool = False):
    try:
        await callbackquery.answer(query, show_alert=show_alert)
        return True
    except TelegramBadRequest as e:
        if "QUERY_ID_INVALID" in str(e):
            return False
        else:
            LOGGER.error(str(e))
            return False
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)


async def callListen(callbackquery: CallbackQuery, timer: int = 120, buttons=None):
    try:
        await editMessage(callbackquery, '💦 __功能暂未实现__ **请等待更新！**', buttons=buttons)
        return False
    except ListenerTimeout:
        await editMessage(callbackquery, '💦 __没有获取到您的输入__ **会话状态自动取消！**', buttons=buttons)
        return False


async def call_dice_Listen(callbackquery: CallbackQuery, timer: int = 120, buttons=None):
    try:
        await editMessage(callbackquery, '💦 __功能暂未实现__ **请等待更新！**', buttons=buttons)
        return False
    except ListenerTimeout:
        await editMessage(callbackquery, '💦 __没有获取到您的输入__ **会话状态自动取消！**', buttons=buttons)
        return False


async def callAsk(callbackquery: CallbackQuery, text: str, timer: int = 120, button=None):
    try:
        return False
    except:
        return False


async def ask_return(update: Union[Message, CallbackQuery], text: str, timer: int = 120, button=None):
    if isinstance(update, CallbackQuery):
        update = update.message
    try:
        await sendMessage(update, '💦 __功能暂未实现__ **请等待更新！**', buttons=button)
        return False
    except ListenerTimeout:
        await sendMessage(update, '💦 __没有获取到您的输入__ **会话状态自动取消！**', buttons=button)
        return False


import re
import html


def escape_html_special_chars(text: str) -> str:
    pattern = r"[\\`*_{}\[\]()#+-.!|]"
    text = re.sub(pattern, r"\\\g<0>", text)
    text = html.escape(text)
    return text


def escape_markdown(text: Optional[str]) -> str:
    return (
        re.sub(r"([_*\[\]()~`>\#\+\-=|{}\.!\\])", r"\\\1", html.unescape(text))
        if text
        else str()
    )


