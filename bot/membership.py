"""
bot/membership.py

Checks whether a user has joined all required channels.
"""

from telegram import Bot

from config import (

    BOT_TOKEN,

    REQUIRED_CHANNELS,

)


bot = Bot(

    BOT_TOKEN

)


async def has_joined_all(

    user_id,

):

    for channel in REQUIRED_CHANNELS:

        try:

            member = await bot.get_chat_member(

                chat_id=channel,

                user_id=user_id,

            )
            if member.status in (

                "left",

                "kicked",

            ):

                return False

        except Exception:

            return False

    return True
