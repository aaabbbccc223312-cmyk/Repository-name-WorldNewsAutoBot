"""
news/scheduler.py
"""

import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import NEWS_CHECK_INTERVAL

from news.fetcher import fetcher
from news.formatter import formatter
from news.sender import sender
from news.router import router

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def post_news():

    logger.info("===== Checking RSS feeds =====")

    articles = fetcher.fetch()

    logger.info("Fetched %s article(s)", len(articles))

    if not articles:
        return

    assignments = await router.distribute(articles)

    logger.info("Assignments: %s", len(assignments))

    for channel, article in assignments:

        caption = formatter.format(article)

        await sender.send(
            channel,
            article,
            caption,
        )

        await router.mark_posted(
            channel,
            article,
        )

        logger.info(
            "Posted to %s",
            channel["username"],
        )


def start_scheduler():

    if scheduler.running:
        return

    scheduler.add_job(
        post_news,
        "interval",
        seconds=NEWS_CHECK_INTERVAL,
        id="news_job",
        replace_existing=True,
    )

    scheduler.start()

    logger.info("News scheduler started.")
