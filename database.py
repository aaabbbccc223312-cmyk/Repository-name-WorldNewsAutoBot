import os
import aiosqlite

from config import DATABASE_PATH

os.makedirs("data", exist_ok=True)


async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:

        # Users
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Channels
        await db.execute("""
        CREATE TABLE IF NOT EXISTS channels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Posted articles (per channel)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS posted_articles(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id TEXT,
            channel TEXT,
            title TEXT,
            url TEXT,
            image TEXT,
            posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(article_id, channel)
        )
        """)

        # Settings
        await db.execute("""
        CREATE TABLE IF NOT EXISTS settings(
            name TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        await db.commit()


# -------------------------
# USERS
# -------------------------

async def save_user(user):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO users
            (user_id, username, first_name)
            VALUES (?, ?, ?)
            """,
            (
                user.id,
                user.username,
                user.first_name,
            ),
        )
        await db.commit()


# -------------------------
# CHANNELS
# -------------------------

async def add_channel(username):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO channels(username)
            VALUES(?)
            """,
            (username,),
        )
        await db.commit()


async def remove_channel(username):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            DELETE FROM channels
            WHERE username=?
            """,
            (username,),
        )
        await db.commit()


async def get_channels():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            """
            SELECT username
            FROM channels
            WHERE active=1
            ORDER BY id
            """
        )
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def pause_channel(username):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            UPDATE channels
            SET active=0
            WHERE username=?
            """,
            (username,),
        )
        await db.commit()


async def resume_channel(username):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            UPDATE channels
            SET active=1
            WHERE username=?
            """,
            (username,),
        )
        await db.commit()


# -------------------------
# ARTICLES
# -------------------------

async def article_exists(article_id, channel):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            """
            SELECT 1
            FROM posted_articles
            WHERE article_id=?
            AND channel=?
            """,
            (
                article_id,
                channel,
            ),
        )
        return await cursor.fetchone() is not None


async def save_article(article_id, channel, title, url, image):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO posted_articles
            (article_id, channel, title, url, image)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                article_id,
                channel,
                title,
                url,
                image,
            ),
        )
        await db.commit()
