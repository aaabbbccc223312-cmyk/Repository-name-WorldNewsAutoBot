from telegram import Update
from telegram.ext import ContextTypes

from config import WELCOME_MESSAGE
from bot.keyboards import join_keyboard
from bot.membership import get_missing_channels
from database import save_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""

    user = update.effective_user

    # Save user
    await save_user(user)

    # Send welcome message with dynamic join buttons
    await update.message.reply_text(
        text=WELCOME_MESSAGE,
        reply_markup=await join_keyboard(),
        disable_web_page_preview=True,
        parse_mode="HTML",
    )


async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the 'I've Joined' button."""

    query = update.callback_query
    await query.answer()

    # Check missing channels
    missing = await get_missing_channels(update, context.bot)

    if missing:
        text = (
            "❌ <b>You haven't joined all required channels.</b>\n\n"
            "Please join every channel below:\n\n"
        )

        for channel in missing:
            text += f"• {channel}\n"

        text += "\nAfter joining all channels, press <b>✅ I've Joined</b> again."

        await query.edit_message_text(
            text=text,
            reply_markup=await join_keyboard(),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        return

    # Save user again (safe if already saved)
    await save_user(update.effective_user)

    await query.edit_message_text(
        text=(
            "🎉 <b>Verification Successful!</b>\n\n"
            "✅ You have successfully joined all required channels.\n\n"
            "Welcome to <b>AATG Global Network</b>!\n\n"
            "You now have full access to the bot."
        ),
        parse_mode="HTML",
    )
