import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNELS = [
    channel.strip()
    for channel in os.getenv(
        "CHANNELS",
        "@paisabase1,@aatgpay,@smrtwallet"
    ).split(",")
]

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

DATABASE_PATH = os.getenv("DATABASE_PATH", "news.db")
