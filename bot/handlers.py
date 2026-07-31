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

    user = update.effective_user

    await save_user(user)

    # Send welcome image if available
    if os.path.exists(WELCOME_IMAGE):

        with open(WELCOME_IMAGE, "rb") as photo:

            await update.message.reply_photo(
                photo=photo,
                caption=WELCOME_MESSAGE,
                parse_mode=ParseMode.HTML,
                reply_markup=join_keyboard(),
            )

    else:

        await update.message.reply_text(
            text=WELCOME_MESSAGE,
            parse_mode=ParseMode.HTML,
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
            "Join every channel below and press "
            "<b>✅ I've Joined</b> again.\n\n"
        )

        for channel in missing:
            text += f"• {channel}\n"

        # If original message has a photo, edit only the caption
        try:
            await query.edit_message_caption(
                caption=text,
                parse_mode=ParseMode.HTML,
                reply_markup=join_keyboard(),
            )
        except Exception:
            await query.edit_message_text(
                text=text,
                parse_mode=ParseMode.HTML,
                reply_markup=join_keyboard(),
            )

        return

    await save_user(update.effective_user)

    success = (
        "🎉 <b>Verification Successful!</b>\n\n"
        "✅ Thank you for joining all required channels.\n\n"
        "You now have full access to this bot."
    )

    try:

        await query.edit_message_caption(
            caption=success,
            parse_mode=ParseMode.HTML,
        )

    except Exception:

        await query.edit_message_text(
            text=success,
            parse_mode=ParseMode.HTML,
        )
