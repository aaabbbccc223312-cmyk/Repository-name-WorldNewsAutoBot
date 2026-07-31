import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

CHANNELS = [
    channel.strip()
    for channel in os.getenv("CHANNELS", "").split(",")
    if channel.strip()
]

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

DATABASE_PATH = "data/news.db"

RSS_FEEDS = [
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://feeds.bbci.co.uk/news/business/rss.xml",
    "https://rss.cnn.com/rss/edition_world.rss",
    "https://rss.cnn.com/rss/edition.rss",
    "https://feeds.skynews.com/feeds/rss/world.xml",
    "https://feeds.reuters.com/reuters/worldNews",
]
