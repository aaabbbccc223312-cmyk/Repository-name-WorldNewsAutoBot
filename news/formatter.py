"""
news/formatter.py

Formats news articles for Telegram.
Automatically generates hashtags.
"""

import re


class NewsFormatter:

    HASHTAGS = {
        "football": [
            "football",
            "premier league",
            "champions league",
            "uefa",
            "fifa",
            "laliga",
            "serie a",
            "bundesliga",
            "transfer",
            "arsenal",
            "chelsea",
            "liverpool",
            "manchester",
            "barcelona",
            "real madrid",
        ],
        "basketball": [
            "nba",
            "basketball",
            "lakers",
            "warriors",
            "celtics",
            "bucks",
        ],
        "tennis": [
            "tennis",
            "atp",
            "wta",
            "grand slam",
            "wimbledon",
            "us open",
            "roland garros",
        ],
        "cricket": [
            "cricket",
            "ipl",
            "icc",
        ],
        "formula1": [
            "formula 1",
            "f1",
            "verstappen",
            "hamilton",
            "ferrari",
            "mercedes",
        ],
        "world": [
            "breaking",
            "world",
            "politics",
            "economy",
            "business",
            "technology",
            "science",
            "health",
        ],
    }

    def hashtags(self, text: str):

        text = text.lower()

        tags = []

        for tag, words in self.HASHTAGS.items():

            if any(word in text for word in words):
                tags.append("#" + tag.capitalize())

        tags.append("#Trending")
        tags.append("#BreakingNews")

        # Remove duplicates
        tags = list(dict.fromkeys(tags))

        return " ".join(tags)

    def shorten(self, text: str, limit=350):

        text = re.sub(r"\s+", " ", text).strip()

        if len(text) <= limit:
            return text

        return text[:limit].rstrip() + "..."

    def format(self, article):

        title = article["title"]

        summary = self.shorten(article.get("summary", ""))

        source = article.get("source", "News")

        link = article["link"]

        tags = self.hashtags(
            title + " " + summary
        )

        return f"""
📰 <b>{title}</b>

{summary}

🌍 <b>Source:</b> {source}

🔗 <a href="{link}">Read Full Story</a>

{tags}
""".strip()


formatter = NewsFormatter()
