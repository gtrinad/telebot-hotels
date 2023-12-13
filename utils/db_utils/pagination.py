from typing import Tuple

from config_data.config import USER_DATABASE
from database.pw_db import HotelsPagination


def set_pagination(message_id: int, city_id: int, command: str) -> None:
    """
    Функция записывает в таблицу HotelsPagination "telebot_db" значения пагинации истории.
    """

    hotel_pagination, created = HotelsPagination.get_or_create(
        message_id=message_id, defaults={"command": command, "city_id": city_id}
    )

    if not created:
        hotel_pagination.command = command
        hotel_pagination.city_id = city_id
        hotel_pagination.save()

    USER_DATABASE.close()


def get_pagination(message_id: int) -> Tuple:
    """
    Функция возвращает из таблицы HotelsPagination "telebot_db" значения пагинации истории.
    """

    hotel_pagination = HotelsPagination.get_or_none(message_id=message_id)

    if hotel_pagination:
        USER_DATABASE.close()
        return hotel_pagination.command, hotel_pagination.city_id

    return "0", 0
