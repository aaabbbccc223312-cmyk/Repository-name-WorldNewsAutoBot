import os
from dotenv import load_dotenv

# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv()

# ==========================================
# BOT
# ==========================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

ADMIN_ID = int(
    os.getenv("ADMIN_ID", "0")
)

# ==========================================
# DATABASE
# ==========================================

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "data/bot.db",
)

# ==========================================
# IMAGES
# ==========================================

WELCOME_IMAGE = os.getenv(
    "WELCOME_IMAGE",
    "assets/welcome.jpg",
)

DEFAULT_NEWS_IMAGE = os.getenv(
    "DEFAULT_NEWS_IMAGE",
    "assets/default_news.jpg",
)

# ==========================================
# WELCOME MESSAGE
# ==========================================

WELCOME_MESSAGE = """
🌟 <b>Welcome to AATG</b>

Atg is a Buy & Sell Token application.

💰 Earn every time you buy tokens using INR or USDT.

📢 Before using this bot, please join all the required channels below.

After joining, tap the <b>✅ I've Joined</b> button.

Thank you for supporting AATG ❤️
""".strip()

# ==========================================
# NEWS SETTINGS
# ==========================================

CHECK_INTERVAL = 300          # 5 minutes

MAX_POSTS_PER_RUN = 20

POST_DELAY = 2

# ==========================================
# LOGGING
# ==========================================

LOG_LEVEL = "INFO"

# ==========================================
# DEFAULT CHANNELS
# These are added automatically on first run.
# Later you'll use /addchannel so you won't
# need to edit this file again.
# ==========================================

DEFAULT_CHANNELS = [
    "@paisabase1",
    "@aatgpay",
    "@smrtwallet",
]

# ==========================================
# RSS FEEDS
# Global sources.
# Later every channel can have its own feed.
# ==========================================

RSS_FEEDS = [

    # World News
    "https://feeds.bbci.co.uk/news/rss.xml",

    "https://www.reutersagency.com/feed/?best-topics=world",

    # Sports
    "https://feeds.bbci.co.uk/sport/rss.xml",

    "https://www.espn.com/espn/rss/news",

    "https://www.skysports.com/rss/12040",

]
