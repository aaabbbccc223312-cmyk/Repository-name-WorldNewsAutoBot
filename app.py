import asyncio
import logging

from database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


async def main():

    logging.info("Starting AATG Super Bot...")

    await init_db()

    logging.info("Database initialized successfully.")

    # Telegram bot starts here
    # News scheduler starts here


if __name__ == "__main__":
    asyncio.run(main())
