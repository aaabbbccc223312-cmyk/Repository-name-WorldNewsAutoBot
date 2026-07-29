import aiosqlite
from pathlib import Path

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
    """
    Create the SQLite database and table if they don't exist.
    """

    db_path = Path(DATABASE_PATH)

    # Create parent folder only if using a nested path.
    if db_path.parent != Path("."):
        db_path.parent.mkdir(parents=True, exist_ok=True)

    async with aiosqlite.connect(str(db_path)) as db:
        await db.execute(CREATE_TABLE)
        await db.commit()


async def is_posted(article_id: str) -> bool:
    """
    Return True if the article has already been posted.
    """

    db_path = Path(DATABASE_PATH)

    async with aiosqlite.connect(str(db_path)) as db:
        cursor = await db.execute(
            """
            SELECT 1
            FROM posted_news
            WHERE article_id = ?
            LIMIT 1
            """,
            (article_id,),
        )

        row = await cursor.fetchone()

        return row is not None


async def save_post(
    article_id: str,
    title: str,
    source: str,
    url: str,
    published: str,
):
    """
    Save a posted article.
    """

    db_path = Path(DATABASE_PATH)

    async with aiosqlite.connect(str(db_path)) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO posted_news
            (
                article_id,
                title,
                source,
                url,
                published
            )
            VALUES
            (?, ?, ?, ?, ?)
            """,
            (
                article_id,
                title,
                source,
                url,
                published,
            ),
        )

        await db.commit()


async def total_posts() -> int:
    """
    Return the number of stored articles.
    """

    db_path = Path(DATABASE_PATH)

    async with aiosqlite.connect(str(db_path)) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM posted_news"
        )

        result = await cursor.fetchone()

        return result[0] if result else 0
