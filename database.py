import os
import aiosqlite

from config import DATABASE_PATH


# ==========================================
# Ensure database folder exists
# ==========================================

os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)


# ==========================================
# Database Initialization
# ==========================================

async def init_db():

    async with aiosqlite.connect(DATABASE_PATH) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS channels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            enabled INTEGER DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS posted_news(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT,
            article_id TEXT,
            posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(channel, article_id)
        )
        """)

        await db.commit()


# ==========================================
# USERS
# ==========================================

async def save_user(user):

    async with aiosqlite.connect(DATABASE_PATH) as db:

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


async def total_users():

    async with aiosqlite.connect(DATABASE_PATH) as db:

        cursor = await db.execute(
            "SELECT COUNT(*) FROM users"
        )

        row = await cursor.fetchone()

        return row[0]


# ==========================================
# CHANNELS
# ==========================================

async def add_channel(username):

    async with aiosqlite.connect(DATABASE_PATH) as db:

        await db.execute("""
        INSERT OR IGNORE INTO channels(username)
        VALUES(?)
        """, (username,))

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

        cursor = await db.execute("""
        SELECT username
        FROM channels
        WHERE enabled=1
        ORDER BY id
        """)

        rows = await cursor.fetchall()

        return [row[0] for row in rows]


# ==========================================
# POSTED ARTICLES
# ==========================================

async def has_posted(channel, article_id):

    async with aiosqlite.connect(DATABASE_PATH) as db:

        cursor = await db.execute("""
        SELECT 1
        FROM posted_news
        WHERE channel=?
        AND article_id=?
        LIMIT 1
        """, (
            channel,
            article_id,
        ))

        return await cursor.fetchone() is not None


async def save_post(channel, article_id):

    async with aiosqlite.connect(DATABASE_PATH) as db:

        await db.execute("""
        INSERT OR IGNORE INTO posted_news(
            channel,
            article_id
        )
        VALUES(?,?)
        """, (
            channel,
            article_id,
        ))

        await db.commit()


# ==========================================
# STATISTICS
# ==========================================

async def total_channels():

    async with aiosqlite.connect(DATABASE_PATH) as db:

        cursor = await db.execute(
            "SELECT COUNT(*) FROM channels WHERE enabled=1"
        )

        row = await cursor.fetchone()

        return row[0]


async def total_posts():

    async with aiosqlite.connect(DATABASE_PATH) as db:

        cursor = await db.execute(
            "SELECT COUNT(*) FROM posted_news"
        )

        row = await cursor.fetchone()

        return row[0]
