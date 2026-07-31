from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from database import get_channels


async def join_keyboard():
    """
    Build a dynamic keyboard from all active channels
    stored in the database.
    """

    channels = await get_channels()

    keyboard = []

    for channel in channels:

        username = channel.lstrip("@")

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


def admin_keyboard():
    """
    Optional admin keyboard.
    """

    keyboard = [

        [
            InlineKeyboardButton(
                text="📊 Statistics",
                callback_data="admin_stats",
            )
        ],

        [
            InlineKeyboardButton(
                text="📢 Channels",
                callback_data="admin_channels",
            )
        ],

        [
            InlineKeyboardButton(
                text="📰 Latest News",
                callback_data="admin_news",
            )
        ],

    ]

    return InlineKeyboardMarkup(keyboard)
