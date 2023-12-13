from typing import List

from loguru import logger
from telebot.types import Message

from bot_loader import bot
from handlers.default_handlers.in_out import from_date
from utils.db_utils.current_requests import get_current_requests, set_current_requests
from utils.db_utils.state import set_state, get_state


def handle_numeric_input(
    chat_id: int,
    text: str,
    current_state: str,
    next_state: str,
    success_messages: List,
    error_message: str,
    success_callback: callable = None
) -> None:
    logger.info(f"В чате - {chat_id} пользователь выполняет {current_state}")
    if text.isdigit():
        value = int(text)
        min_value = get_current_requests(chat_id=chat_id, column=f"{current_state[:-4]}_min")
        if current_state == "distance_min":
            if value >= 0 and value >= min_value:
                for success_message in success_messages:
                    bot.send_message(chat_id=chat_id, text=success_message)
                set_current_requests(chat_id=chat_id, **{current_state: value})
                set_state(chat_id=chat_id, states=next_state)
                if success_callback:
                    success_callback()
            else:
                bot.send_message(chat_id=chat_id, text=error_message)
        else:
            if value > 0 and value > min_value:
                for success_message in success_messages:
                    bot.send_message(chat_id=chat_id, text=success_message)
                set_current_requests(chat_id=chat_id, **{current_state: value})
                set_state(chat_id=chat_id, states=next_state)
                if success_callback:
                    success_callback()
            else:
                bot.send_message(chat_id=chat_id, text=error_message)
    else:
        bot.send_message(chat_id=chat_id, text=error_message)


@bot.message_handler(func=lambda message: "distance_max" == get_state(chat_id=message.chat.id, column="states"))
@logger.catch
def max_distance_choice(message: Message) -> None:
    chat_id: int = message.chat.id
    text: str = message.text
    handle_numeric_input(
        chat_id=chat_id,
        text=text,
        current_state="distance_max",
        next_state="date_from",
        success_messages=[f"Выбранный диапазон расстояния "
                          f"{get_current_requests(chat_id=chat_id, column='distance_min')} - {text} км."],
        error_message=f"Ошибка, введите число больше, "
                      f"чем минимальное: {get_current_requests(chat_id=chat_id, column='distance_min')}.",
        success_callback=lambda: from_date(message)
    )


@bot.message_handler(func=lambda message: "price_max" == get_state(chat_id=message.chat.id, column="states"))
@logger.catch
def max_price_choice(message: Message) -> None:
    chat_id: int = message.chat.id
    text: str = message.text
    handle_numeric_input(
        chat_id=chat_id,
        text=text,
        current_state="price_max",
        next_state="distance_min",
        success_messages=[
            f"Выбранный диапазон цен ${get_current_requests(chat_id=chat_id, column='price_min')} - {text}",
            f"Введите желаемое минимальное расстояние до центра города (км):"
        ],
        error_message=f"Ошибка, введите число больше, "
                      f"чем минимальное: {get_current_requests(chat_id=chat_id, column='price_min')}."
    )


@bot.message_handler(func=lambda message: "price_min" == get_state(chat_id=message.chat.id, column="states"))
@logger.catch
def min_price_choice(message: Message) -> None:
    chat_id: int = message.chat.id
    handle_numeric_input(
        chat_id=chat_id,
        text=message.text,
        current_state="price_min",
        next_state="price_max",
        success_messages=["Введите желаемую максимальную стоимость за ночь, (USD):"],
        error_message="Ошибка, введите число больше 0"
    )


@bot.message_handler(func=lambda message: "distance_min" == get_state(chat_id=message.chat.id, column="states"))
@logger.catch
def min_distance_choice(message: Message) -> None:
    chat_id: int = message.chat.id
    handle_numeric_input(
        chat_id=chat_id,
        text=message.text,
        current_state="distance_min",
        next_state="distance_max",
        success_messages=["Введите желаемое максимальное расстояние до центра города (км):"],
        error_message="Ошибка, введите число больше или равно 0"
    )
