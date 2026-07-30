from telegram import Update
from telegram.ext import ContextTypes

from config import WELCOME_MESSAGE
from bot.keyboards import join_keyboard
from bot.membership import get_missing_channels


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=join_keyboard(),
    )


async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    missing = await get_missing_channels(update, context.bot)

    if missing:

        text = "❌ You haven't joined all required channels.\n\n"

        for channel in missing:
            text += f"• {channel}\n"

        text += "\nJoin them first, then press 'I've Joined' again."

        await query.edit_message_text(
            text=text,
            reply_markup=join_keyboard(),
        )

        return

    await query.edit_message_text(
        "🎉 Welcome!\n\n"
        "Your membership has been verified successfully.\n\n"
        "You now have full access."
    )
