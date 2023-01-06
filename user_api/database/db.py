from typing import List

from tortoise import Tortoise


# TODO: remove generate schemas, connect to existing db
async def connect(connection_string: str, models: List):
    """Try to connect to database and generate schemas if schemas do not exists"""
    await Tortoise.init(db_url=connection_string, modules={"models": models})
    await Tortoise.generate_schemas(safe=True)


async def close_connection():
    """Use this function to close connection on application shutdown"""
    await Tortoise.close_connections()
