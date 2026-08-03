"""
news/formatter.py

Formats news into beautiful Telegram posts.
"""

import html


class NewsFormatter:

    def format(self, article):

        title = html.escape(
            article.get(
                "title",
                "Untitled",
            )
        )

        summary = html.escape(
            article.get(
                "summary",
                "",
            )
        )

        source = html.escape(
            article.get(
                "source",
                "News",
            )
        )

        link = article.get(
            "link",
            "",
        )

        category = article.get(
            "category",
            "world",
        ).lower()

        emojis = {
            "world": "🌍",
            "sports": "⚽",
            "business": "💼",
            "technology": "💻",
            "trading": "📈",
        }

        emoji = emojis.get(
            category,
            "📰",
        )

        if len(summary) > 300:
            summary = summary[:297] + "..."

        text = (
            f"{emoji} <b>{title}</b>\n\n"
            f"{summary}\n\n"
            f"📰 <b>Source:</b> {source}\n"
            f"🔗 <a href=\"{link}\">Read Full Story</a>"
        )

        return text


formatter = NewsFormatter()
