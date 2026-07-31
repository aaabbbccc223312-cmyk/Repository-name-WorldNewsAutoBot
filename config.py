import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# Telegram
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# =========================
# Channels
# Add or remove channels here.
# Example:
# CHANNELS=@paisabase1,@aatgpay,@smrtwallet,@newchannel
# =========================

CHANNELS = [
    c.strip()
    for c in os.getenv("CHANNELS", "").split(",")
    if c.strip()
]

# =========================
# News
# =========================

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

RSS_FEEDS = [

    # BBC
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.bbci.co.uk/news/business/rss.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",

    # CNN
    "https://rss.cnn.com/rss/edition_world.rss",

    # Reuters
    "https://feeds.reuters.com/reuters/worldNews",

    # Al Jazeera
    "https://www.aljazeera.com/xml/rss/all.xml",

    # CNBC
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",

    # TechCrunch
    "https://techcrunch.com/feed/",

]

# =========================
# Database
# =========================

DATA_FOLDER = "data"

DATABASE_PATH = os.path.join(
    DATA_FOLDER,
    "aatg_super_bot.db",
)

# =========================
# Images
# =========================

IMAGE_FOLDER = "images/assets"

DEFAULT_WORLD_IMAGE = "images/assets/world.jpg"
DEFAULT_TECH_IMAGE = "images/assets/technology.jpg"
DEFAULT_BUSINESS_IMAGE = "images/assets/business.jpg"
DEFAULT_SPORT_IMAGE = "images/assets/sports.jpg"
DEFAULT_HEALTH_IMAGE = "images/assets/health.jpg"

# =========================
# Logging
# =========================

LOG_LEVEL = "INFO"
