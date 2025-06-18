# Gemini AI @Google

from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
from database.database import db
from helper_func import admin

# --- Text Settings ---

@Bot.on_message(filters.command("set_start_text") & filters.private & admin)
async def set_start_text(client: Bot, message: Message):
    if not message.reply_to_message or not message.reply_to_message.text:
        return await message.reply("<b>Usage:</b> Reply to a message with the text you want to set as the new start message.")
    
    # Using text.html to preserve formatting
    new_text = message.reply_to_message.text.html
    await db.update_setting("start_text", new_text)
    await message.reply("✅ Start text updated successfully!")


@Bot.on_message(filters.command("set_about_text") & filters.private & admin)
async def set_about_text(client: Bot, message: Message):
    if not message.reply_to_message or not message.reply_to_message.text:
        return await message.reply("<b>Usage:</b> Reply to a message with the text you want to set as the new about message.")
    
    new_text = message.reply_to_message.text.html
    await db.update_setting("about_text", new_text)
    await message.reply("✅ About text updated successfully!")


@Bot.on_message(filters.command("set_help_text") & filters.private & admin)
async def set_help_text(client: Bot, message: Message):
    if not message.reply_to_message or not message.reply_to_message.text:
        return await message.reply("<b>Usage:</b> Reply to a message with the text you want to set as the new help message.")
    
    new_text = message.reply_to_message.text.html
    await db.update_setting("help_text", new_text)
    await message.reply("✅ Help text updated successfully!")


# --- Picture Setting ---

@Bot.on_message(filters.command("set_start_pic") & filters.private & admin)
async def set_start_pic(client: Bot, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply("<b>Usage:</b> Reply to a photo to set it as the new start picture.")
    
    # Saving the file_id of the photo
    pic_id = message.reply_to_message.photo.file_id
    await db.update_setting("start_pic", pic_id)
    await message.reply("✅ Start picture updated successfully!")


# --- Button Setting ---

@Bot.on_message(filters.command("set_channel_button") & filters.private & admin)
async def set_channel_button(client: Bot, message: Message):
    try:
        # Command format: /set_channel_button <URL> <Button Text>
        _, url, *text_parts = message.command
        button_text = " ".join(text_parts)

        if not button_text:
            raise ValueError

        button_data = {"text": button_text, "url": url}
        await db.update_setting("channel_button", button_data)
        await message.reply(f"✅ Channel button updated successfully!\n\n**Text:** {button_text}\n**URL:** {url}")

    except ValueError:
        await message.reply(
            "<b>Usage:</b> <code>/set_channel_button [URL] [Button Text]</code>\n\n"
            "<b>Example:</b> <code>/set_channel_button https://t.me/TheTechSavageTelegram Visit My Channel</code>"
        )
