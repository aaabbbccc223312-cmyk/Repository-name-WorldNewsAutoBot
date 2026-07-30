from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
)

from config import BOT_TOKEN
from bot.handlers import start, check_join


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        CallbackQueryHandler(
            check_join,
            pattern="^check_join$",
        )
    )

    print("✅ Force Join Bot Started")

    app.run_polling()


if __name__ == "__main__":
    main()
