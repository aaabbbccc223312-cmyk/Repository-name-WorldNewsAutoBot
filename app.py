import logging
import os

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
)

from config import (
    BOT_TOKEN,
    DEFAULT_CHANNELS,
    LOG_LEVEL,
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


# =====================================
# Logging
# =====================================

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("AATG")


# =====================================
# Startup
# =====================================

async def startup(app: Application):

    logger.info("=" * 60)
    logger.info("🚀 Starting AATG Super Bot V4")
    logger.info("=" * 60)

    # Create folders
    os.makedirs("data", exist_ok=True)
    os.makedirs("assets", exist_ok=True)

    # Initialize database
    await init_db()

    logger.info("✅ Database initialized")

    # Add default channels only once
    for channel in DEFAULT_CHANNELS:
        await add_channel(channel)

    logger.info("✅ Default channels loaded")

    # Start automatic news scheduler
    scheduler.start()

    logger.info("✅ News Scheduler Started")
    logger.info("✅ Telegram Ready")
    logger.info("🎉 Bot Started Successfully")


# =====================================
# Shutdown
# =====================================

async def shutdown(app: Application):

    logger.info("Stopping Scheduler...")

    scheduler.shutdown()

    logger.info("Bot Stopped")


# =====================================
# Main
# =====================================

def main():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing. Please set it in your .env file."
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(startup)
        .post_shutdown(shutdown)
        .build()
    )

    # ===============================
    # User Commands
    # ===============================

    application.add_handler(
        CommandHandler("start", start)
    )

    # ===============================
    # Admin Commands
    # ===============================

    application.add_handler(
        CommandHandler("addchannel", addchannel)
    )

    application.add_handler(
        CommandHandler("removechannel", removechannel)
    )

    application.add_handler(
        CommandHandler("pausechannel", pausechannel)
    )

    application.add_handler(
        CommandHandler("resumechannel", resumechannel)
    )

    application.add_handler(
        CommandHandler("channels", channels)
    )

    application.add_handler(
        CommandHandler("stats", stats)
    )

    # ===============================
    # Callback Buttons
    # ===============================

    application.add_handler(
        CallbackQueryHandler(
            check_join,
            pattern="^verify_join$",
        )
    )

    logger.info("🤖 Bot Polling Started...")

    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=["message", "callback_query"],
    )


# =====================================
# Run
# =====================================

if __name__ == "__main__":
    main()
