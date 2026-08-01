from telegram import Update

from telegram.constants import ParseMode

from telegram.ext import ContextTypes

from bot.keyboards import join_keyboard

from bot.membership import has_joined_all

from database import save_user

from config import WELCOME_IMAGE


async def start(

    update: Update,

    context: ContextTypes.DEFAULT_TYPE,

):

    user = update.effective_user

    await save_user(

        user

    )

    joined = await has_joined_all(

        user.id

    )

    if not joined:

        caption = (

            "🌟 <b>Welcome to AATG</b>\n\n"

            "To use this bot you must join all the channels below.\n\n"

            "After joining, press <b>✅ I HAVE JOINED</b>."

        )        await update.message.reply_photo(

            photo=open(

                WELCOME_IMAGE,

                "rb",

            ),

            caption=caption,

            parse_mode=ParseMode.HTML,

            reply_markup=join_keyboard(),

        )

        return

    await update.message.reply_text(

        "✅ Welcome! You now have access to the bot.",

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

        await query.message.edit_caption(

            caption=(

                "✅ <b>Verification Successful!</b>\n\n"

                "You have joined all the required channels."

            ),

            parse_mode=ParseMode.HTML,

            reply_markup=None,

        )

    else:

        await query.answer(

            text="❌ Please join all required channels first.",

            show_alert=True,

        )
