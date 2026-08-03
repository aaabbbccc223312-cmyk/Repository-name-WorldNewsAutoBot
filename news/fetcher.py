"""
news/fetcher.py

Professional RSS Fetcher
"""

import hashlib
import logging
from collections import deque

import feedparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (NewsBot)"
}

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

        self.cache_queue = deque()

        self.max_cache = 5000

    def clean(self, text):

        if not text:
            return ""

        return BeautifulSoup(
            text,
            "html.parser",
        ).get_text(
            " ",
            strip=True,
        )

    def article_id(self, link):

        return hashlib.md5(
            link.encode(
                "utf-8",
            )
        ).hexdigest()

    def trim_cache(self):

        while len(self.cache_queue) > self.max_cache:

            old = self.cache_queue.popleft()

            self.cache.discard(old)

    def extract_image(self, entry):

        if getattr(entry, "media_content", None):

            media = entry.media_content

            if media:

                url = media[0].get("url")

                if url:
                    return url

        if getattr(entry, "media_thumbnail", None):

            thumb = entry.media_thumbnail

            if thumb:

                url = thumb[0].get("url")

                if url:
                    return url

        if getattr(entry, "enclosures", None):

            for enc in entry.enclosures:

                if enc.get("type", "").startswith("image"):

                    return enc.get("href")

        try:

            response = requests.get(
                entry.link,
                timeout=8,
                headers=HEADERS,
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser",
            )

            og = soup.find(
                "meta",
                property="og:image",
            )

            if og:

                image = og.get("content")

                if image:
                    return image

            img = soup.find("img")

            if img:

                src = img.get("src")

                if src:
                    return src

        except Exception:

            pass

        return None

    def fetch(self):

        articles = []

        seen_links = set()

        for category, feeds in RSS_FEEDS.items():

            for feed in feeds:

                try:

                    rss = feedparser.parse(feed)

                    if rss.bozo:

                        logger.warning(
                            "Invalid RSS: %s",
                            feed,
                        )

                    for entry in rss.entries:

                        title = self.clean(
                            entry.get(
                                "title",
                                "",
                            )
                        )

                        if len(title) < 8:
                            continue

                        link = entry.get(
                            "link",
                            "",
                        )

                        if not link:
                            continue

                        if link in seen_links:
                            continue

                        seen_links.add(link)

                        article_id = self.article_id(link)

                        if article_id in self.cache:
                            continue

                        self.cache.add(article_id)

                        self.cache_queue.append(article_id)

                        summary = self.clean(
                            entry.get(
                                "summary",
                                "",
                            )
                        )

                        articles.append({

                            "id": article_id,

                            "category": category,

                            "title": title,

                            "summary": summary,

                            "link": link,

                            "image": self.extract_image(entry),

                            "source": rss.feed.get(
                                "title",
                                "News",
                            ),

                        })

                except Exception as e:

                    logger.exception(
                        "RSS failed: %s",
                        feed,
                    )

        self.trim_cache()

        logger.info(
            "Fetched %s unique articles.",
            len(articles),
        )

        return articles


fetcher = NewsFetcher()
