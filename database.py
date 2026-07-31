import os
import aiosqlite

from config import DATABASE_PATH

# ==========================================================
# Ensure database directory exists
# ==========================================================

db_dir = os.path.dirname(DATABASE_PATH)

if db_dir:
    os.makedirs(db_dir, exist_ok=True)


# ==========================================================
# Initialize Database
# ==========================================================

async def init_db():

    async with aiosqlite.connect(DATABASE_PATH) as db:

        # ---------------- USERS ----------------

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ---------------- CHANNELS ----------------

        await db.execute("""
        CREATE TABLE IF NOT EXISTS channels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            enabled INTEGER DEFAULT 1,
            category TEXT DEFAULT 'general',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ---------------- POSTED NEWS ----------------

        await db.execute("""
        CREATE TABLE IF NOT EXISTS posted_news(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT NOT NULL,
            article_id TEXT NOT NULL,
            posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(channel, article_id)
        )
        """)

        await db.commit()


# ==========================================================
# USERS
# ==========================================================

async def save_user(user):

    async with aiosqlite.connect(DATABASE_PATH) as db:

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

    async with aiosqlite.connect(DATABASE_PATH) as db:

        cursor = await db.execute(
            "SELECT COUNT(*) FROM users"
        )

        row = await cursor.fetchone()

        return row[0]


# ==========================================================
# CHANNELS
# ==========================================================

async def add_channel(username, category="general"):

    async with aiosqlite.connect(DATABASE_PATH) as db:

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
                category,
            ),
        )

        await db.commit()


async def remove_channel(username):

    async with aiosqlite.connect(DATABASE_PATH) as db:

        await db.execute(
            "DELETE FROM channels WHERE username=?",
            (username,),
        )

        await db.commit()


async def pause_channel(username):

    async with aiosqlite.connect(DATABASE_PATH) as db:

        await db.execute(
            "UPDATE channels SET enabled=0 WHERE username=?",
            (username,),
        )

        await db.commit()


async def resume_channel(username):

    async with aiosqlite.connect(DATABASE_PATH) as db:

        await db.execute(
            "UPDATE channels SET enabled=1 WHERE username=?",
            (username,),
        )

        await db.commit()


async def get_channels():

    async with aiosqlite.connect(DATABASE_PATH) as db:

        cursor = await db.execute(
            """
            SELECT username
            FROM channels
            WHERE enabled=1
            ORDER BY id
            """
        )

        rows = await cursor.fetchall()

        return [row[0] for row in rows]


async def total_channels():

    async with aiosqlite.connect(DATABASE_PATH) as db:

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
# NEWS HISTORY
# ==========================================================

async def has_posted(channel, article_id):

    async with aiosqlite.connect(DATABASE_PATH) as db:

        cursor = await db.execute(
            """
            SELECT 1
            FROM posted_news
            WHERE channel=?
            AND article_id=?
            LIMIT 1
            """,
            (
                channel,
                article_id,
            ),
        )

        return await cursor.fetchone() is not None


async def save_post(channel, article_id):

    async with aiosqlite.connect(DATABASE_PATH) as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO posted_news(
                channel,
                article_id
            )
            VALUES(?,?)
            """,
            (
                channel,
                article_id,
            ),
        )

        await db.commit()


async def total_posts():

    async with aiosqlite.connect(DATABASE_PATH) as db:

        cursor = await db.execute(
            "SELECT COUNT(*) FROM posted_news"
        )

        row = await cursor.fetchone()

        return row[0]
