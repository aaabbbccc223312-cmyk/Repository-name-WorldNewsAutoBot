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

    # ======================================================
    # Send Text
    # ======================================================

    async def send_text(
        self,
        chat_id: str,
        text: str,
    ) -> bool:

        try:

            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False,
            )

            logger.info(f"Text sent -> {chat_id}")

            return True

        except RetryAfter as e:

            logger.warning(
                f"Flood control. Waiting {e.retry_after} seconds."
            )

            await asyncio.sleep(e.retry_after)

            return await self.send_text(
                chat_id,
                text,
            )

        except TimedOut:

            logger.warning("Telegram timeout.")

        except TelegramError as e:

            logger.error(e)

        except Exception:

            logger.exception("Unexpected error while sending text.")

        return False

    # ======================================================
    # Send Local Photo
    # ======================================================

    async def send_photo(
        self,
        chat_id: str,
        photo_path: str,
        caption: str = "",
    ) -> bool:

        try:

            with open(photo_path, "rb") as photo:

                await self.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                )

            logger.info(f"Photo sent -> {chat_id}")

            return True

        except RetryAfter as e:

            logger.warning(
                f"Flood control. Waiting {e.retry_after} seconds."
            )

            await asyncio.sleep(e.retry_after)

            return await self.send_photo(
                chat_id,
                photo_path,
                caption,
            )

        except Exception:

            logger.exception("Failed sending local photo.")

        return False

    # ======================================================
    # Send Image URL
    # ======================================================

    async def send_photo_url(
        self,
        chat_id: str,
        image_url: str,
        caption: str,
    ) -> bool:

        try:

            async with aiohttp.ClientSession() as session:

                async with session.get(image_url) as response:

                    if response.status != 200:

                        return await self.send_default_photo(
                            chat_id,
                            caption,
                        )

                    image = await response.read()

                    await self.bot.send_photo(
                        chat_id=chat_id,
                        photo=image,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                    )

            logger.info(f"Image sent -> {chat_id}")

            return True

        except Exception:

            logger.exception("Image URL failed.")

            return await self.send_default_photo(
                chat_id,
                caption,
            )

    # ======================================================
    # Default Image
    # ======================================================

    async def send_default_photo(
        self,
        chat_id: str,
        caption: str,
    ) -> bool:

        if os.path.isfile(DEFAULT_NEWS_IMAGE):

            return await self.send_photo(
                chat_id,
                DEFAULT_NEWS_IMAGE,
                caption,
            )

        return await self.send_text(
            chat_id,
            caption,
        )


telegram = TelegramSender()
