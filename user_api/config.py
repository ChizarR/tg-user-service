import os


class Config:
    ENV = "DEV"

    CONNECTION_STRING = os.environ["CONNECTION_STRING"]
    MODELS = ["user_api.database.models"]


