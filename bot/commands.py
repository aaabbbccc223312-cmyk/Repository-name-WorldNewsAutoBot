from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_ID
from database import (
    add_channel,
    remove_channel,
    get_channels,
    pause_channel,
    resume_channel,
)


def is_admin(user_id: int) -> bool:
    return int(user_id) == int(ADMIN_ID)


async def addchannel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/addchannel @channelusername"
        )
        return

    username = context.args[0]

    if not username.startswith("@"):
        username = "@" + username

    await add_channel(username)

    await update.message.reply_text(
        f"✅ Channel added successfully.\n\n{username}"
    )


async def removechannel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/removechannel @channelusername"
        )
        return

    username = context.args[0]

    if not username.startswith("@"):
        username = "@" + username

    await remove_channel(username)

    await update.message.reply_text(
        f"🗑 Channel removed.\n\n{username}"
    )


async def pausechannel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/pausechannel @channelusername"
        )
        return

    username = context.args[0]

    if not username.startswith("@"):
        username = "@" + username

    await pause_channel(username)

    await update.message.reply_text(
        f"⏸ Channel paused.\n\n{username}"
    )


async def resumechannel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/resumechannel @channelusername"
        )
        return

    username = context.args[0]

    if not username.startswith("@"):
        username = "@" + username

    await resume_channel(username)

    await update.message.reply_text(
        f"▶️ Channel resumed.\n\n{username}"
    )


async def channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    channel_list = await get_channels()

    if not channel_list:
        await update.message.reply_text(
            "No active channels found."
        )
        return

    text = "📢 Active Channels\n\n"

    for i, channel in enumerate(channel_list, start=1):
        text += f"{i}. {channel}\n"

    await update.message.reply_text(text)


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    channels = await get_channels()

    await update.message.reply_text(
        f"""
📊 Bot Statistics

👥 Active Channels: {len(channels)}

🚀 Status: Running

✅ Version: V3
"""
    )
