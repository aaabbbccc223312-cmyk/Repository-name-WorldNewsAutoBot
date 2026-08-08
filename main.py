import logging
import os
import threading

import uvicorn
from fastapi.responses import HTMLResponse

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
)

from config import (
    BOT_TOKEN,
    LOG_LEVEL,
    DEFAULT_CHANNELS,
)

from database import (
    init_db,
    add_channel,
)

from bot.handlers import (
    start,
    check_join,
)

from bot.commands import (
    addchannel,
    removechannel,
    pausechannel,
    resumechannel,
    channels,
    stats,
)

from news.scheduler import (
    start_scheduler,
    post_news,
)

from web import app as web_app


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("AATG")


# ============================================================
# RAILWAY / WEB HOMEPAGE
# ============================================================

@web_app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Global News Network</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                min-height: 100vh;
                font-family: Arial, Helvetica, sans-serif;
                background:
                    radial-gradient(circle at top, #172554 0%, #090d1a 45%, #05070d 100%);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 25px;
            }

            .container {
                width: 100%;
                max-width: 720px;
                text-align: center;
            }

            .logo {
                width: 90px;
                height: 90px;
                margin: 0 auto 25px;
                border-radius: 50%;
                background: white;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 42px;
            }

            h1 {
                margin: 0 0 12px;
                font-size: 34px;
            }

            .subtitle {
                color: #b8c1d9;
                font-size: 17px;
                margin-bottom: 30px;
            }

            .status {
                display: inline-flex;
                align-items: center;
                gap: 9px;
                background: rgba(34, 197, 94, 0.12);
                border: 1px solid rgba(34, 197, 94, 0.35);
                color: #4ade80;
                padding: 10px 18px;
                border-radius: 999px;
                margin-bottom: 30px;
                font-weight: bold;
            }

            .dot {
                width: 9px;
                height: 9px;
                background: #22c55e;
                border-radius: 50%;
                box-shadow: 0 0 12px #22c55e;
            }

            .cards {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-bottom: 30px;
            }

            .card {
                background: rgba(255,255,255,0.06);
                border: 1px solid rgba(255,255,255,0.10);
                border-radius: 16px;
                padding: 22px 15px;
                backdrop-filter: blur(10px);
            }

            .icon {
                font-size: 28px;
                margin-bottom: 10px;
            }

            .card h3 {
                margin: 0 0 7px;
                font-size: 17px;
            }

            .card p {
                margin: 0;
                color: #9ca8c2;
                font-size: 14px;
                line-height: 1.5;
            }

            .footer {
                color: #68748f;
                font-size: 13px;
            }

            @media (max-width: 550px) {
                h1 {
                    font-size: 28px;
                }

                .cards {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>

    <body>

        <div class="container">

            <div class="logo">
                🌍
            </div>

            <h1>Global News Network</h1>

            <div class="subtitle">
                Automated worldwide news delivered to Telegram.
            </div>

            <div class="status">
                <span class="dot"></span>
                Bot is online
            </div>

            <div class="cards">

                <div class="card">
                    <div class="icon">📰</div>
                    <h3>Worldwide News</h3>
                    <p>
                        News is automatically collected from configured RSS sources.
                    </p>
                </div>

                <div class="card">
                    <div class="icon">⚡</div>
                    <h3>Automatic Posting</h3>
                    <p>
                        New articles are processed and posted automatically.
                    </p>
                </div>

                <div class="card">
                    <div class="icon">📡</div>
                    <h3>Live Scheduler</h3>
                    <p>
                        The news scheduler continuously runs in the background.
                    </p>
                </div>

                <div class="card">
                    <div class="icon">🤖</div>
                    <h3>Telegram Bot</h3>
                    <p>
                        The Telegram bot is connected and running.
                    </p>
                </div>

            </div>

            <div class="footer">
                © Global News Network · Automated News System
            </div>

        </div>

    </body>
    </html>
    """


# ============================================================
# BOT STARTUP
# ============================================================

async def startup(application: Application):

    os.makedirs(
        "assets",
        exist_ok=True,
    )

    os.makedirs(
        "data",
        exist_ok=True,
    )

    os.makedirs(
        "webapp",
        exist_ok=True,
    )

    await init_db()

    for channel in DEFAULT_CHANNELS:
        await add_channel(channel)

    # Start the news scheduler
    start_scheduler()

    logger.info("Running first news check...")

    try:
        await post_news()

    except Exception:
        logger.exception(
            "First news check failed."
        )

    logger.info(
        "Bot started successfully."
    )


# ============================================================
# BOT SHUTDOWN
# ============================================================

async def shutdown(application: Application):

    logger.info(
        "Bot stopped."
    )


# ============================================================
# WEB SERVER
# ============================================================

def run_web():

    port = int(
        os.getenv(
            "PORT",
            "8080",
        )
    )

    logger.info(
        "Starting web server on port %s",
        port,
    )

    uvicorn.run(
        web_app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )


# ============================================================
# MAIN
# ============================================================

def main():

    # Start FastAPI / Railway web server
    threading.Thread(
        target=run_web,
        daemon=True,
    ).start()

    # Create Telegram application
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(startup)
        .post_shutdown(shutdown)
        .build()
    )

    # ========================================================
    # TELEGRAM HANDLERS
    # ========================================================

    application.add_handler(
        CommandHandler(
            "start",
            start,
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            check_join,
            pattern="^verify_join$",
        )
    )

    application.add_handler(
        CommandHandler(
            "addchannel",
            addchannel,
        )
    )

    application.add_handler(
        CommandHandler(
            "removechannel",
            removechannel,
        )
    )

    application.add_handler(
        CommandHandler(
            "pausechannel",
            pausechannel,
        )
    )

    application.add_handler(
        CommandHandler(
            "resumechannel",
            resumechannel,
        )
    )

    application.add_handler(
        CommandHandler(
            "channels",
            channels,
        )
    )

    application.add_handler(
        CommandHandler(
            "stats",
            stats,
        )
    )

    # ========================================================
    # START TELEGRAM POLLING
    # ========================================================

    application.run_polling(
        drop_pending_updates=True,
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
