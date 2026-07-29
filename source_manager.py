from sources.rss import fetch_rss_articles


async def check_all_sources():

    articles = []

    articles.extend(await fetch_rss_articles())

    return articles
