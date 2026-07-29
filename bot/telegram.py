"""
bot/telegram.py

Handles sending messages to Telegram channels.
"""

import asyncio
import logging
from typing import Iterable

from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError, RetryAfter, TimedOut

from config import BOT_TOKEN, CHANNELS

logger = logging.getLogger(__name__)


class TelegramSender:
    def __init__(self):
        self.bot = Bot(token=BOT_TOKEN)

    async def send_message(
        self,
        chat_id: str,
        text: str,
        disable_web_preview: bool = False
    ) -> bool:
        """
        Send one message to one Telegram channel.
        """

        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=disable_web_preview,
            )

            logger.info(f"✓ Sent message to {chat_id}")
            return True

        except RetryAfter as e:
            logger.warning(
                f"Rate limited by Telegram. Retrying in {e.retry_after} seconds..."
            )
            await asyncio.sleep(e.retry_after)

            return await self.send_message(
                chat_id,
                text,
                disable_web_preview,
            )

        except TimedOut:
            logger.warning(f"Timeout sending to {chat_id}")

        except TelegramError as e:
            logger.error(f"Telegram error for {chat_id}: {e}")

        except Exception as e:
            logger.exception(e)

        return False

    async def broadcast(
        self,
        text: str,
        channels: Iterable[str] | None = None,
        disable_web_preview: bool = False,
    ) -> dict:
        """
        Send the same message to all configured channels.

        Returns:
            {
                "@paisabase1": True,
                "@aatgpay": True,
                "@smrtwallet": False
            }
        """

        if channels is None:
            channels = CHANNELS

        results = {}

        for channel in channels:
            success = await self.send_message(
                chat_id=channel,
                text=text,
                disable_web_preview=disable_web_preview,
            )

            results[channel] = success

        return results

    async def close(self):
        """
        Close the HTTP session cleanly.
        """

        await self.bot.session.close()


telegram_sender = TelegramSender()
