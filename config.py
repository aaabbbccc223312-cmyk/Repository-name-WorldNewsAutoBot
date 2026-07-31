import os
from dotenv import load_dotenv

load_dotenv()

# ===========================
# BOT
# ===========================

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# ===========================
# DATABASE
# ===========================

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/bot.db",
)

# ===========================
# IMAGES
# ===========================

WELCOME_IMAGE = os.getenv(
    "WELCOME_IMAGE",
    "assets/welcome.jpg",
)

DEFAULT_NEWS_IMAGE = os.getenv(
    "DEFAULT_NEWS_IMAGE",
    "assets/default_news.jpg",
)

# ===========================
# WELCOME
# ===========================

WELCOME_MESSAGE = os.getenv(
    "WELCOME_MESSAGE",
    """
🌟 <b>Welcome to AATG</b>

Before using this bot, please join all the required channels below.

After joining, press the <b>✅ I've Joined</b> button.

Thank you for supporting our community ❤️
""",
)

# ===========================
# LOGGING
# ===========================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)

# ===========================
# RSS
# ===========================

RSS_FETCH_INTERVAL = 300

MAX_POSTS_PER_RUN = 20

# ===========================
# TELEGRAM LIMITS
# ===========================

MAX_CAPTION = 1024

MAX_MESSAGE = 4096

# ===========================
# DEFAULT CHANNELS
# (Added to DB only if empty)
# ===========================

DEFAULT_CHANNELS = [
    "@paisabase1",
    "@aatgpay",
    "@smrtwallet",
]
