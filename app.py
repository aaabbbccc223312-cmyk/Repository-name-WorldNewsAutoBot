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

# ===========================
# Logging
# ===========================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=getattr(logging, LOG_LEVEL),
)

logger = logging.getLogger(__name__)


# ===========================
# Startup
# ===========================

async def on_startup(app: Application):

    logger.info("Initializing database...")

    os.makedirs("data", exist_ok=True)
    os.makedirs("assets", exist_ok=True)

    await init_db()

    for channel in DEFAULT_CHANNELS:
        await add_channel(channel)

    logger.info("Database Ready")
    logger.info("Default Channels Loaded")
    logger.info("Bot Started Successfully")


# ===========================
# Main
# ===========================

def main():

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # User Commands
    application.add_handler(
        CommandHandler("start", start)
    )

    # Admin Commands
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

    # Verify Join Button
    application.add_handler(
        CallbackQueryHandler(
            check_join,
            pattern="^verify_join$",
        )
    )

    application.post_init = on_startup

    logger.info("Polling Started...")

    application.run_polling(
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
