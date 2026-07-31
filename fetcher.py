"""
news/fetcher.py

Fetches trending news from multiple RSS feeds.
Automatically extracts images.
Removes duplicate articles.
"""

import hashlib
import feedparser
from bs4 import BeautifulSoup


RSS_FEEDS = [

    # BBC
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://feeds.bbci.co.uk/sport/rss.xml",

    # Reuters
    "https://www.reutersagency.com/feed/?best-topics=world",
    "https://www.reutersagency.com/feed/?best-topics=sports",

    # ESPN
    "https://www.espn.com/espn/rss/news",

    # Sky Sports
    "https://www.skysports.com/rss/12040",

    # Goal
    "https://www.goal.com/feeds/en/news",

]


class NewsFetcher:

    def __init__(self):
        self.cache = set()

    def clean(self, text):

        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text(" ", strip=True)

    def article_id(self, link):

        return hashlib.md5(link.encode()).hexdigest()

    def image(self, entry):

        # media_content
        if "media_content" in entry:
            media = entry.media_content

            if media:
                return media[0].get("url")

        # media_thumbnail
        if "media_thumbnail" in entry:
            thumb = entry.media_thumbnail

            if thumb:
                return thumb[0].get("url")

        # enclosure
        if "links" in entry:
            for link in entry.links:
                if link.get("type", "").startswith("image"):
                    return link.get("href")

        return None

    def fetch(self):

        news = []

        for feed in RSS_FEEDS:

            try:

                rss = feedparser.parse(feed)

                for entry in rss.entries:

                    title = self.clean(
                        entry.get("title", "")
                    )

                    link = entry.get("link", "")

                    if not title or not link:
                        continue

                    article = self.article_id(link)

                    if article in self.cache:
                        continue

                    self.cache.add(article)

                    news.append({

                        "id": article,

                        "title": title,

                        "link": link,

                        "summary": self.clean(
                            entry.get(
                                "summary",
                                "",
                            )
                        ),

                        "image": self.image(entry),

                        "source": rss.feed.get(
                            "title",
                            "News",
                        ),

                    })

            except Exception:
                pass

        return news


fetcher = NewsFetcher()
