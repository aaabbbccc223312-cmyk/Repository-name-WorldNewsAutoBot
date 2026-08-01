"""
news/sender.py

Sends news to Telegram channels.
"""

from telegram import Bot

from telegram.constants import ParseMode

from config import BOT_TOKEN


class NewsSender:

    def __init__(

        self,

    ):

        self.bot = Bot(

            BOT_TOKEN

        )


    async def send(

        self,

        channel,

        article,

        caption,

    ):

        image = article.get(

            "image",

        )
        if image:

            await self.bot.send_photo(

                chat_id=channel["username"],

                photo=image,

                caption=caption,

                parse_mode=ParseMode.HTML,

            )

        else:

            await self.bot.send_message(

                chat_id=channel["username"],

                text=caption,

                parse_mode=ParseMode.HTML,

                disable_web_page_preview=False,

            )


sender = NewsSender()
