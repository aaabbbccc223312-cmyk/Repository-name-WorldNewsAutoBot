from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from database import get_channels


async def join_keyboard():
    """
    Dynamically builds the join keyboard from the database.
    Every active channel automatically appears.
    """

    keyboard = []

    channels = await get_channels()

    for channel in channels:

        keyboard.append([
            InlineKeyboardButton(
                text=f"📢 {channel}",
                url=f"https://t.me/{channel.replace('@','')}",
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            text="✅ I've Joined",
            callback_data="verify_join",
        )
    ])

    return InlineKeyboardMarkup(keyboard)
