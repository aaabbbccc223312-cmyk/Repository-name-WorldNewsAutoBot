"""
news/scheduler.py

Professional queued news scheduler.
"""

import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import (
    NEWS_CHECK_INTERVAL,
    MAX_POSTS_PER_CYCLE,
)

from news.fetcher import fetcher
from news.formatter import formatter
from news.router import router
from news.sender import sender

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def post_news():

    logger.info("=" * 60)
    logger.info("Checking RSS feeds...")

    try:

        articles = fetcher.fetch()

    except Exception:

        logger.exception(
            "RSS fetch failed."
        )

        return

    logger.info(
        "Fetched %s article(s).",
        len(articles),
    )

    if not articles:

        logger.info(
            "No articles available."
        )

        return

    try:

        assignments = await router.distribute(
            articles
        )

    except Exception:

        logger.exception(
            "Router failed."
        )

        return

    logger.info(
        "Queue contains %s post(s).",
        len(assignments),
    )

    if not assignments:

        logger.info(
            "Nothing to send."
        )

        return

    posted = 0

    skipped = 0

    failed = 0

    for channel, article in assignments:

        if posted >= MAX_POSTS_PER_CYCLE:

            logger.info(
                "Reached cycle limit (%s posts).",
                MAX_POSTS_PER_CYCLE,
            )

            break

        try:

            caption = formatter.format(
                article
            )

            await sender.send(
                channel,
                article,
                caption,
            )

            await router.mark_posted(
                channel,
                article,
            )

            posted += 1

            logger.info(
                "[%s/%s] Posted '%s' -> %s",
                posted,
                MAX_POSTS_PER_CYCLE,
                article.get(
                    "title",
                    "Untitled",
                ),
                channel["username"],
            )

            #
            # Wait between posts.
            # Prevents Telegram FloodWait.
            #
            await asyncio.sleep(3)

        except Exception:

            failed += 1

            logger.exception(
                "Failed posting '%s' -> %s",
                article.get(
                    "title",
                    "Untitled",
                ),
                channel["username"],
            )

            #
            # Small pause before continuing.
            #
            await asyncio.sleep(2)

    logger.info("=" * 60)

    logger.info(
        "Cycle complete."
    )

    logger.info(
        "Posted : %s",
        posted,
    )

    logger.info(
        "Failed : %s",
        failed,
    )

    logger.info(
        "Skipped: %s",
        skipped,
    )

    logger.info("=" * 60)


def start_scheduler():

    if scheduler.running:

        logger.info(
            "Scheduler already running."
        )

        return

    scheduler.add_job(

        post_news,

        trigger="interval",

        seconds=NEWS_CHECK_INTERVAL,

        id="news_scheduler",

        replace_existing=True,

        max_instances=1,

        coalesce=True,

        misfire_grace_time=300,

    )

    scheduler.start()

    logger.info(
        "News scheduler started."
    )
