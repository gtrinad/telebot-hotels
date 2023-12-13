from typing import Union, Optional

from config_data.config import USER_DATABASE
from database.pw_db import UserStates


def get_state(chat_id: int, column: str) -> Optional[Union[str, int]]:
    """
    Функция возвращает значение состояния пользователя из таблицы UserStates "telebot_db".
    """

    try:
        row = UserStates.get_or_none(UserStates.chat_id == chat_id)
        return getattr(row, column) if row else None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def set_state(chat_id: int, states: Optional[str] = None, message_id: Optional[int] = None) -> None:
    """
    Функция устанавливает состояние пользователя в таблицу UserStates "telebot_db".
    """

    try:
        with USER_DATABASE.atomic():
            row, created = UserStates.get_or_create(chat_id=chat_id, defaults={"states": "0", "message_id": 0})

            if states is not None:
                row.states = states
            if message_id is not None:
                row.message_id = message_id

            row.save()
    except Exception as e:
        print(f"An error occurred: {e}")
