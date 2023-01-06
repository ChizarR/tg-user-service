from fastapi import FastAPI

from user_api.config import Config
from user_api.helpers import startup, shutdown
from user_api.routes import UserRouter
from user_api.utils.logger import get_logger


log = get_logger("user-api", Config.ENV)


app = FastAPI()

user_router = UserRouter(log)
app.include_router(user_router.router)


@app.on_event("startup")
async def on_startup():
    await startup.connect_to_database(Config.CONNECTION_STRING, Config.MODELS)


@app.on_event("shutdown")
async def on_shutdown():
    await shutdown.close_database_connection()
