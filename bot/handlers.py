from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.keyboards import join_keyboard
from bot.membership import has_joined_all
from database import save_user


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user

    await save_user(user)

    joined = await has_joined_all(user.id)

    if not joined:

        message = (
            "🌟 <b>Welcome to AATG</b>\n\n"
            "Atg is a buy and sell token application, you can earn every time you buy tokens using INR or USDT.\n\n"
            "📢 Before using this bot, you must join all the channels below.\n\n"
            "✅ After joining every channel, press <b>I HAVE JOINED</b>."
        )

        await update.message.reply_text(
            text=message,
            parse_mode=ParseMode.HTML,
            reply_markup=join_keyboard(),
        )

        return

    await update.message.reply_text(
        text=(
            "✅ <b>Verification Successful!</b>\n\n"
            "Welcome to AATG.\n"
            "You now have full access to the bot."
        ),
        parse_mode=ParseMode.HTML,
    )


async def check_join(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    await query.answer()

    joined = await has_joined_all(
        query.from_user.id
    )

    if joined:

        await query.edit_message_text(
            text=(
                "✅ <b>Verification Successful!</b>\n\n"
                "Welcome to AATG.\n"
                "You now have full access to the bot."
            ),
            parse_mode=ParseMode.HTML,
        )

    else:

        await query.answer(
            text="❌ Please join all required channels first.",
            show_alert=True,
        )
