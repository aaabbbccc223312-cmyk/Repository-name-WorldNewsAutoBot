"""
news/scheduler.py

Reliable automatic news scheduler.

- Checks RSS feeds automatically.
- Posts new articles to the configured channels.
- Prevents overlapping posting cycles.
- Runs an immediate check when the scheduler starts.
- Continues checking at NEWS_CHECK_INTERVAL.
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

_job_lock = asyncio.Lock()


async def post_news():
    """
    Fetch and publish available news.
    """

    # Prevent two posting cycles from running together.
    if _job_lock.locked():

        logger.info(
            "A news cycle is already running. Skipping this cycle."
        )

        return

    async with _job_lock:

        logger.info("=" * 60)
        logger.info("Starting news check...")
        logger.info("=" * 60)

        # --------------------------------------------------
        # FETCH NEWS
        # --------------------------------------------------

        try:

            logger.info("Checking RSS feeds...")

            articles = fetcher.fetch()

        except Exception:

            logger.exception(
                "RSS fetch failed."
            )

            return

        logger.info(
            "Fetched %s unique article(s).",
            len(articles),
        )

        if not articles:

            logger.info(
                "No articles available from RSS feeds."
            )

            return

        # --------------------------------------------------
        # DISTRIBUTE NEWS
        # --------------------------------------------------

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
            "Prepared %s assignment(s).",
            len(assignments),
        )

        if not assignments:

            logger.info(
                "No new assignments available."
            )

            return

        # --------------------------------------------------
        # POST NEWS
        # --------------------------------------------------

        posted = 0
        failed = 0

        for channel, article in assignments:

            # Respect cycle limit.
            if posted >= MAX_POSTS_PER_CYCLE:

                logger.info(
                    "Reached cycle limit (%s posts).",
                    MAX_POSTS_PER_CYCLE,
                )

                break

            title = article.get(
                "title",
                "Untitled",
            )

            username = channel.get(
                "username",
                "unknown",
            )

            try:

                logger.info(
                    "Preparing post [%s/%s] -> %s",
                    posted + 1,
                    MAX_POSTS_PER_CYCLE,
                    username,
                )

                caption = formatter.format(
                    article
                )

                await sender.send(
                    channel,
                    article,
                    caption,
                )

                # Mark only after Telegram confirms
                # that the message was sent.
                await router.mark_posted(
                    channel,
                    article,
                )

                posted += 1

                logger.info(
                    "[%s/%s] Posted '%s' -> %s",
                    posted,
                    MAX_POSTS_PER_CYCLE,
                    title,
                    username,
                )

                # Protect against Telegram rate limits.
                await asyncio.sleep(3)

            except Exception:

                failed += 1

                logger.exception(
                    "Failed posting '%s' -> %s",
                    title,
                    username,
                )

                # Continue with the next assignment.
                await asyncio.sleep(2)

        # --------------------------------------------------
        # CYCLE SUMMARY
        # --------------------------------------------------

        logger.info("=" * 60)
        logger.info("News cycle complete.")
        logger.info("Posted : %s", posted)
        logger.info("Failed : %s", failed)
        logger.info(
            "Remaining assignments: %s",
            max(
                0,
                len(assignments) - posted,
            ),
        )
        logger.info("=" * 60)


def start_scheduler():
    """
    Start the automatic news scheduler.
    """

    if scheduler.running:

        logger.info(
            "News scheduler is already running."
        )

        return

    # Make sure the interval is valid.
    interval = int(
        NEWS_CHECK_INTERVAL
    )

    if interval < 30:

        logger.warning(
            "NEWS_CHECK_INTERVAL=%s is too low. "
            "Using 30 seconds instead.",
            interval,
        )

        interval = 30

    logger.info(
        "Automatic news check interval: %s seconds.",
        interval,
    )

    scheduler.add_job(

        post_news,

        trigger="interval",

        seconds=interval,

        id="news_scheduler",

        replace_existing=True,

        max_instances=1,

        coalesce=True,

        misfire_grace_time=300,

    )

    scheduler.start()

    logger.info(
        "News scheduler started successfully."
    )

    logger.info(
        "Next automatic news check will occur "
        "in approximately %s seconds.",
        interval,
    )
