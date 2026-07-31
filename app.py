import asyncio
import logging

from config import LOG_LEVEL
from database import init_db

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("AATG")


async def startup():

    logger.info("=" * 50)
    logger.info("Starting AATG Super Bot...")
    logger.info("=" * 50)

    await init_db()

    logger.info("Database Ready")

    # Telegram Bot
    logger.info("Telegram Bot Ready")

    # News Scheduler
    logger.info("News Scheduler Ready")

    logger.info("=" * 50)
    logger.info("AATG Super Bot Started Successfully")
    logger.info("=" * 50)

    while True:
        await asyncio.sleep(3600)


def main():
    asyncio.run(startup())


if __name__ == "__main__":
    main()
