from telegram import (

    InlineKeyboardButton,

    InlineKeyboardMarkup,

)

from config import REQUIRED_CHANNELS


def join_keyboard():

    keyboard = []

    for channel in REQUIRED_CHANNELS:

        username = channel.replace(

            "@",

            "",

        )

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

                text="✅ I HAVE JOINED",

                callback_data="verify_join",

            )

        ]

    )

    return InlineKeyboardMarkup(

        keyboard

    )
