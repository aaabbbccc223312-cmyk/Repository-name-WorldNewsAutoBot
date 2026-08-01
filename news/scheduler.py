"""
news/scheduler.py

Automatically fetches and posts news.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from news.fetcher import fetcher

from news.formatter import formatter

from news.router import router

from news.sender import sender


scheduler = AsyncIOScheduler()


async def post_news():

    articles = fetcher.fetch()

    assignments = await router.distribute(

        articles

    )

    for channel, article in assignments:

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


scheduler.add_job(

    post_news,

    "interval",

    minutes=5,

)
