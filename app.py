import asyncio
import logging

from config import LOG_LEVEL
from database import (
    init_db,
    add_channel,
)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("AATG")


# Default channels (only added if missing)
DEFAULT_CHANNELS = [
    "@paisabase1",
    "@aatgpay",
    "@smrtwallet",
]


async def startup():

    logger.info("=" * 60)
    logger.info("🚀 Starting AATG Super Bot V3")
    logger.info("=" * 60)

    # Create database
    await init_db()
    logger.info("✅ Database initialized")

    # Add default channels once
    for channel in DEFAULT_CHANNELS:
        await add_channel(channel)

    logger.info("✅ Default channels loaded")

    logger.info("✅ Telegram Bot Ready")
    logger.info("✅ News Engine Ready")
    logger.info("✅ Scheduler Ready")

    logger.info("=" * 60)
    logger.info("🎉 AATG Super Bot Started Successfully")
    logger.info("=" * 60)

    # Keep Railway process alive
    while True:
        await asyncio.sleep(3600)


def main():
    asyncio.run(startup())


if __name__ == "__main__":
    main()
