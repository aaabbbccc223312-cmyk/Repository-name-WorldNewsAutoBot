from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import CHANNELS


def join_keyboard():
    keyboard = []

    for i, channel in enumerate(CHANNELS, start=1):
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"📢 Join Channel {i}",
                    url=f"https://t.me/{channel.replace('@', '')}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="✅ I've Joined",
                callback_data="check_join",
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)
