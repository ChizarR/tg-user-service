from user_api.database import db


async def close_database_connection():
    await db.close_connection()
