import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

CHANNELS = [
    channel.strip()
    for channel in os.getenv("CHANNELS", "").split(",")
    if channel.strip()
]

WELCOME_MESSAGE = os.getenv(
    "WELCOME_MESSAGE",
    "Welcome!"
)
