from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)

from telegram.ext import ContextTypes

from config import WEB_APP_URL


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🌍 Open Global News",
                    web_app=WebAppInfo(
                        url=WEB_APP_URL
                    ),
                )
            ]
        ]
    )

    await update.message.reply_text(
        text=(
            "🌍 *Welcome to Global News Network*\n\n"
            "Get breaking news from around the world.\n\n"
            "Tap the button below to open the News App."
        ),
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def check_join(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    return
