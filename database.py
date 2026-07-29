import aiosqlite
from config import DATABASE_PATH


CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS posted_news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    source TEXT,
    url TEXT,
    published TEXT,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(CREATE_TABLE)
        await db.commit()


async def is_posted(article_id: str) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT 1 FROM posted_news WHERE article_id = ?",
            (article_id,)
        )
        row = await cursor.fetchone()
        return row is not None


async def save_post(
    article_id: str,
    title: str,
    source: str,
    url: str,
    published: str
):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO posted_news
            (article_id, title, source, url, published)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                article_id,
                title,
                source,
                url,
                published
            )
        )
        await db.commit()
