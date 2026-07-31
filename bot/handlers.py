import os

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import (
    WELCOME_IMAGE,
    WELCOME_MESSAGE,
)

from bot.keyboards import join_keyboard
from bot.membership import get_missing_channels
from database import save_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start command
    """

    if update.message is None:
        return

    user = update.effective_user

    # Save user
    await save_user(user)

    keyboard = await join_keyboard()

    # Send welcome image if it exists
    if os.path.isfile(WELCOME_IMAGE):

        with open(WELCOME_IMAGE, "rb") as photo:

            await update.message.reply_photo(
                photo=photo,
                caption=WELCOME_MESSAGE,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
            )

    else:

        await update.message.reply_text(
            text=WELCOME_MESSAGE,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )


async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Verify user joined all required channels.
    """

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    missing = await get_missing_channels(update, context.bot)

    # User has not joined every channel
    if missing:

        keyboard = await join_keyboard()

        text = (
            "❌ <b>You haven't joined all required channels.</b>\n\n"
            "Please join every channel below before using this bot.\n\n"
        )

        for channel in missing:
            text += f"• {channel}\n"

        text += "\nAfter joining, press <b>✅ I've Joined</b> again."

        try:

            await query.edit_message_caption(
                caption=text,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
            )

        except Exception:

            await query.edit_message_text(
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )

        return

    # Save user again
    await save_user(update.effective_user)

    success_text = (
        "🎉 <b>Verification Successful!</b>\n\n"
        "✅ Thank you for joining all our required channels.\n\n"
        "You now have full access to this bot.\n\n"
        "Enjoy using AATG ❤️"
    )

    try:

        await query.edit_message_caption(
            caption=success_text,
            parse_mode=ParseMode.HTML,
        )

    except Exception:

        await query.edit_message_text(
            text=success_text,
            parse_mode=ParseMode.HTML,
        )
