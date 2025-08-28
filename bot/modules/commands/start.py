"""
启动面板start命令 返回面板
从Pyrogram框架改为aiogram框架

+ myinfo 个人数据
+ count  服务器媒体数
"""
import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.func_helper.emby import Embyservice
from bot.modules.commands.exchange import rgs_code
from bot.sql_helper.sql_emby import sql_add_emby
from bot.func_helper.filters import user_in_group_filter, user_in_group_on_filter
from bot.func_helper.msg_utils import deleteMessage, sendMessage, sendPhoto, callAnswer, editMessage
from bot.func_helper.fix_bottons import group_f, judge_start_ikb, judge_group_ikb, cr_kk_ikb
from bot import bot, prefixes, group, bot_photo, ranks
from bot.func_helper import moviepilot

# 创建路由器
router = Router()

# 反命令提示 - 在群组中使用私聊命令
@router.message(Command("start", prefixes=prefixes), F.chat.id.in_(group))
@router.message(Command("count", prefixes=prefixes), F.chat.id.in_(group))
async def ui_g_command(msg: Message):
    """在群组中使用私聊命令的提示"""
    await asyncio.gather(
        deleteMessage(msg),
        sendMessage(msg,
                    f"🤖 亲爱的 [{msg.from_user.first_name}](tg://user?id={msg.from_user.id}) 这是一条私聊命令",
                    buttons=group_f, timer=60)
    )


# 查看自己的信息
@router.message(Command("myinfo", prefixes=prefixes), user_in_group_on_filter)
async def my_info(msg: Message):
    """查看用户个人信息"""
    await msg.delete()
    if msg.sender_chat:
        return
    text, keyboard = await cr_kk_ikb(uid=msg.from_user.id, first=msg.from_user.first_name)
    await sendMessage(msg, text, timer=60)


@router.message(Command("count", prefixes=prefixes), user_in_group_on_filter, F.chat.type == "private")
async def count_info(msg: Message):
    """查看媒体库数量"""
    await deleteMessage(msg)
    text = Embyservice.get_medias_count()
    await sendMessage(msg, text, timer=60)


# 私聊开启面板
@router.message(Command("start", prefixes=prefixes), F.chat.type == "private")
async def p_start(msg: Message):
    """私聊启动命令 - 显示主面板"""
    if not await user_in_group_filter(msg):
        return await asyncio.gather(
            deleteMessage(msg),
            sendMessage(msg,
                        '💢 拜托啦！请先点击下面加入我们的群组和频道，然后再 /start 一下好吗？',
                        buttons=judge_group_ikb)
        )
    
    try:
        # 处理邀请链接
        u = msg.text.split()[1].split('-')[0]
        if u in f'{ranks.logo}' or u == str(msg.from_user.id):
            await asyncio.gather(msg.delete(), rgs_code(msg, register_code=msg.text.split()[1]))
        else:
            await asyncio.gather(sendMessage(msg, '🤺 你也想和bot击剑吗 ?'), msg.delete())
    except (IndexError, TypeError):
        # 正常启动显示主面板
        await asyncio.gather(
            deleteMessage(msg),
            sendPhoto(msg, bot_photo,
                      f"**✨ 只有你想见我的时候我们的相遇才有意义**\n\n🍉__你好鸭 [{msg.from_user.first_name}](tg://user?id={msg.from_user.id}) 请选择功能__👇",
                      buttons=judge_start_ikb(msg.from_user.id))
        )
        sql_add_emby(msg.from_user.id)


# 返回面板
@router.callback_query(F.data == "back_start")
async def b_start(call: CallbackQuery):
    """返回主面板的回调处理"""
    if await user_in_group_filter(call):
        await asyncio.gather(
            callAnswer(call, "⭐ 返回start"),
            editMessage(call,
                        text=f"**✨ 只有你想见我的时候我们的相遇才有意义**\n\n🍉__你好鸭 [{call.from_user.first_name}](tg://user?id={call.from_user.id}) 请选择功能__👇",
                        buttons=judge_start_ikb(call.from_user.id))
        )
    elif not await user_in_group_filter(call):
        await asyncio.gather(
            callAnswer(call, "⭐ 返回start"),
            editMessage(call, 
                        text='💢 拜托啦！请先点击下面加入我们的群组和频道，然后再 /start 一下好吗？',
                        buttons=judge_group_ikb)
        )


@router.callback_query(F.data == "store_all")
async def store_alls(call: CallbackQuery):
    """商店全部功能的回调处理"""
    if not await user_in_group_filter(call):
        await asyncio.gather(
            callAnswer(call, "⭐ 返回start"),
            deleteMessage(call), 
            sendPhoto(call, bot_photo,
                       '💢 拜托啦！请先点击下面加入我们的群组和频道，然后再 /start 一下好吗？',
                       judge_group_ikb)
        )
    elif await user_in_group_filter(call):
        await callAnswer(call, '⭕ 正在编辑', True)
