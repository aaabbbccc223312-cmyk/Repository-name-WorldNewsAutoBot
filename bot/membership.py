from telegram import Update
from telegram import Bot
from telegram.error import TelegramError

from database import get_channels


async def get_missing_channels(
    update: Update,
    bot: Bot,
):
    """
    Returns a list of channels the user
    has NOT joined.
    """

    user_id = update.effective_user.id

    channels = await get_channels()

    missing = []

    for channel in channels:

        try:

            member = await bot.get_chat_member(
                chat_id=channel,
                user_id=user_id,
            )

            if member.status in (
                "left",
                "kicked",
            ):
                missing.append(channel)

        except TelegramError:
            # If the bot can't check membership,
            # treat it as missing.
            missing.append(channel)

    return missing


async def has_joined_all(
    update: Update,
    bot: Bot,
):
    """
    Returns True if the user has joined
    every required channel.
    """

    missing = await get_missing_channels(
        update,
        bot,
    )

    return len(missing) == 0
