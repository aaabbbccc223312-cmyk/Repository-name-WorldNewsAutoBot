from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import ADMIN_ID

from database import (
    add_channel,
    remove_channel,
    pause_channel,
    resume_channel,
    get_channels,
    total_users,
    total_channels,
    total_posts,
)


# ==========================================================
# ADMIN CHECK
# ==========================================================

def is_admin(update: Update) -> bool:
    return update.effective_user.id == ADMIN_ID


# ==========================================================
# /addchannel
# ==========================================================

async def addchannel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        return

    if len(context.args) != 1:

        await update.message.reply_text(
            "Usage:\n\n/addchannel @channelusername"
        )
        return

    channel = context.args[0].strip()

    if not channel.startswith("@"):

        await update.message.reply_text(
            "Channel username must start with @"
        )
        return

    await add_channel(channel)

    await update.message.reply_text(
        f"✅ Channel added successfully.\n\n{channel}"
    )


# ==========================================================
# /removechannel
# ==========================================================

async def removechannel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        return

    if len(context.args) != 1:

        await update.message.reply_text(
            "Usage:\n\n/removechannel @channelusername"
        )
        return

    channel = context.args[0].strip()

    await remove_channel(channel)

    await update.message.reply_text(
        f"🗑 Channel removed.\n\n{channel}"
    )


# ==========================================================
# /pausechannel
# ==========================================================

async def pausechannel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        return

    if len(context.args) != 1:

        await update.message.reply_text(
            "Usage:\n\n/pausechannel @channelusername"
        )
        return

    channel = context.args[0].strip()

    await pause_channel(channel)

    await update.message.reply_text(
        f"⏸ Channel paused.\n\n{channel}"
    )


# ==========================================================
# /resumechannel
# ==========================================================

async def resumechannel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        return

    if len(context.args) != 1:

        await update.message.reply_text(
            "Usage:\n\n/resumechannel @channelusername"
        )
        return

    channel = context.args[0].strip()

    await resume_channel(channel)

    await update.message.reply_text(
        f"▶️ Channel resumed.\n\n{channel}"
    )


# ==========================================================
# /channels
# ==========================================================

async def channels(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        return

    channel_list = await get_channels()

    if not channel_list:

        await update.message.reply_text(
            "No active channels found."
        )
        return

    text = "<b>📢 Active Channels</b>\n\n"

    for index, channel in enumerate(channel_list, start=1):

        text += f"{index}. {channel}\n"

    text += f"\nTotal: <b>{len(channel_list)}</b>"

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
    )


# ==========================================================
# /stats
# ==========================================================

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update):
        return

    users = await total_users()
    channels = await total_channels()
    posts = await total_posts()

    text = f"""
📊 <b>AATG BOT STATISTICS</b>

👥 Total Users: <b>{users}</b>

📢 Active Channels: <b>{channels}</b>

📰 Posted News: <b>{posts}</b>
"""

    await update.message.reply_text(
        text.strip(),
        parse_mode=ParseMode.HTML,
    )
