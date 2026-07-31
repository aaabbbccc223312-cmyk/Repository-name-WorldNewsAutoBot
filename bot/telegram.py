"""
bot/telegram.py

Professional Telegram Sender

Features
--------
✅ Send text
✅ Send photos from URL
✅ Send local photos
✅ Auto fallback image
✅ HTML formatting
✅ Retry on FloodWait
✅ Dynamic channels
"""

import asyncio
import logging
import os

import aiohttp

from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import RetryAfter, TimedOut, TelegramError

from config import (
    BOT_TOKEN,
    DEFAULT_NEWS_IMAGE,
)

logger = logging.getLogger(__name__)


class TelegramSender:

    def __init__(self):
        self.bot = Bot(BOT_TOKEN)

    # --------------------------------------------------
    # TEXT
    # --------------------------------------------------

    async def send_text(self, channel: str, text: str):

        try:

            await self.bot.send_message(
                chat_id=channel,
                text=text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False,
            )

            logger.info(f"Sent text -> {channel}")
            return True

        except RetryAfter as e:

            await asyncio.sleep(e.retry_after)
            return await self.send_text(channel, text)

        except TimedOut:

            logger.warning("Telegram Timeout")

        except TelegramError as e:

            logger.error(e)

        except Exception as e:

            logger.exception(e)

        return False

    # --------------------------------------------------
    # LOCAL PHOTO
    # --------------------------------------------------

    async def send_photo(self, channel: str, photo_path: str, caption: str):

        try:

            with open(photo_path, "rb") as photo:

                await self.bot.send_photo(
                    chat_id=channel,
                    photo=photo,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                )

            logger.info(f"Sent photo -> {channel}")
            return True

        except RetryAfter as e:

            await asyncio.sleep(e.retry_after)
            return await self.send_photo(channel, photo_path, caption)

        except Exception as e:

            logger.exception(e)

        return False

    # --------------------------------------------------
    # PHOTO FROM URL
    # --------------------------------------------------

    async def send_photo_url(
        self,
        channel: str,
        image_url: str,
        caption: str,
    ):

        try:

            async with aiohttp.ClientSession() as session:

                async with session.get(image_url) as response:

                    if response.status != 200:
                        return await self.send_default_photo(
                            channel,
                            caption,
                        )

                    image = await response.read()

                    await self.bot.send_photo(
                        chat_id=channel,
                        photo=image,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                    )

            logger.info(f"Image sent -> {channel}")

            return True

        except Exception as e:

            logger.warning(e)

            return await self.send_default_photo(
                channel,
                caption,
            )

    # --------------------------------------------------
    # DEFAULT IMAGE
    # --------------------------------------------------

    async def send_default_photo(
        self,
        channel,
        caption,
    ):

        if os.path.exists(DEFAULT_NEWS_IMAGE):

            return await self.send_photo(
                channel,
                DEFAULT_NEWS_IMAGE,
                caption,
            )

        return await self.send_text(
            channel,
            caption,
        )


telegram = TelegramSender()
