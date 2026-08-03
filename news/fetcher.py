"""
news/fetcher.py

Fast, reliable RSS fetcher with duplicate protection.
"""

import hashlib
import logging
import time
from concurrent.futures import ThreadPoolExecutor

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
        self.cache = {}
        self.cache_expire = 86400

    def clean(self, text):

        if not text:
            return ""

        try:
            return BeautifulSoup(
                str(text),
                "html.parser",
            ).get_text(
                " ",
                strip=True,
            )
        except Exception:
            return str(text)

    def article_id(self, link):

        return hashlib.sha256(
            link.encode("utf-8")
        ).hexdigest()

    def image(self, entry):

        try:

            if hasattr(entry, "media_content"):
                media = entry.media_content
                if media:
                    return media[0].get("url")

            if hasattr(entry, "media_thumbnail"):
                media = entry.media_thumbnail
                if media:
                    return media[0].get("url")

            if hasattr(entry, "links"):

                for item in entry.links:

                    if item.get(
                        "type",
                        "",
                    ).startswith("image"):

                        return item.get("href")

            if "summary" in entry:

                soup = BeautifulSoup(
                    entry.summary,
                    "html.parser",
                )

                img = soup.find("img")

                if img:
                    return img.get("src")

        except Exception:
            pass

        return None

    def fetch_feed(self, category, url):

        articles = []

        try:

            rss = feedparser.parse(url)

            if rss.bozo:
                logger.warning(
                    "RSS warning: %s",
                    url,
                )

            source = rss.feed.get(
                "title",
                category.title(),
            )

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

                article_id = self.article_id(
                    link
                )

                if article_id in self.cache:
                    continue

                self.cache[
                    article_id
                ] = time.time()

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
                        "image": self.image(
                            entry
                        ),
                        "source": source,
                    }
                )

        except Exception:

            logger.exception(
                "Failed RSS: %s",
                url,
            )

        return articles

    def cleanup_cache(self):

        now = time.time()

        expired = [
            key
            for key, value in self.cache.items()
            if now - value > self.cache_expire
        ]

        for key in expired:
            del self.cache[key]

    def fetch(self):

        self.cleanup_cache()

        articles = []

        futures = []

        with ThreadPoolExecutor(
            max_workers=8
        ) as executor:

            for category, feeds in RSS_FEEDS.items():

                for url in feeds:

                    futures.append(
                        executor.submit(
                            self.fetch_feed,
                            category,
                            url,
                        )
                    )

            for future in futures:

                try:

                    articles.extend(
                        future.result()
                    )

                except Exception:

                    logger.exception(
                        "Worker failed."
                    )

        unique = {}

        for article in articles:
            unique[
                article["id"]
            ] = article

        articles = list(
            unique.values()
        )

        articles.sort(
            key=lambda x: x["title"]
        )

        logger.info(
            "Fetched %s unique articles.",
            len(articles),
        )

        return articles


fetcher = NewsFetcher()
