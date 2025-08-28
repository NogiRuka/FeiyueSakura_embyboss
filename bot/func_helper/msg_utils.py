#! /usr/bin/python3
# -*- coding: utf-8 -*-

import asyncio
from aiogram import F
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message
from bot import LOGGER, group, bot

# 自定义异常类，替代 pyromod 的 ListenerTimeout
class ListenerTimeout(Exception):
    """监听超时异常"""
    pass


# 将来自己要是重写，希望不要把/cancel当关键词，用call.data，省代码还好看，切记。

async def sendMessage(message, text: str, buttons=None, timer=None, send=False, chat_id=None):
    """
    发送消息
    :param message: 消息
    :param text: 实体
    :param buttons: 按钮
    :param timer: 定时删除
    :param send: 非reply,发送到第一个主授权群组
    :return:
    """
    if isinstance(message, CallbackQuery):
        message = message.message
    try:
        if send is True:
            if chat_id is None:
                chat_id = group[0]
            return await bot.send_message(chat_id=chat_id, text=text, reply_markup=buttons)
        # 禁用通知 disable_notification=True,
        send = await message.reply(text=text, quote=True, disable_web_page_preview=True, reply_markup=buttons)
        if timer is not None:
            return await deleteMessage(send, timer)
        return True
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)


async def editMessage(message, text: str, buttons=None, timer=None):
    """
    编辑消息
    :param message:
    :param text:
    :param buttons:
    :return:
    """
    if isinstance(message, CallbackQuery):
        message = message.message
    try:
        edt = await message.edit_text(text=text, disable_web_page_preview=True, reply_markup=buttons)
        if timer is not None:
            return await deleteMessage(edt, timer)
        return True
    except TelegramBadRequest as e:
        if 'BUTTON_URL_INVALID' in str(e):
            # await editMessage(message, text='⚠️ 底部按钮设置失败。', buttons=back_start_ikb)
            return False
        # 判断是否是因为编辑到一样的消息
        if "MESSAGE_NOT_MODIFIED" in str(e) or 'MESSAGE_ID_INVALID' in str(e):
            # await callAnswer(message, "慢速模式开启，切勿多点\n慢一点，慢一点，生活更有趣 - zztai", True)
            return False
        else:
            # 记录或处理其他异常
            LOGGER.warning(e)
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)


async def sendFile(message, file, file_name, caption=None, buttons=None):
    """
    发送文件
    :param message:
    :param file:
    :param file_name:
    :param caption:
    :param buttons:
    :return:
    """
    if isinstance(message, CallbackQuery):
        message = message.message
    try:
        await message.reply_document(document=file, caption=caption, reply_markup=buttons)
        return True
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)


async def sendPhoto(message, photo, caption=None, buttons=None, timer=None, send=False, chat_id=None):
    """
    发送图片
    :param message:
    :param photo:
    :param caption:
    :param buttons:
    :param timer:
    :param send: 是否发送到授权主群
    :return:
    """
    if isinstance(message, CallbackQuery):
        message = message.message
    try:
        if send is True:
            if chat_id is None:
                chat_id = group[0]
            return await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=buttons)
        # quote=True 引用回复
        send = await message.reply_photo(photo=photo, caption=caption, reply_markup=buttons)
        if timer is not None:
            return await deleteMessage(send, timer)
        return True
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)


async def deleteMessage(message, timer=None):
    """
    删除消息,带定时
    :param message:
    :param timer:
    :return:
    """
    if timer is not None:
        await asyncio.sleep(timer)
    if isinstance(message, CallbackQuery):
        try:
            await message.message.delete()
            return await callAnswer(message, '✔️ Done!')  # 返回 True 表示删除成功
        except Exception as e:
            LOGGER.error(e)
            return str(e)  # 返回异常字符串表示删除出错
    else:
        try:
            await message.delete()
            return True  # 返回 True 表示删除成功
        except Exception as e:
            LOGGER.warning(e)
            await message.reply(f'⚠️ **错误！**检查群组 `{message.chat.id}` 权限 【删除消息】')
            # return await deleteMessage(send, 60)
        except Exception as e:
            LOGGER.error(e)
            return str(e)  # 返回异常字符串表示删除出错


async def callAnswer(callbackquery: CallbackQuery, query, bool=False):
    try:
        await callbackquery.answer(query, show_alert=bool)
        return True
    except TelegramBadRequest as e:
        # 判断异常的消息是否是 "Query_id_invalid"
        if "QUERY_ID_INVALID" in str(e):
            # 忽略这个异常
            return False
        else:
            LOGGER.error(str(e))
            return False
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)


async def callListen(callbackquery, timer: int = 120, buttons=None):
    try:
        # TODO: 实现 aiogram 版本的监听功能
        # 这里需要根据 aiogram 的架构重新设计
        await editMessage(callbackquery, '💦 __功能暂未实现__ **请等待更新！**', buttons=buttons)
        return False
    except ListenerTimeout:
        await editMessage(callbackquery, '💦 __没有获取到您的输入__ **会话状态自动取消！**', buttons=buttons)
        return False


async def call_dice_Listen(callbackquery, timer: int = 120, buttons=None):
    try:
        # TODO: 实现 aiogram 版本的骰子监听功能
        # 这里需要根据 aiogram 的架构重新设计
        await editMessage(callbackquery, '💦 __功能暂未实现__ **请等待更新！**', buttons=buttons)
        return False
    except ListenerTimeout:
        await editMessage(callbackquery, '💦 __没有获取到您的输入__ **会话状态自动取消！**', buttons=buttons)
        return False


async def callAsk(callbackquery, text, timer: int = 120, button=None):
    # TODO: 实现 aiogram 版本的 ask 功能
    # 这里需要根据 aiogram 的架构重新设计
    try:
        # 暂时返回 False，等待实现
        return False
    except:
        return False


async def ask_return(update, text, timer: int = 120, button=None):
    if isinstance(update, CallbackQuery):
        update = update.message
    try:
        # TODO: 实现 aiogram 版本的 ask 功能
        # 这里需要根据 aiogram 的架构重新设计
        await sendMessage(update, '💦 __功能暂未实现__ **请等待更新！**', buttons=button)
        return False
    except ListenerTimeout:
        await sendMessage(update, '💦 __没有获取到您的输入__ **会话状态自动取消！**', buttons=button)
        return False


import re
import html


# 转义特殊字符
def escape_html_special_chars(text):
    # 定义一些常用的字符
    pattern = r"[\\`*_{}[\]()#+-.!|]"
    # 使用正则表达式替换掉特殊字符
    text = re.sub(pattern, r"\\\g<0>", text)
    # 使用html模块转义HTML的特殊字符
    text = html.escape(text)
    return text


def escape_markdown(text):
    return (
        re.sub(r"([_*\[\]()~`>\#\+\-=|{}\.!\\])", r"\\\1", html.unescape(text))
        if text
        else str()
    )
