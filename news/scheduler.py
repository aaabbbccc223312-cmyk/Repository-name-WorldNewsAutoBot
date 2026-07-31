"""
news/scheduler.py

Runs the news engine automatically every few minutes.
"""

import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import RSS_FETCH_INTERVAL
from news.poster import poster

logger = logging.getLogger(__name__)


class NewsScheduler:

    def __init__(self):

        self.scheduler = AsyncIOScheduler()

    async def job(self):

        logger.info("=" * 60)
        logger.info("Checking RSS feeds...")
        logger.info("=" * 60)

        try:

            await poster.run()

        except Exception as e:

            logger.exception(e)

    def start(self):

        if self.scheduler.running:
            return

        self.scheduler.add_job(
            self.job,
            trigger="interval",
            seconds=RSS_FETCH_INTERVAL,
            id="rss_news_job",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )

        self.scheduler.start()

        logger.info("News Scheduler Started")
        logger.info(
            f"Checking news every {RSS_FETCH_INTERVAL} seconds."
        )

    def shutdown(self):

        if self.scheduler.running:
            self.scheduler.shutdown()


scheduler = NewsScheduler()
