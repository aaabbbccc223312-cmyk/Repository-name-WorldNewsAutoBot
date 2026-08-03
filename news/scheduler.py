"""
news/scheduler.py

Category-aware news scheduler.
"""

import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import NEWS_CHECK_INTERVAL

from news.fetcher import fetcher
from news.formatter import formatter
from news.router import router
from news.sender import sender

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def post_news():

    logger.info("Checking RSS feeds...")

    try:

        articles = fetcher.fetch()

    except Exception:

        logger.exception("Failed to fetch RSS feeds.")

        return

    if not articles:

        logger.info("No new articles found.")

        return

    try:

        assignments = await router.distribute(
            articles
        )

    except Exception:

        logger.exception("Router failed.")

        return

    if not assignments:

        logger.info("Nothing to post.")

        return

    total = 0

    for channel, article in assignments:

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

            total += 1

            logger.info(
                "Posted '%s' -> %s",
                article.get("title", "Untitled"),
                channel,
            )

        except Exception:

            logger.exception(
                "Failed posting to %s",
                channel,
            )

    logger.info(
        "Finished posting %s article(s).",
        total,
    )


scheduler.add_job(
    post_news,
    trigger="interval",
    seconds=NEWS_CHECK_INTERVAL,
    id="post_news",
    replace_existing=True,
    max_instances=1,
    coalesce=True,
)
