"""
news/formatter.py

Professional Telegram Formatter
"""

from datetime import datetime


class Formatter:

    def __init__(self):

        self.hashtags = {

            "world": "#WorldNews 🌍",

            "breaking": "#BreakingNews 🚨",

            "sports": "#Sports ⚽",

            "business": "#Business 💼",

            "technology": "#Technology 💻",

            "crypto": "#Crypto ₿",

            "trading": "#Trading 📈",

            "entertainment": "#Entertainment 🎬",

        }

    def clean(self, text):

        if not text:
            return ""

        return " ".join(text.split())

    def shorten(self, text, limit=350):

        text = self.clean(text)

        if len(text) <= limit:
            return text

        return text[:limit].rstrip() + "..."

    def format(self, article):

        title = self.clean(
            article.get("title", "")
        )

        summary = self.shorten(
            article.get("summary", "")
        )

        source = article.get(
            "source",
            "Global News",
        )

        link = article.get(
            "link",
            "",
        )

        category = article.get(
            "category",
            "world",
        ).lower()

        hashtag = self.hashtags.get(
            category,
            "#News",
        )

        date = datetime.utcnow().strftime(
            "%d %b %Y"
        )

        return (
            f"📰 <b>{title}</b>\n\n"
            f"{summary}\n\n"
            f"{hashtag}\n\n"
            f"🌐 <b>Source:</b> {source}\n"
            f"📅 <b>Date:</b> {date}\n\n"
            f"👉 <a href=\"{link}\">Read Full Story</a>\n\n"
            f"━━━━━━━━━━━━━━\n"
            f"🌍 <b>Global News Network</b>"
        )


formatter = Formatter()
