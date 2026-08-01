import os

import aiosqlite

from config import DATABASE_PATH


db_folder = os.path.dirname(
    DATABASE_PATH
)

if db_folder:

    os.makedirs(
        db_folder,
        exist_ok=True,
    )


async def connect():

    db = await aiosqlite.connect(
        DATABASE_PATH
    )

    db.row_factory = aiosqlite.Row

    return db


async def init_db():

    db = await connect()

    try:

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users(

                user_id INTEGER PRIMARY KEY,

                username TEXT,

                first_name TEXT,

                joined_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS channels(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE,

                category TEXT,

                enabled INTEGER
                DEFAULT 1,

                created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS rss_sources(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                category TEXT,

                feed_url TEXT UNIQUE,

                enabled INTEGER
                DEFAULT 1

            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS posted_news(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                channel_username TEXT,

                article_id TEXT,

                title TEXT,

                posted_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

                UNIQUE(

                    channel_username,

                    article_id

                )

            )
            """
        )

        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS settings(

                key TEXT PRIMARY KEY,

                value TEXT

            )
            """
        )

        await db.commit()

    finally:

        await db.close()
async def save_user(

    user,

):

    db = await connect()

    try:

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

    finally:

        await db.close()


async def total_users():

    db = await connect()

    try:

        cursor = await db.execute(
            "SELECT COUNT(*) FROM users"
        )

        row = await cursor.fetchone()

        return row[0]

    finally:

        await db.close()


async def add_channel(

    username,

    category="world",

):

    db = await connect()

    try:

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

    finally:

        await db.close()


async def remove_channel(

    username,

):

    db = await connect()

    try:

        await db.execute(
            """
            DELETE FROM channels

            WHERE username=?

            """,
            (
                username,
            ),
        )

        await db.commit()

    finally:

        await db.close()
async def pause_channel(

    username,

):

    db = await connect()

    try:

        await db.execute(
            """
            UPDATE channels

            SET enabled=0

            WHERE username=?

            """,
            (
                username,
            ),
        )

        await db.commit()

    finally:

        await db.close()


async def resume_channel(

    username,

):

    db = await connect()

    try:

        await db.execute(
            """
            UPDATE channels

            SET enabled=1

            WHERE username=?

            """,
            (
                username,
            ),
        )

        await db.commit()

    finally:

        await db.close()


async def get_channels():

    db = await connect()

    try:

        cursor = await db.execute(
            """
            SELECT *

            FROM channels

            WHERE enabled=1

            ORDER BY username

            """
        )

        return await cursor.fetchall()

    finally:

        await db.close()


async def total_channels():

    db = await connect()

    try:

        cursor = await db.execute(
            """
            SELECT COUNT(*)

            FROM channels

            WHERE enabled=1

            """
        )

        row = await cursor.fetchone()

        return row[0]

    finally:

        await db.close()
async def has_posted(

    channel_username,

    article_id,

):

    db = await connect()

    try:

        cursor = await db.execute(
            """
            SELECT 1

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

        return await cursor.fetchone() is not None

    finally:

        await db.close()


async def save_post(

    channel_username,

    article_id,

    title,

):

    db = await connect()

    try:

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

    finally:

        await db.close()
async def get_all_rss():

    db = await connect()

    try:

        cursor = await db.execute(
            """
            SELECT *

            FROM rss_sources

            WHERE enabled=1

            ORDER BY category,id

            """
        )

        return await cursor.fetchall()

    finally:

        await db.close()
