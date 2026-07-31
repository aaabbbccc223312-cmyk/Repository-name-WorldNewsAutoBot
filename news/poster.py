"""
news/poster.py

Automatic News Poster

Workflow
--------
1. Fetch news
2. Format news
3. Assign different news to each channel
4. Send image (or fallback)
5. Mark article as posted
"""

import logging

from news.fetcher import fetcher
from news.formatter import formatter
from news.router import router
from bot.telegram import telegram

logger = logging.getLogger(__name__)


class NewsPoster:

    async def run(self):

        logger.info("Checking for latest news...")

        articles = fetcher.fetch()

        if not articles:
            logger.info("No new articles found.")
            return

        assignments = await router.distribute(articles)

        if not assignments:
            logger.info("No channels available or no fresh articles.")
            return

        success = 0

        for channel, article in assignments:

            caption = formatter.format(article)

            image = article.get("image")

            try:

                if image:

                    sent = await telegram.send_photo_url(
                        channel=channel,
                        image_url=image,
                        caption=caption,
                    )

                else:

                    sent = await telegram.send_default_photo(
                        channel=channel,
                        caption=caption,
                    )

                if sent:

                    await router.mark_posted(
                        channel,
                        article["id"],
                    )

                    success += 1

                    logger.info(
                        f"Posted '{article['title']}' -> {channel}"
                    )

            except Exception as e:

                logger.exception(e)

        logger.info(
            f"Posting completed. Successful posts: {success}"
        )


poster = NewsPoster()
