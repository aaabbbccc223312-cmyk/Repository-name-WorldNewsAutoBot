import os

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import (
    WELCOME_IMAGE,
    WELCOME_MESSAGE,
)

from database import save_user
from bot.keyboards import join_keyboard
from bot.membership import get_missing_channels


# ==========================================================
# /start
# ==========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if update.message is None:
        return

    # Save user
    await save_user(update.effective_user)

    keyboard = await join_keyboard()

    # Send welcome image if available
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


# ==========================================================
# VERIFY JOIN
# ==========================================================

async def check_join(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    if query is None:
        return

    await query.answer()

    missing = await get_missing_channels(
        update,
        context.bot,
    )

    # ------------------------------------------------------
    # USER HAS NOT JOINED EVERY CHANNEL
    # ------------------------------------------------------

    if missing:

        keyboard = await join_keyboard()

        text = (
            "❌ <b>You haven't joined all required channels.</b>\n\n"
            "Please join every channel below before continuing.\n\n"
        )

        for channel in missing:

            text += f"• {channel}\n"

        text += (
            "\nAfter joining them all, press\n"
            "<b>✅ I've Joined</b> again."
        )

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

    # ------------------------------------------------------
    # USER VERIFIED
    # ------------------------------------------------------

    await save_user(update.effective_user)

    success = (
        "🎉 <b>Verification Successful!</b>\n\n"
        "✅ Thank you for joining all required channels.\n\n"
        "Welcome to <b>AATG</b> ❤️\n\n"
        "You now have full access to the bot."
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
