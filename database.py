import os
import aiosqlite
from config import DATABASE_PATH

os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)


class Database:

    def __init__(self):
        self.db_path = DATABASE_PATH

    async def connect(self):
        return await aiosqlite.connect(self.db_path)

    async def init(self):

        async with await self.connect() as db:

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
                enabled INTEGER DEFAULT 1,
                category TEXT DEFAULT 'general',
                rss_feed TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Posted Articles
            await db.execute("""
            CREATE TABLE IF NOT EXISTS posted_news(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id INTEGER,
                article_id TEXT,
                posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(channel_id, article_id)
            )
            """)

            # Settings
            await db.execute("""
            CREATE TABLE IF NOT EXISTS settings(
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """)

            await db.commit()

    # ---------------------------------------------------
    # USERS
    # ---------------------------------------------------

    async def save_user(self, user):

        async with await self.connect() as db:

            await db.execute("""
            INSERT OR IGNORE INTO users(
                user_id,
                username,
                first_name
            )
            VALUES(?,?,?)
            """, (
                user.id,
                user.username,
                user.first_name,
            ))

            await db.commit()

    async def total_users(self):

        async with await self.connect() as db:

            cur = await db.execute(
                "SELECT COUNT(*) FROM users"
            )

            row = await cur.fetchone()

            return row[0]

    # ---------------------------------------------------
    # CHANNELS
    # ---------------------------------------------------

    async def add_channel(
        self,
        username,
        category="general",
        rss_feed="",
    ):

        async with await self.connect() as db:

            await db.execute("""
            INSERT OR IGNORE INTO channels(
                username,
                category,
                rss_feed
            )
            VALUES(?,?,?)
            """, (
                username,
                category,
                rss_feed,
            ))

            await db.commit()

    async def remove_channel(self, username):

        async with await self.connect() as db:

            await db.execute(
                "DELETE FROM channels WHERE username=?",
                (username,),
            )

            await db.commit()

    async def pause_channel(self, username):

        async with await self.connect() as db:

            await db.execute(
                "UPDATE channels SET enabled=0 WHERE username=?",
                (username,),
            )

            await db.commit()

    async def resume_channel(self, username):

        async with await self.connect() as db:

            await db.execute(
                "UPDATE channels SET enabled=1 WHERE username=?",
                (username,),
            )

            await db.commit()

    async def get_channels(self):

        async with await self.connect() as db:

            cur = await db.execute("""
            SELECT
                id,
                username,
                category,
                rss_feed
            FROM channels
            WHERE enabled=1
            ORDER BY id
            """)

            rows = await cur.fetchall()

            return rows

    async def total_channels(self):

        async with await self.connect() as db:

            cur = await db.execute(
                "SELECT COUNT(*) FROM channels WHERE enabled=1"
            )

            row = await cur.fetchone()

            return row[0]

    # ---------------------------------------------------
    # POSTED ARTICLES
    # ---------------------------------------------------

    async def has_posted(
        self,
        channel_id,
        article_id,
    ):

        async with await self.connect() as db:

            cur = await db.execute("""
            SELECT id
            FROM posted_news
            WHERE channel_id=?
            AND article_id=?
            """, (
                channel_id,
                article_id,
            ))

            return await cur.fetchone() is not None

    async def save_post(
        self,
        channel_id,
        article_id,
    ):

        async with await self.connect() as db:

            await db.execute("""
            INSERT OR IGNORE INTO posted_news(
                channel_id,
                article_id
            )
            VALUES(?,?)
            """, (
                channel_id,
                article_id,
            ))

            await db.commit()

    async def total_posts(self):

        async with await self.connect() as db:

            cur = await db.execute(
                "SELECT COUNT(*) FROM posted_news"
            )

            row = await cur.fetchone()

            return row[0]


db = Database()
