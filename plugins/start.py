#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.

import html # <<< ADDED THIS IMPORT
from pyrogram import Client
from bot import Bot
from config import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import *

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data

    if data == "help":
        help_text_setting = await db.get_setting("help_text")
        text = help_text_setting['value'] if help_text_setting else HELP_TXT

        # <<< MODIFIED: Escaping user-provided data >>>
        await query.message.edit_text(
            text=text.format(first=html.escape(query.from_user.first_name)),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                 InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')]
            ])
        )

    elif data == "about":
        about_text_setting = await db.get_setting("about_text")
        text = about_text_setting['value'] if about_text_setting else ABOUT_TXT

        # <<< MODIFIED: Escaping user-provided data >>>
        await query.message.edit_text(
            text=text.format(first=html.escape(query.from_user.first_name)),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                 InlineKeyboardButton('ᴄʟᴏꜱᴇ', callback_data='close')]
            ])
        )

    elif data == "start":
        await query.message.delete()

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
        
        buttons.append(
            [InlineKeyboardButton("• ᴀʙᴏᴜᴛ", callback_data='about'),
             InlineKeyboardButton('ʜᴇʟᴘ •', callback_data='help')]
        )
        
        # <<< MODIFIED: Escaping user-provided data >>>
        await client.send_photo(
            chat_id=query.message.chat.id,
            photo=pic,
            caption=text.format(
                first=html.escape(query.from_user.first_name),
                last=html.escape(query.from_user.last_name or ''),
                username=f"@{query.from_user.username}" if query.from_user.username else "N/A",
                mention=query.from_user.mention,
                id=query.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )


    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
            
    elif data.startswith("rfs_ch_"):
        cid = int(data.split("_")[2])
        try:
            chat = await client.get_chat(cid)
            mode = await db.get_channel_mode(cid)
            status = "🟢 ᴏɴ" if mode == "on" else "🔴 ᴏғғ"
            new_mode = "ᴏғғ" if mode == "on" else "on"
            buttons = [
                [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
            ]
            await query.message.edit_text(
                f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception:
            await query.answer("Failed to fetch channel info", show_alert=True)

    elif data.startswith("rfs_toggle_"):
        cid, action = data.split("_")[2:]
        cid = int(cid)
        mode = "on" if action == "on" else "off"

        await db.set_channel_mode(cid, mode)
        await query.answer(f"Force-Sub set to {'ON' if mode == 'on' else 'OFF'}")

        chat = await client.get_chat(cid)
        status = "🟢 ON" if mode == "on" else "🔴 OFF"
        new_mode = "off" if mode == "on" else "on"
        buttons = [
            [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
        ]
        await query.message.edit_text(
            f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "fsub_back":
        channels = await db.show_channels()
        buttons = []
        for cid in channels:
            try:
                chat = await client.get_chat(cid)
                mode = await db.get_channel_mode(cid)
                status = "🟢" if mode == "on" else "🔴"
                buttons.append([InlineKeyboardButton(f"{status} {chat.title}", callback_data=f"rfs_ch_{cid}")])
            except:
                continue

        await query.message.edit_text(
            "sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ɪᴛs ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
