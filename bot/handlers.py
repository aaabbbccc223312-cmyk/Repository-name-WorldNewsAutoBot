"""
bot/handlers.py

Main bot handlers.
"""

import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    WebAppInfo,
)

from telegram.ext import ContextTypes

from config import WEBAPP_URL

from database import save_user

from bot.membership import has_joined_all
from bot.keyboards import join_keyboard


logger = logging.getLogger(__name__)


WELCOME_TEXT = """
🌍 <b>Welcome to AATG Global News</b>

Stay ahead with real-time updates from trusted sources.

📰 Breaking News
🌍 World News
⚽ Sports
💼 Business
💻 Technology
📈 Trading & Crypto

━━━━━━━━━━━━━━━━━━

<b>Before continuing, please join all required channels.</b>

Once you've joined, tap:

<b>✅ I've Joined</b>

to unlock the Mini App.
"""


def mini_app_keyboard():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🚀 Open Mini App",
                    web_app=WebAppInfo(
                        url=WEBAPP_URL
                    ),
                )
            ]
        ]
    )


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    try:

        user = update.effective_user

        logger.info(
            "Start command from %s",
            user.id,
        )

        await save_user(user)

        joined = await has_joined_all(
            user.id
        )

        if not joined:

            await update.message.reply_text(
                text=WELCOME_TEXT,
                parse_mode="HTML",
                reply_markup=join_keyboard(),
            )

            return

        await update.message.reply_text(
            text=(
                "🎉 <b>Access Granted!</b>\n\n"
                "Welcome to AATG.\n\n"
                "Tap below to open the Mini App."
            ),
            parse_mode="HTML",
            reply_markup=mini_app_keyboard(),
        )

    except Exception:

        logger.exception(
            "START ERROR"
        )

        if update.message:

            await update.message.reply_text(
                "⚠️ Something went wrong.\nPlease try again."
            )


async def check_join(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    try:

        joined = await has_joined_all(
            query.from_user.id
        )

        if joined:

            await query.edit_message_text(
                text=(
                    "✅ <b>Verification Successful!</b>\n\n"
                    "You now have access to AATG.\n\n"
                    "Open the Mini App below."
                ),
                parse_mode="HTML",
                reply_markup=mini_app_keyboard(),
            )

        else:

            await query.answer(
                "❌ Please join every required channel first.",
                show_alert=True,
            )

    except Exception:

        logger.exception(
            "VERIFY ERROR"
        )

        await query.answer(
            "⚠️ Verification failed.",
            show_alert=True,
        )
