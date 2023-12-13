import os
from pathlib import Path
from typing import Tuple

from dotenv import find_dotenv, load_dotenv
from peewee import SqliteDatabase
from pydantic import BaseSettings, SecretStr, StrictStr


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()


class BotConfig(BaseSettings):
    BOT_TOKEN: SecretStr = os.getenv(key="BOT_TOKEN", default=None)


class RapidAPIConfig(BaseSettings):
    API_HOST: StrictStr = os.getenv(key="RAPID_API_HOST", default=None)
    API_KEY: SecretStr = os.getenv(key="RAPID_API_KEY", default=None)


DEFAULT_COMMANDS: Tuple = (
    ("start", "Запустить бота."),
    ("help", "Вывести справку."),
    ("low", "Узнать топ самых дешёвых отелей в городе."),
    ("high", "Узнать топ самых дорогих отелей в городе."),
    (
        "custom",
        "Узнать топ отелей, наиболее подходящих по цене и расстоянию от центра города.",
    ),
    ("history", "Узнать историю поиска отелей."),
    ("cancel", "Завершить команду."),
)

DATABASE_FILE = "telebot_db.db"
USER_DATABASE: SqliteDatabase = SqliteDatabase(database=DATABASE_FILE)

DATA_HISTORY_FILE = "history.pickle"
NUMBER_HISTORY: int = 10
MAX_IMAGES_TO_SAVE: int = 10
DATA_HISTORY_PATH = Path(DATA_HISTORY_FILE).absolute()
