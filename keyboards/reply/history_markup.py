from typing import List, Dict

from loguru import logger
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_utils.cities import get_cities
from utils.db_utils.db_history import get_pickle


@logger.catch
def show_commands(commands: List) -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру выбора истории поиска.
    """

    logger.info("Выбор истории поиска.")
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons: List[InlineKeyboardButton] = [
        InlineKeyboardButton(text=f"{index}", callback_data=index[::-1])
        for index in commands
    ]
    buttons.append(InlineKeyboardButton(text="Закрыть историю", callback_data="close_history"))
    markup.add(*buttons)
    return markup


@logger.catch
def show_search_hotel(command: str, chat_id: int) -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру выбора истории поиска команды.
    """

    data: Dict = get_pickle(chat_id)

    logger.info("Выбор истории поиска команды.")
    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1)
    buttons: List[InlineKeyboardButton] = [
        InlineKeyboardButton(text=f'{data[command][city_id][0]} {get_cities(city_id, "name")}',
                             callback_data=f"final {command} {city_id}")
        for city_id in data[command]
    ]
    buttons.append(InlineKeyboardButton(text="Закрыть просмотр", callback_data="close_hotels"))
    markup.add(*buttons)
    return markup
