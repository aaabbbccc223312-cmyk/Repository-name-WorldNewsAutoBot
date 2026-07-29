"""
bot/telegram.py

Professional Telegram sender.

Supports:
- Text messages
- Photo messages
- Multiple channels
- Automatic retry
"""

import asyncio
import logging
from pathlib import Path
from typing import Iterable

from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import RetryAfter, TimedOut, TelegramError

from config import BOT_TOKEN, CHANNELS

logger = logging.getLogger(__name__)


class TelegramSender:

    def __init__(self):
        self.bot = Bot(BOT_TOKEN)

    async def send_text(
        self,
        chat_id: str,
        text: str,
        disable_preview: bool = True,
    ) -> bool:

        try:

            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=disable_preview,
            )

            logger.info(f"Text sent -> {chat_id}")
            return True

        except RetryAfter as e:

            logger.warning(f"Retry after {e.retry_after}s")
            await asyncio.sleep(e.retry_after)

            return await self.send_text(
                chat_id,
                text,
                disable_preview,
            )

        except TimedOut:

            logger.warning("Telegram timeout.")

        except TelegramError as e:

            logger.error(e)

        except Exception as e:

            logger.exception(e)

        return False

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

            await asyncio.sleep(e.retry_after)

            return await self.send_photo(
                chat_id,
                photo_path,
                caption,
            )

        except Exception as e:

            logger.exception(e)

        return False

    async def broadcast_text(
        self,
        text: str,
        channels: Iterable[str] = CHANNELS,
    ):

        results = {}

        for channel in channels:

            results[channel] = await self.send_text(
                channel,
                text,
            )

        return results

    async def broadcast_photo(
        self,
        photo_path: str,
        caption: str,
        channels: Iterable[str] = CHANNELS,
    ):

        if not Path(photo_path).exists():
            raise FileNotFoundError(photo_path)

        results = {}

        for channel in channels:

            results[channel] = await self.send_photo(
                channel,
                photo_path,
                caption,
            )

        return results


telegram = TelegramSender()
