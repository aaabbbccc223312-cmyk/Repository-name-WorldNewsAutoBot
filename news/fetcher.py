"""
news/fetcher.py

Smart RSS Fetcher
"""

import hashlib
import logging

import feedparser
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


RSS_FEEDS = {

    "world": [

        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",

    ],

    "sports": [

        "https://feeds.bbci.co.uk/sport/rss.xml",
        "https://www.espn.com/espn/rss/news",

    ],

    "business": [

        "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",

    ],

    "technology": [

        "https://feeds.arstechnica.com/arstechnica/index",

    ],

    "trading": [

        "https://www.forexlive.com/feed/",
        "https://www.coindesk.com/arc/outboundfeeds/rss/",

    ],

}


class NewsFetcher:

    def __init__(self):

        self.cache = set()

    def clean(self, text):

        return BeautifulSoup(
            text,
            "html.parser",
        ).get_text(
            " ",
            strip=True,
        )

    def article_id(self, link):

        return hashlib.md5(
            link.encode()
        ).hexdigest()

    def image(self, entry):

        if "media_content" in entry:
            media = entry.media_content
            if media:
                return media[0].get("url")

        if "media_thumbnail" in entry:
            thumb = entry.media_thumbnail
            if thumb:
                return thumb[0].get("url")

        if "links" in entry:

            for link in entry.links:

                if link.get(
                    "type",
                    "",
                ).startswith("image"):

                    return link.get("href")

        return None

    def fetch(self):

        articles = []

        for category, feeds in RSS_FEEDS.items():

            for feed in feeds:

                try:

                    rss = feedparser.parse(feed)

                    for entry in rss.entries:

                        title = self.clean(
                            entry.get(
                                "title",
                                "",
                            )
                        )

                        link = entry.get(
                            "link",
                            "",
                        )

                        if not title or not link:
                            continue

                        article_id = self.article_id(link)

                        if article_id in self.cache:
                            continue

                        self.cache.add(article_id)

                        articles.append(

                            {

                                "id": article_id,

                                "category": category,

                                "title": title,

                                "summary": self.clean(
                                    entry.get(
                                        "summary",
                                        "",
                                    )
                                ),

                                "link": link,

                                "image": self.image(entry),

                                "source": rss.feed.get(
                                    "title",
                                    "News",
                                ),

                            }

                        )

                except Exception as e:

                    logger.warning(
                        "RSS failed: %s",
                        feed,
                    )

        logger.info(
            "Fetched %s articles",
            len(articles),
        )

        return articles


fetcher = NewsFetcher()
