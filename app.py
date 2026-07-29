import asyncio
import logging

from database import init_db
from bot.telegram import telegram
from source_manager import check_all_sources


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


async def main():

    logging.info("Starting GlobalPulseBot...")

    await init_db()

    while True:

        try:

            articles = await check_all_sources()

            for article in articles:

                message = f"""
🌍 <b>GLOBAL PULSE</b>

🚨 <b>{article['category']}</b>

📰 <b>{article['title']}</b>

📝 {article['summary']}

📍 <b>Source:</b> {article['source']}

🔗 {article['url']}
"""

                await telegram.broadcast_text(message)

        except Exception as e:
            logging.exception(e)

        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
