# ==========================================================
# DATABASE.PY
# PART 1 OF 4
# ==========================================================

import os
import aiosqlite

from config import DATABASE_PATH


# ==========================================================
# CREATE DATABASE FOLDER
# ==========================================================

database_folder = os.path.dirname(DATABASE_PATH)

if database_folder:
    os.makedirs(database_folder, exist_ok=True)


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

async def connect():

    db = await aiosqlite.connect(DATABASE_PATH)

    db.row_factory = aiosqlite.Row

    return db


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

async def init_db():

    async with await connect() as db:

        # --------------------------------------
        # USERS
        # --------------------------------------

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(

            user_id INTEGER PRIMARY KEY,

            username TEXT,

            first_name TEXT,

            joined_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # --------------------------------------
        # CHANNELS
        # --------------------------------------

        await db.execute("""
        CREATE TABLE IF NOT EXISTS channels(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            category TEXT NOT NULL,

            enabled INTEGER DEFAULT 1,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # --------------------------------------
        # RSS SOURCES
        # --------------------------------------

        await db.execute("""
        CREATE TABLE IF NOT EXISTS rss_sources(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            category TEXT NOT NULL,

            feed_url TEXT UNIQUE NOT NULL,

            enabled INTEGER DEFAULT 1,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # --------------------------------------
        # POSTED NEWS
        # --------------------------------------

        await db.execute("""
        CREATE TABLE IF NOT EXISTS posted_news(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            channel_username TEXT NOT NULL,

            article_id TEXT NOT NULL,

            title TEXT,

            posted_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(channel_username, article_id)

        )
        """)

        # --------------------------------------
        # SETTINGS
        # --------------------------------------

        await db.execute("""
        CREATE TABLE IF NOT EXISTS settings(

            setting_key TEXT PRIMARY KEY,

            setting_value TEXT

        )
        """)

        await db.commit()


# ==========================================================
# USERS
# ==========================================================

async def save_user(user):

    async with await connect() as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO users(

                user_id,

                username,

                first_name

            )

            VALUES(?,?,?)

            """,
            (
                user.id,
                user.username,
                user.first_name,
            ),
        )

        await db.commit()


async def total_users():

    async with await connect() as db:

        cursor = await db.execute(
            "SELECT COUNT(*) FROM users"
        )

        row = await cursor.fetchone()

        return row[0]


# ==========================================================
# END OF PART 1
# ==========================================================


# ==========================================================
# >>> PASTE PART 2 BELOW THIS LINE <<<
# ==========================================================
# ==========================================================
# DATABASE.PY
# PART 2 OF 4
# ==========================================================

# ==========================================================
# CHANNELS
# ==========================================================

async def add_channel(
    username: str,
    category: str = "world",
):

    async with await connect() as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO channels(

                username,

                category

            )

            VALUES(?,?)

            """,
            (
                username,
                category.lower(),
            ),
        )

        await db.commit()


async def remove_channel(username: str):

    async with await connect() as db:

        await db.execute(
            """
            DELETE FROM channels
            WHERE username=?
            """,
            (username,),
        )

        await db.commit()


async def pause_channel(username: str):

    async with await connect() as db:

        await db.execute(
            """
            UPDATE channels

            SET enabled=0

            WHERE username=?
            """,
            (username,),
        )

        await db.commit()


async def resume_channel(username: str):

    async with await connect() as db:

        await db.execute(
            """
            UPDATE channels

            SET enabled=1

            WHERE username=?
            """,
            (username,),
        )

        await db.commit()


async def get_channels():

    async with await connect() as db:

        cursor = await db.execute(
            """
            SELECT username

            FROM channels

            WHERE enabled=1

            ORDER BY id
            """
        )

        rows = await cursor.fetchall()

        return [row["username"] for row in rows]


async def get_channels_with_category():

    async with await connect() as db:

        cursor = await db.execute(
            """
            SELECT *

            FROM channels

            WHERE enabled=1

            ORDER BY id
            """
        )

        return await cursor.fetchall()


async def total_channels():

    async with await connect() as db:

        cursor = await db.execute(
            """
            SELECT COUNT(*)

            FROM channels

            WHERE enabled=1
            """
        )

        row = await cursor.fetchone()

        return row[0]


# ==========================================================
# RSS SOURCES
# ==========================================================

async def add_rss(

    category: str,

    feed_url: str,

):

    async with await connect() as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO rss_sources(

                category,

                feed_url

            )

            VALUES(?,?)

            """,
            (
                category.lower(),
                feed_url,
            ),
        )

        await db.commit()


async def remove_rss(feed_url: str):

    async with await connect() as db:

        await db.execute(
            """
            DELETE FROM rss_sources

            WHERE feed_url=?
            """,
            (feed_url,),
        )

        await db.commit()


async def get_rss(category: str):

    async with await connect() as db:

        cursor = await db.execute(
            """
            SELECT feed_url

            FROM rss_sources

            WHERE enabled=1

            AND category=?

            ORDER BY id
            """,
            (
                category.lower(),
            ),
        )

        rows = await cursor.fetchall()

        return [row["feed_url"] for row in rows]


async def total_rss():

    async with await connect() as db:

        cursor = await db.execute(
            """
            SELECT COUNT(*)

            FROM rss_sources

            WHERE enabled=1
            """
        )

        row = await cursor.fetchone()

        return row[0]


# ==========================================================
# END OF PART 2
# ==========================================================


# ==========================================================
# >>> PASTE PART 3 BELOW THIS LINE <<<
# ==========================================================
# ==========================================================
# DATABASE.PY
# PART 3 OF 4
# ==========================================================

# ==========================================================
# POSTED NEWS
# ==========================================================

async def has_posted(
    channel_username: str,
    article_id: str,
):

    async with await connect() as db:

        cursor = await db.execute(
            """
            SELECT id

            FROM posted_news

            WHERE channel_username=?

            AND article_id=?

            LIMIT 1
            """,
            (
                channel_username,
                article_id,
            ),
        )

        row = await cursor.fetchone()

        return row is not None


async def save_post(
    channel_username: str,
    article_id: str,
    title: str,
):

    async with await connect() as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO posted_news(

                channel_username,

                article_id,

                title

            )

            VALUES(?,?,?)

            """,
            (
                channel_username,
                article_id,
                title,
            ),
        )

        await db.commit()


async def total_posts():

    async with await connect() as db:

        cursor = await db.execute(
            """
            SELECT COUNT(*)

            FROM posted_news
            """
        )

        row = await cursor.fetchone()

        return row[0]


async def clear_post_history():

    async with await connect() as db:

        await db.execute(
            """
            DELETE FROM posted_news
            """
        )

        await db.commit()


# ==========================================================
# SETTINGS
# ==========================================================

async def set_setting(
    key: str,
    value: str,
):

    async with await connect() as db:

        await db.execute(
            """
            INSERT INTO settings(

                setting_key,

                setting_value

            )

            VALUES(?,?)

            ON CONFLICT(setting_key)

            DO UPDATE SET

            setting_value=excluded.setting_value
            """,
            (
                key,
                value,
            ),
        )

        await db.commit()


async def get_setting(
    key: str,
    default=None,
):

    async with await connect() as db:

        cursor = await db.execute(
            """
            SELECT setting_value

            FROM settings

            WHERE setting_key=?

            LIMIT 1
            """,
            (key,),
        )

        row = await cursor.fetchone()

        if row:

            return row["setting_value"]

        return default


# ==========================================================
# END OF PART 3
# ==========================================================


# ==========================================================
# >>> PASTE PART 4 BELOW THIS LINE <<<
# ==========================================================
# ==========================================================
# DATABASE.PY
# PART 4 OF 4
# ==========================================================

# ==========================================================
# DEFAULT RSS SOURCES
# ==========================================================

DEFAULT_RSS = {

    "world": [

        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.reutersagency.com/feed/?best-topics=world",

    ],

    "football": [

        "https://feeds.bbci.co.uk/sport/football/rss.xml",

    ],

    "technology": [

        "https://techcrunch.com/feed/",

    ],

    "crypto": [

        "https://www.coindesk.com/arc/outboundfeeds/rss/",

    ],

    "business": [

        "https://feeds.bbci.co.uk/news/business/rss.xml",

    ],

}


# ==========================================================
# LOAD DEFAULT RSS
# ==========================================================

async def load_default_rss():

    for category, feeds in DEFAULT_RSS.items():

        for feed in feeds:

            await add_rss(category, feed)


# ==========================================================
# DATABASE HEALTH CHECK
# ==========================================================

async def database_health():

    try:

        async with await connect() as db:

            await db.execute("SELECT 1")

        return True

    except Exception:

        return False


# ==========================================================
# RESET DATABASE
# ==========================================================

async def clear_users():

    async with await connect() as db:

        await db.execute("DELETE FROM users")

        await db.commit()


async def clear_channels():

    async with await connect() as db:

        await db.execute("DELETE FROM channels")

        await db.commit()


async def clear_rss():

    async with await connect() as db:

        await db.execute("DELETE FROM rss_sources")

        await db.commit()


# ==========================================================
# STARTUP
# ==========================================================

async def startup_database():

    await init_db()

    await load_default_rss()


# ==========================================================
# END OF DATABASE
# ==========================================================
