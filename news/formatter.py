"""
news/formatter.py

Formats articles for Telegram.
"""

from datetime import datetime


class Formatter:

    def __init__(self):

        pass


    def clean(

        self,

        text,

    ):

        if not text:

            return ""

        return " ".join(

            text.split()

        )


    def format(

        self,

        article,

    ):

        title = self.clean(

            article.get(

                "title",

                "",

            )

        )

        summary = self.clean(

            article.get(

                "summary",

                "",

            )

        )
        source = article.get(

            "source",

            "News",

        )

        link = article.get(

            "link",

            "",

        )

        now = datetime.utcnow().strftime(

            "%d %b %Y"

        )

        text = (

            f"📰 <b>{title}</b>\n\n"

            f"{summary}\n\n"

            f"🌍 <b>Source:</b> {source}\n"

            f"📅 <b>Date:</b> {now}\n\n"

            f"🔗 {link}"

        )

        return text


formatter = Formatter()
