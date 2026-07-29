import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

CHANNELS = [
    channel.strip()
    for channel in os.getenv(
        "CHANNELS",
        "@paisabase1,@aatgpay,@smrtwallet"
    ).split(",")
    if channel.strip()
]

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

# Store SQLite database in the project root by default.
# Railway can create this file automatically.
DATABASE_PATH = os.getenv("DATABASE_PATH", "news.db")
