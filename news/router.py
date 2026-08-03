"""
news/router.py

Routes news articles to the correct Telegram channels.
"""

import logging

from database import (
    get_channels,
    has_posted,
    save_post,
)

logger = logging.getLogger(__name__)


class NewsRouter:

    async def distribute(self, articles):

        channels = await get_channels()

        if not channels:
            logger.warning("No channels configured.")
            return []

        assignments = []

        for article in articles:

            category = (
                article.get(
                    "category",
                    "world",
                )
                .lower()
                .strip()
            )

            matched = False

            for channel in channels:

                channel_category = (
                    channel["category"]
                    or "world"
                ).lower().strip()

                if channel_category != category:
                    continue

                already_posted = await has_posted(
                    channel["username"],
                    article["id"],
                )

                if already_posted:
                    continue

                assignments.append(
                    (
                        channel,
                        article,
                    )
                )

                matched = True
                break

            if not matched:
                logger.debug(
                    "No channel available for '%s' (%s)",
                    article["title"],
                    category,
                )

        logger.info(
            "Prepared %s post assignment(s).",
            len(assignments),
        )

        return assignments

    async def mark_posted(
        self,
        channel,
        article,
    ):

        await save_post(
            channel["username"],
            article["id"],
            article["title"],
        )


router = NewsRouter()
