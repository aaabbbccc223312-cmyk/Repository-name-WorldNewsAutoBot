import logging
import os

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

from news.scheduler import scheduler


logging.basicConfig(

    level=getattr(

        logging,

        LOG_LEVEL,

    ),

    format="%(asctime)s | %(levelname)s | %(message)s",

)

logger = logging.getLogger(

    "AATG"

)


async def startup(

    app: Application,

):

    os.makedirs(

        "assets",

        exist_ok=True,

    )

    os.makedirs(

        "data",

        exist_ok=True,

    )

    await init_db()

    for channel in DEFAULT_CHANNELS:

        await add_channel(

            channel

        )

    if not scheduler.running:

        scheduler.start()

    logger.info(

        "Bot started successfully."

    )


async def shutdown(

    app: Application,

):

    scheduler.shutdown()

    logger.info(

        "Bot stopped."

    )


def main():

    application = (

        Application.builder()

        .token(

            BOT_TOKEN

        )

        .post_init(

            startup

        )

        .post_shutdown(

            shutdown

        )

        .build()

    )

    application.add_handler(

        CommandHandler(

            "start",

            start,

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

    application.add_handler(

        CallbackQueryHandler(

            check_join,

            pattern="^verify_join$",

        )

    )

    application.run_polling(

        drop_pending_updates=True,

    )


if __name__ == "__main__":

    main()
