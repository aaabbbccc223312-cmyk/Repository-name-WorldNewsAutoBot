from telegram import Bot
import logging

from config import BOT_TOKEN, REQUIRED_CHANNELS

bot = Bot(BOT_TOKEN)

logger = logging.getLogger(__name__)

async def has_joined_all(user_id):

    logger.info(f"Required channels: {REQUIRED_CHANNELS}")

    for channel in REQUIRED_CHANNELS:

        try:

            member = await bot.get_chat_member(
                chat_id=channel,
                user_id=user_id,
            )

            logger.info(
                f"{channel} -> {member.status}"
            )

            if member.status in (
                "left",
                "kicked",
            ):
                return False

        except Exception as e:

            logger.exception(
                f"Failed checking {channel}: {e}"
            )

            return False

    return True
