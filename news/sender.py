"""
news/sender.py

Professional Telegram Sender
"""

import logging

from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError

from config import BOT_TOKEN

logger = logging.getLogger(__name__)


class NewsSender:

    def __init__(self):

        self.bot = Bot(BOT_TOKEN)

    async def send(
        self,
        channel,
        article,
        caption,
    ):

        image = article.get("image")

        try:

            if image:

                await self.bot.send_photo(
                    chat_id=channel["username"],
                    photo=image,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                )

                logger.info(
                    "Photo sent -> %s",
                    channel["username"],
                )

            else:

                await self.bot.send_message(
                    chat_id=channel["username"],
                    text=caption,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=False,
                )

                logger.info(
                    "Message sent -> %s",
                    channel["username"],
                )

        except TelegramError as e:

            logger.error(
                "Telegram error for %s: %s",
                channel["username"],
                e,
            )

            # If sending a photo fails,
            # try sending the text version.

            if image:

                try:

                    await self.bot.send_message(
                        chat_id=channel["username"],
                        text=caption,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=False,
                    )

                    logger.info(
                        "Fallback message sent -> %s",
                        channel["username"],
                    )

                except Exception as ex:

                    logger.exception(ex)

        except Exception as e:

            logger.exception(e)


sender = NewsSender()
