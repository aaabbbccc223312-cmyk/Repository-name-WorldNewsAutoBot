"""
news/router.py

Routes articles to channels based on category.
"""

from database import (
    get_channels,
    has_posted,
    save_post,
)


class NewsRouter:

    def __init__(self):
        pass

    def detect_category(self, article):

        text = (
            f"{article.get('title', '')} "
            f"{article.get('summary', '')}"
        ).lower()

        if any(word in text for word in [
            "forex",
            "trading",
            "market",
            "stocks",
            "shares",
            "invest",
            "bitcoin",
            "ethereum",
            "crypto",
            "gold",
            "oil",
            "nasdaq",
            "dow",
            "fed",
            "interest rate",
        ]):
            return "trading"

        if any(word in text for word in [
            "football",
            "soccer",
            "premier league",
            "champions league",
            "nba",
            "tennis",
            "formula 1",
            "cricket",
        ]):
            return "sports"

        if any(word in text for word in [
            "business",
            "economy",
            "company",
            "bank",
            "finance",
            "inflation",
            "earnings",
        ]):
            return "business"

        if any(word in text for word in [
            "ai",
            "technology",
            "apple",
            "google",
            "microsoft",
            "android",
            "iphone",
            "openai",
        ]):
            return "technology"

        return "world"

    async def distribute(self, articles):

        channels = await get_channels()

        if not channels or not articles:
            return []

        assignments = []

        for article in articles:

            category = self.detect_category(article)

            for channel in channels:

                channel_category = (
                    channel["category"] or "world"
                ).lower()

                if channel_category != category:
                    continue

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
