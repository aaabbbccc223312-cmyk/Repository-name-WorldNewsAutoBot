import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
    Update,
)

from telegram.ext import ContextTypes

from config import (
    WEBAPP_URL,
)

from database import save_user

from bot.membership import has_joined_all

from bot.keyboards import join_keyboard


logger = logging.getLogger(__name__)


WELCOME_TEXT = """
🌍 <b>Welcome to Global News Network</b>

Get real-time news from around the world.

✅ Breaking News
⚽ Sports
💹 Business
🌎 World Headlines

Join all required channels to continue.

Or open the Mini App below.
"""


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    logger.info("========== /START RECEIVED ==========")

    try:

        user = update.effective_user

        logger.info(f"User: {user.id}")

        logger.info("Saving user...")
        await save_user(user)
        logger.info("User saved.")

        logger.info("Checking channel membership...")
        joined = await has_joined_all(user.id)
        logger.info(f"Membership result: {joined}")

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🌐 Open Mini App",
                        web_app=WebAppInfo(
                            url=WEBAPP_URL,
                        ),
                    )
                ]
            ]
        )

        if not joined:

            logger.info("User has NOT joined all channels.")

            await update.message.reply_text(
                WELCOME_TEXT,
                parse_mode="HTML",
                reply_markup=join_keyboard(),
            )

            await update.message.reply_text(
                "You can also open our Mini App.",
                reply_markup=keyboard,
            )

            return

        logger.info("User joined all channels.")

        await update.message.reply_text(
            "✅ Access granted.",
            reply_markup=keyboard,
        )

    except Exception:
        logger.exception("START COMMAND FAILED")

        if update.message:
            await update.message.reply_text(
                "⚠️ An internal error occurred. Check Railway logs."
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

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🌐 Open Mini App",
                        web_app=WebAppInfo(
                            url=WEBAPP_URL,
                        ),
                    )
                ]
            ]
        )

        if joined:

            await query.edit_message_text(
                "✅ Verification successful!\n\nOpen the Mini App below.",
                reply_markup=keyboard,
            )

        else:

            await query.answer(
                "❌ Join all required channels first.",
                show_alert=True,
            )

    except Exception:

        logger.exception("VERIFY JOIN FAILED")

        await query.answer(
            "An internal error occurred.",
            show_alert=True,
        )
