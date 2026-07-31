from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from database import get_channels


async def join_keyboard():
    """
    Build the Force Join keyboard dynamically from the database.
    """

    keyboard = []

    channels = await get_channels()

    for channel in channels:
        username = channel.replace("@", "")

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"📢 {channel}",
                    url=f"https://t.me/{username}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="✅ I've Joined",
                callback_data="verify_join",
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)
