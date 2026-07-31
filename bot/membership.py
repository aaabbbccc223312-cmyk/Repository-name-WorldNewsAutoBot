from telegram import Update
from telegram import Bot

from database import get_channels


async def get_missing_channels(update: Update, bot: Bot):
    """
    Returns a list of channels the user has not joined.
    """

    user_id = update.effective_user.id
    missing_channels = []

    channels = await get_channels()

    for channel in channels:
        try:
            member = await bot.get_chat_member(channel, user_id)

            if member.status in ("left", "kicked"):
                missing_channels.append(channel)

        except Exception:
            # If the bot can't check a channel, treat it as missing.
            # Make sure:
            # 1. The bot is an admin in the channel.
            # 2. The channel username is correct.
            missing_channels.append(channel)

    return missing_channels


async def has_joined_all(update: Update, bot: Bot):
    """
    Returns True if the user has joined every required channel.
    """

    missing = await get_missing_channels(update, bot)
    return len(missing) == 0
