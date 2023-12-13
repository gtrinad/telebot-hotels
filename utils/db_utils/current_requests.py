from typing import Union

from config_data.config import USER_DATABASE
from database.pw_db import CurrentRequests


def get_current_requests(chat_id: int, column: str) -> Union[str, int]:
    """
    Функция возвращает значения колонок из таблицы CurrentRequests "telebot_db".
    """

    row = CurrentRequests.get_or_none(CurrentRequests.chat_id == chat_id)
    USER_DATABASE.close()

    return getattr(row, column) if row and hasattr(row, column) else "0"


def set_current_requests(chat_id: int, default: bool = False, **kwargs) -> None:
    """
    Функция с переданным параметром default=True устанавливает
    в таблице CurrentRequests "telebot_db" дефолтные значения.
    Без default записывает в колонки таблицы переданные значения.
    """

    with USER_DATABASE.atomic():
        if default:
            # Удаляем текущую запись для чата и устанавливаем дефолтные значения
            CurrentRequests.delete().where(CurrentRequests.chat_id == chat_id).execute()

        defaults = {
            "chat_id": chat_id,
            "current_command": "0",
            "destination_id": 0,
            "hotels_count": 0,
            "images_count": 0,
            "check_in": "0",
            "check_out": "0",
            "price_min": 0,
            "price_max": 0,
            "distance_min": 0,
            "distance_max": 100
        }

        row, _ = CurrentRequests.get_or_create(chat_id=chat_id, defaults=defaults)

        for key, value in kwargs.items():
            if hasattr(row, key):
                setattr(row, key, value)

        row.save()
