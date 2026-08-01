"""
news/router.py

Distributes unique news across channels.
"""

import random

from database import (

    get_channels,

    has_posted,

    save_post,

)


class NewsRouter:

    def __init__(

        self,

    ):

        pass


    async def distribute(

        self,

        articles,

    ):

        channels = await get_channels()

        if not channels:

            return []

        if not articles:

            return []

        random.shuffle(

            articles

        )

        assignments = []

        article_index = 0
        for channel in channels:

            assigned = False

            while article_index < len(

                articles

            ):

                article = articles[

                    article_index

                ]

                article_index += 1

                if await has_posted(

                    channel["username"],

                    article["id"],

                ):

                    continue

                assignments.append(

                    (

                        channel,

                        article,

                    )

                )

                assigned = True

                break

            if not assigned:

                break

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
