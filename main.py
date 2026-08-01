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
