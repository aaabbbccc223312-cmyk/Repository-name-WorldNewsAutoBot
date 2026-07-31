import logging
import os

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
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

from news.scheduler import scheduler


# ==========================================================
# LOGGING
# ==========================================================

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("AATG")


# ==========================================================
# STARTUP
# ==========================================================

async def startup(app: Application):

    logger.info("=" * 60)
    logger.info("Starting AATG Super Bot")
    logger.info("=" * 60)

    # Create required folders
    os.makedirs("assets", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # Initialize database
    await init_db()

    logger.info("Database initialized")

    # Load default channels
    for channel in DEFAULT_CHANNELS:
        await add_channel(channel)

    logger.info("Default channels loaded")

    # Start automatic news scheduler
    scheduler.start()

    logger.info("News scheduler started")

    logger.info("Bot is ready")


# ==========================================================
# SHUTDOWN
# ==========================================================

async def shutdown(app: Application):

    logger.info("Stopping scheduler...")

    scheduler.shutdown()

    logger.info("Bot stopped.")


# ==========================================================
# MAIN
# ==========================================================

def main():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing in your .env file."
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(startup)
        .post_shutdown(shutdown)
        .build()
    )

    # ------------------------------------------------------
    # USER COMMANDS
    # ------------------------------------------------------

    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    # ------------------------------------------------------
    # ADMIN COMMANDS
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # CALLBACK BUTTONS
    # ------------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            check_join,
            pattern="^verify_join$",
        )
    )

    logger.info("Bot polling started...")

    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=[
            "message",
            "callback_query",
        ],
    )


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":
    main()
