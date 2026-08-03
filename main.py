import logging
import os
import threading

import uvicorn

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
)

from config import (
    BOT_TOKEN,
    LOG_LEVEL,
    DEFAULT_CHANNELS,
)

from database import (
    init_db,
    add_channel,
)

from bot.handlers import (
    start,
    check_join,
)

from bot.commands import (
    addchannel,
    removechannel,
    pausechannel,
    resumechannel,
    channels,
    stats,
)

from news.scheduler import (
    scheduler,
    post_news,
)

from web import app as web_app


logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("AATG")


async def startup(application: Application):

    os.makedirs(
        "assets",
        exist_ok=True,
    )

    os.makedirs(
        "data",
        exist_ok=True,
    )

    os.makedirs(
        "webapp",
        exist_ok=True,
    )

    await init_db()

    for channel in DEFAULT_CHANNELS:

        await add_channel(channel)

    if not scheduler.running:

        scheduler.start()

    logger.info(
        "Scheduler jobs: %s",
        scheduler.get_jobs(),
    )

    logger.info(
        "Running first news check..."
    )

    try:

        await post_news()

    except Exception:

        logger.exception(
            "First news check failed."
        )

    logger.info(
        "Bot started successfully."
    )


async def shutdown(application: Application):

    if scheduler.running:

        scheduler.shutdown()

    logger.info(
        "Bot stopped."
    )


def run_web():

    uvicorn.run(
        web_app,
        host="0.0.0.0",
        port=int(
            os.getenv(
                "PORT",
                8000,
            )
        ),
        log_level="info",
    )


def main():

    threading.Thread(
        target=run_web,
        daemon=True,
    ).start()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(startup)
        .post_shutdown(shutdown)
        .build()
    )

    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            check_join,
            pattern="^verify_join$",
        )
    )

    application.add_handler(
        CommandHandler(
            "addchannel",
            addchannel,
        )
    )

    application.add_handler(
        CommandHandler(
            "removechannel",
            removechannel,
        )
    )

    application.add_handler(
        CommandHandler(
            "pausechannel",
            pausechannel,
        )
    )

    application.add_handler(
        CommandHandler(
            "resumechannel",
            resumechannel,
        )
    )

    application.add_handler(
        CommandHandler(
            "channels",
            channels,
        )
    )

    application.add_handler(
        CommandHandler(
            "stats",
            stats,
        )
    )

    application.run_polling(
        drop_pending_updates=True,
    )


if __name__ == "__main__":

    main()
