import os
import aiosqlite

from config import DATABASE_PATH


async def init_db():
    os.makedirs("data", exist_ok=True)

    async with aiosqlite.connect(DATABASE_PATH) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS posted_articles(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id TEXT UNIQUE,
            title TEXT,
            image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.commit()


async def article_exists(article_id):

    async with aiosqlite.connect(DATABASE_PATH) as db:

        cursor = await db.execute(
            "SELECT 1 FROM posted_articles WHERE article_id=?",
            (article_id,),
        )

        return await cursor.fetchone() is not None


async def save_article(article_id, title, image):

    async with aiosqlite.connect(DATABASE_PATH) as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO posted_articles
            (article_id,title,image)
            VALUES(?,?,?)
            """,
            (article_id, title, image),
        )

        await db.commit()


async def save_user(user):

    async with aiosqlite.connect(DATABASE_PATH) as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO users
            (user_id,username,first_name)
            VALUES(?,?,?)
            """,
            (
                user.id,
                user.username,
                user.first_name,
            ),
        )

        await db.commit()
