from telegram import Update
from config import CHANNELS


async def get_missing_channels(update: Update, bot):
    user_id = update.effective_user.id

    missing = []

    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)

            if member.status in ("left", "kicked"):
                missing.append(channel)

        except Exception:
            missing.append(channel)

    return missing
