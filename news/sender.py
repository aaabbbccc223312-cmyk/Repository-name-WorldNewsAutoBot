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
        chat_id = channel["username"]

        while True:

            try:

                if image:

                    await self.bot.send_photo(
                        chat_id=chat_id,
                        photo=image,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                    )

                    logger.info(
                        "Photo sent -> %s",
                        chat_id,
                    )

                else:

                    await self.bot.send_message(
                        chat_id=chat_id,
                        text=caption,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=False,
                    )

                    logger.info(
                        "Message sent -> %s",
                        chat_id,
                    )

                # Small delay to reduce flood limits
                await asyncio.sleep(2)

                return

            except RetryAfter as e:

                wait = int(e.retry_after)

                logger.warning(
                    "Flood control for %s. Waiting %s seconds...",
                    chat_id,
                    wait,
                )

                await asyncio.sleep(wait + 1)

                continue

            except TelegramError as e:

                logger.error(
                    "Telegram error for %s: %s",
                    chat_id,
                    e,
                )

                # If photo failed, try text only
                if image:

                    try:

                        await self.bot.send_message(
                            chat_id=chat_id,
                            text=caption,
                            parse_mode=ParseMode.HTML,
                            disable_web_page_preview=False,
                        )

                        logger.info(
                            "Fallback message sent -> %s",
                            chat_id,
                        )

                        await asyncio.sleep(2)

                    except RetryAfter as ex:

                        wait = int(ex.retry_after)

                        logger.warning(
                            "Flood control during fallback for %s. Waiting %s seconds...",
                            chat_id,
                            wait,
                        )

                        await asyncio.sleep(wait + 1)

                        continue

                    except Exception:

                        logger.exception(
                            "Fallback message failed for %s",
                            chat_id,
                        )

                return

            except Exception:

                logger.exception(
                    "Unexpected sender error for %s",
                    chat_id,
                )

                return


sender = NewsSender()
