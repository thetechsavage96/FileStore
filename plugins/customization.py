# Gemini AI @Google

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
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


# --- List All Commands ---

# <<< CHANGED from "command" to "commands" >>>
@Bot.on_message(filters.command("commands") & filters.private & admin)
async def command_list(client: Bot, message: Message):
    # Text for the command list
    command_text = """
<b>Here is the full list of available commands:</b>

<blockquote><b>🤖 General Bot Commands</b></blockquote>

<code>/start</code> - Starts the bot.
<code>/batch</code> - Creates a link for a range of messages.
<code>/genlink</code> - Creates a link for a single message.
<code>/custom_batch</code> - Creates a batch link from multiple forwarded messages.
<code>/dlt_time</code> - Sets auto-delete time for files sent by the bot.
<code>/check_dlt_time</code> - Checks the current auto-delete time.
<code>/stats</code> - Shows bot uptime and stats.
<code>/users</code> - Shows the total number of users.

<blockquote><b>⚙️ Customization Commands (Admin Only)</b></blockquote>

<i>(Reply to a message/photo to use these)</i>
<code>/set_start_text</code> - Sets the welcome message.
<code>/set_about_text</code> - Sets the 'About' page text.
<code>/set_help_text</code> - Sets the 'Help' page text.
<code>/set_start_pic</code> - Sets the welcome picture.

<i>(Use with arguments)</i>
<code>/set_channel_button [URL] [Text]</code> - Sets the main URL button on the start message.
<code>/commands</code> - Displays this command list.

<blockquote><b>🛡️ Admin & User Management</b></blockquote>

<code>/add_admin</code> & <code>/deladmin</code> - Add or remove a bot admin.
<code>/admins</code> - View the list of bot admins.
<code>/ban</code> & <code>/unban</code> - Ban or unban a user from the bot.
<code>/banlist</code> - View all banned users.

<blockquote><b>📣 Channel Management</b></blockquote>

<code>/addchnl</code> & <code>/delchnl</code> - Add or remove a Force Subscribe channel.
<code>/listchnl</code> - View all Force Subscribe channels.
<code>/fsub_mode</code> - Toggle request-to-join mode for a channel.
"""

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("❌ Close", callback_data="close")]]
    )

    await message.reply(
        text=command_text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )
