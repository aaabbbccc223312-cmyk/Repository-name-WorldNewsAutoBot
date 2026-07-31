import os

from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# BOT
# ==========================================================

BOT_TOKEN = os.getenv(
    "BOT_TOKEN",
    "",
)

ADMIN_ID = int(
    os.getenv(
        "ADMIN_ID",
        "0",
    )
)

# ==========================================================
# DATABASE
# ==========================================================

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/database.db",
)

# ==========================================================
# LOGGING
# ==========================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
).upper()

# ==========================================================
# REQUIRED CHANNELS
# ==========================================================

REQUIRED_CHANNELS = [

    os.getenv(
        "REQUIRED_CHANNEL_1",
        "",
    ),

    os.getenv(
        "REQUIRED_CHANNEL_2",
        "",
    ),

    os.getenv(
        "REQUIRED_CHANNEL_3",
        "",
    ),

]

REQUIRED_CHANNELS = [

    channel

    for channel in REQUIRED_CHANNELS

    if channel.strip()

]

# ==========================================================
# DEFAULT CHANNELS
# ==========================================================

DEFAULT_CHANNELS = [

    os.getenv(
        "DEFAULT_CHANNEL_1",
        "",
    ),

    os.getenv(
        "DEFAULT_CHANNEL_2",
        "",
    ),

    os.getenv(
        "DEFAULT_CHANNEL_3",
        "",
    ),

]

DEFAULT_CHANNELS = [

    channel

    for channel in DEFAULT_CHANNELS

    if channel.strip()

]

NEWS_CHECK_INTERVAL = int(
    os.getenv(
        "NEWS_CHECK_INTERVAL",
        "300",
    )
)

MAX_ARTICLES_PER_FEED = int(
    os.getenv(
        "MAX_ARTICLES_PER_FEED",
        "10",
    )
)

MAX_POSTS_PER_CYCLE = int(
    os.getenv(
        "MAX_POSTS_PER_CYCLE",
        "20",
    )
)

ASSETS_FOLDER = "assets"

DATA_FOLDER = "data"

WELCOME_IMAGE = os.path.join(
    ASSETS_FOLDER,
    "welcome.jpg",
)

os.makedirs(
    ASSETS_FOLDER,
    exist_ok=True,
)

os.makedirs(
    DATA_FOLDER,
    exist_ok=True,
)

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is missing in your .env file."
    )

if ADMIN_ID <= 0:
    raise RuntimeError(
        "ADMIN_ID is missing in your .env file."
    )

__all__ = [

    "BOT_TOKEN",

    "ADMIN_ID",

    "DATABASE_PATH",

    "LOG_LEVEL",

    "REQUIRED_CHANNELS",

    "DEFAULT_CHANNELS",

    "NEWS_CHECK_INTERVAL",

    "MAX_ARTICLES_PER_FEED",

    "MAX_POSTS_PER_CYCLE",

    "ASSETS_FOLDER",

    "DATA_FOLDER",

    "WELCOME_IMAGE",

]
