from typing import List

from user_api.database import db


async def connect_to_database(conn_string: str, models: List):
    await db.connect(conn_string, models)


