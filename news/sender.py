"""
news/sender.py

Professional Telegram Sender
"""

import asyncio
import logging

from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import RetryAfter, TelegramError

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

        while True:

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

                # Success
                return

            except RetryAfter as e:

                wait = int(e.retry_after)

                logger.warning(
                    "Flood control. Waiting %s seconds...",
                    wait,
                )

                await asyncio.sleep(wait + 1)

                continue

            except TelegramError as e:

                logger.error(
                    "Telegram error for %s: %s",
                    channel["username"],
                    e,
                )

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

                    except RetryAfter as ex:

                        wait = int(ex.retry_after)

                        logger.warning(
                            "Flood control on fallback. Waiting %s seconds...",
                            wait,
                        )

                        await asyncio.sleep(wait + 1)

                        continue

                    except Exception:

                        logger.exception(
                            "Fallback send failed."
                        )

                return

            except Exception:

                logger.exception(
                    "Unexpected sender error."
                )

                return


sender = NewsSender()
