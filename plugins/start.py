# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import html
import traceback # <<< ADDED FOR DEBUGGING
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *
from datetime import datetime, timedelta

# Cache for chat info to reduce DB calls
chat_data_cache = {}

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id

    if await db.ban_user_exist(user_id):
        return await message.reply_text(
            "<b>⛔️ You are Banned from using this bot.</b>\n\n"
            "<i>Contact support if you think this is a mistake.</i>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Contact Support", url=BAN_SUPPORT)]])
        )

    if not await is_subscribed(client, user_id):
        return await not_joined(client, message)

    if not await db.present_user(user_id):
        try:
            await db.add_user(user_id)
        except:
            pass

    text = message.text
    if len(text) > 7:
        # This part handles file sending logic, it remains the same
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return

        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start, end+1)
            else:
                ids = range(start, end-1, -1)
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        
        temp_msg = await message.reply("<b>Please wait...</b>")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        FILE_AUTO_DELETE = await db.get_del_timer()
        for msg in messages:
            sent_msg = []
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(file_name=msg.document.file_name, file_size=get_size(msg.document.file_size), caption=msg.caption)
            elif bool(CUSTOM_CAPTION) & bool(msg.video):
                caption = CUSTOM_CAPTION.format(file_name=msg.video.file_name, file_size=get_size(msg.video.file_size), caption=msg.caption)
            else:
                caption = msg.caption
            
            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                sent_msg.append(snt_msg)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                sent_msg.append(snt_msg)
            except:
                pass
        
        if FILE_AUTO_DELETE > 0:
            await asyncio.sleep(FILE_AUTO_DELETE)
            for snt_msg in sent_msg:
                try:
                    await snt_msg.delete()
                except:
                    pass
        return
    
    else:
        # <<< --- DEBUGGING BLOCK ADDED --- >>>
        try:
            start_pic_setting = await db.get_setting("start_pic")
            start_text_setting = await db.get_setting("start_text")
            channel_button_setting = await db.get_setting("channel_button")

            pic = start_pic_setting['value'] if start_pic_setting else START_PIC
            text = start_text_setting['value'] if start_text_setting else START_MSG

            buttons = []
            if channel_button_setting:
                btn_text = channel_button_setting['value']['text']
                btn_url = channel_button_setting['value']['url']
                buttons.append([InlineKeyboardButton(btn_text, url=btn_url)])
            else:
                buttons.append([InlineKeyboardButton("• THETECHSAVAGE CHANNELS •", url="https://t.me/TheTechSavageTelegram")])

            buttons.append([
                InlineKeyboardButton("• ᴀʙᴏᴜᴛ", callback_data="about"),
                InlineKeyboardButton('ʜᴇʟᴘ •', callback_data="help")
            ])
            
            reply_markup = InlineKeyboardMarkup(buttons)

            await message.reply_photo(
                photo=pic,
                caption=text.format(
                    first=html.escape(message.from_user.first_name),
                    last=html.escape(message.from_user.last_name or ''),
                    username=f"@{message.from_user.username}" if message.from_user.username else "N/A",
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                message_effect_id=5104841245755180586
            )
        except Exception as e:
            # This will print the exact error to your server's log
            print("--- ERROR IN /start HANDLER ---")
            traceback.print_exc()
            print("-----------------------------")
            await message.reply("Sorry, a critical error occurred while generating the start message. Please check the logs for details.")
        return

async def not_joined(client: Client, message: Message):
    force_pic_setting = await db.get_setting("force_pic")
    force_text_setting = await db.get_setting("force_text")

    pic = force_pic_setting['value'] if force_pic_setting else FORCE_PIC
    text = force_text_setting['value'] if force_text_setting else FORCE_MSG

    buttons = []
    try:
        for c_id in (await db.show_channels()):
            chat = await client.get_chat(c_id)
            if chat.invite_link:
                link = chat.invite_link
            else:
                link = await client.export_chat_invite_link(c_id)
            buttons.append([InlineKeyboardButton(f"🔺 Jᴏɪɴ {chat.title} 🔺", url=link)])
    except Exception as e:
        print(e)

    try:
        await message.reply_photo(
            photo=pic,
            caption=text.format(
                first=html.escape(message.from_user.first_name),
                last=html.escape(message.from_user.last_name or ''),
                username=f"@{message.from_user.username}" if message.from_user.username else "N/A",
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except:
        await message.reply(
            text=text.format(
                first=html.escape(message.from_user.first_name),
                last=html.escape(message.from_user.last_name or ''),
                username=f"@{message.from_user.username}" if message.from_user.username else "N/A",
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview = True
        )

@Bot.on_message(filters.command('commands') & filters.private & admin)
async def bcmd(bot: Bot, message: Message):
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data = "close")]])
    await message.reply(text=CMD_TXT, reply_markup = reply_markup, quote= True)
