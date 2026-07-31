"""
news/router.py

Smart News Router

Features
--------
✅ Different news for every channel
✅ No duplicate posts
✅ Unlimited channels
✅ Fair article distribution
"""

import random

from database import (
    get_channels,
    has_posted,
    save_post,
)


class NewsRouter:

    def __init__(self):
        pass

    async def distribute(self, articles):
        """
        Returns:
        [
            (channel, article),
            (channel, article),
            ...
        ]
        """

        channels = await get_channels()

        if not channels or not articles:
            return []

        # Randomize articles so channels don't always
        # receive the same order.
        random.shuffle(articles)

        assignments = []

        article_index = 0

        for channel in channels:

            assigned = False

            while article_index < len(articles):

                article = articles[article_index]
                article_index += 1

                already_posted = await has_posted(
                    channel,
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

                assigned = True
                break

            # No more fresh articles available
            if not assigned:
                break

        return assignments

    async def mark_posted(
        self,
        channel,
        article_id,
    ):
        """
        Save successful post so it is never
        repeated in this channel.
        """

        await save_post(
            channel,
            article_id,
        )


router = NewsRouter()
