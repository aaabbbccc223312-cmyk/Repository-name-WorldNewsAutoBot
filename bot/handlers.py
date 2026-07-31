from telegram import Update
from telegram.ext import ContextTypes

from config import WELCOME_MESSAGE
from bot.keyboards import join_keyboard
from bot.membership import get_missing_channels
from database import save_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    # Save user to database
    await save_user(user)

    # Send welcome message
    await update.message.reply_text(
        text=WELCOME_MESSAGE,
        reply_markup=join_keyboard(),
        disable_web_page_preview=True,
    )


async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    missing = await get_missing_channels(update, context.bot)

    if missing:

        text = (
            "❌ <b>You haven't joined all required channels.</b>\n\n"
            "Please join every channel below before continuing:\n\n"
        )

        for channel in missing:
            text += f"• {channel}\n"

        text += "\nAfter joining, press <b>✅ I've Joined</b> again."

        await query.edit_message_text(
            text=text,
            reply_markup=join_keyboard(),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        return

    # Save again just in case user wasn't recorded previously
    await save_user(update.effective_user)

    await query.edit_message_text(
        text=(
            "🎉 <b>Verification Successful!</b>\n\n"
            "Welcome to AATG.\n\n"
            "You now have full access to this bot."
        ),
        parse_mode="HTML",
    )
