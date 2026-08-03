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
# LOAD CHANNELS
# ==========================================================

def load_channels(
    prefix: str,
    maximum: int = 20,
):

    channels = []

    for index in range(
        1,
        maximum + 1,
    ):

        value = os.getenv(
            f"{prefix}_{index}",
            "",
        ).strip()

        if value:

            channels.append(
                value
            )

    return channels


REQUIRED_CHANNELS = load_channels(
    "REQUIRED_CHANNEL"
)

DEFAULT_CHANNELS = load_channels(
    "DEFAULT_CHANNEL"
)

# ==========================================================
# NEWS
# ==========================================================

NEWS_CHECK_INTERVAL = int(
    os.getenv(
        "NEWS_CHECK_INTERVAL",
        "30",
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

# ==========================================================
# MINI APP
# ==========================================================

WEBAPP_URL = os.getenv(
    "WEBAPP_URL",
    "",
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "CHANGE_THIS_SECRET_KEY",
)

# ==========================================================
# FOLDERS
# ==========================================================

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

# ==========================================================
# VALIDATION
# ==========================================================

if not BOT_TOKEN:

    raise RuntimeError(
        "BOT_TOKEN is missing in Railway Variables."
    )

if ADMIN_ID <= 0:

    raise RuntimeError(
        "ADMIN_ID is missing in Railway Variables."
    )

# ==========================================================
# EXPORTS
# ==========================================================

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

    "WEBAPP_URL",

    "SECRET_KEY",

    "ASSETS_FOLDER",

    "DATA_FOLDER",

    "WELCOME_IMAGE",

]
