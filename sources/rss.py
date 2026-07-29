import hashlib
import feedparser

RSS_FEEDS = [

    "https://feeds.bbci.co.uk/news/world/rss.xml",

    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",

]


async def fetch_rss_articles():

    news = []

    for url in RSS_FEEDS:

        feed = feedparser.parse(url)

        for item in feed.entries[:5]:

            news.append(
                {
                    "id": hashlib.md5(item.link.encode()).hexdigest(),
                    "title": item.title,
                    "summary": item.get("summary", ""),
                    "url": item.link,
                    "source": feed.feed.get("title", "News"),
                    "category": "WORLD",
                }
            )

    return news
