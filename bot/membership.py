from telegram import Update, Bot
from telegram.error import TelegramError

from database import get_channels


async def get_missing_channels(
    update: Update,
    bot: Bot,
):
    """
    Returns a list of channels that the user
    has NOT joined.
    """

    user = update.effective_user

    if user is None:
        return []

    channels = await get_channels()

    missing = []

    for channel in channels:

        try:

            member = await bot.get_chat_member(
                chat_id=channel,
                user_id=user.id,
            )

            if member.status in (
                "left",
                "kicked",
            ):
                missing.append(channel)

        except TelegramError:

            # If Telegram can't verify membership,
            # treat the channel as missing.
            missing.append(channel)

        except Exception:

            missing.append(channel)

    return missing


async def has_joined_all(
    update: Update,
    bot: Bot,
):
    """
    Returns True if the user has joined every
    required channel.
    """

    missing = await get_missing_channels(
        update,
        bot,
    )

    return len(missing) == 0


async def get_joined_channels(
    update: Update,
    bot: Bot,
):
    """
    Returns a list of channels the user
    has successfully joined.
    """

    user = update.effective_user

    if user is None:
        return []

    channels = await get_channels()

    joined = []

    for channel in channels:

        try:

            member = await bot.get_chat_member(
                chat_id=channel,
                user_id=user.id,
            )

            if member.status not in (
                "left",
                "kicked",
            ):
                joined.append(channel)

        except Exception:
            pass

    return joined
