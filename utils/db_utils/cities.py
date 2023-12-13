from typing import List

from peewee import IntegrityError

from config_data.config import USER_DATABASE
from database.pw_db import Cities


def add_cities(cities: List) -> None:
    """
    Функция записывает в таблицу Cities "telebot_db" найденные города.
    """

    with USER_DATABASE.atomic():
        for index in cities:
            try:
                row, created = Cities.get_or_create(
                    destination_id=index.get("destination_id"),
                    defaults={
                        "name": index.get("city_name"),
                        "latitude": index.get("latitude"),
                        "longitude": index.get("longitude"),
                    },
                )
            except IntegrityError:
                # Обработка случая, когда запись не существует
                pass


def get_cities(destination_id: int, column: str) -> str:
    """
    Функция возвращает из таблицы Cities "telebot_db" значения переданной колонки.
    """

    city = Cities.get_or_none(destination_id=destination_id)

    return getattr(city, column, "0") if city else "0"
