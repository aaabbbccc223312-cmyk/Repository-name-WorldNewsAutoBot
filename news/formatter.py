"""
news/formatter.py

Professional Telegram News Formatter
"""

import html


class NewsFormatter:

    HASHTAGS = {
        "world": "#WorldNews 🌍",
        "sports": "#Sports ⚽",
        "business": "#Business 💼",
        "technology": "#Technology 💻",
        "trading": "#Trading 📈",
    }

    MAX_SUMMARY = 350

    def shorten(self, text):

        if not text:
            return ""

        text = " ".join(text.split())

        if len(text) <= self.MAX_SUMMARY:
            return text

        return text[: self.MAX_SUMMARY].rstrip() + "..."

    def format(self, article):

        title = html.escape(
            article.get(
                "title",
                "No title",
            )
        )

        summary = html.escape(
            self.shorten(
                article.get(
                    "summary",
                    "",
                )
            )
        )

        source = html.escape(
            article.get(
                "source",
                "Unknown",
            )
        )

        category = (
            article.get(
                "category",
                "world",
            )
            .lower()
        )

        hashtag = self.HASHTAGS.get(
            category,
            "#News 📰",
        )

        link = article.get(
            "link",
            "",
        )

        message = (
            f"📰 <b>{title}</b>\n\n"
            f"{summary}\n\n"
            f"📌 <b>Source:</b> {source}\n"
            f"{hashtag}\n\n"
            f'🔗 <a href="{link}">Read Full Story</a>'
        )

        if len(message) > 1024:

            allowed = (
                1024
                - (
                    len(message)
                    - len(summary)
                )
                - 3
            )

            summary = summary[:allowed] + "..."

            message = (
                f"📰 <b>{title}</b>\n\n"
                f"{summary}\n\n"
                f"📌 <b>Source:</b> {source}\n"
                f"{hashtag}\n\n"
                f'🔗 <a href="{link}">Read Full Story</a>'
            )

        return message


formatter = NewsFormatter()
