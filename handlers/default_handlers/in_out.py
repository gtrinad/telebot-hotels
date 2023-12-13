from datetime import datetime

from loguru import logger
from telebot.types import Message

from bot_loader import bot
from keyboards.other.calendar import calendar, calendar_date_to, calendar_date_from
from utils.db_utils.state import set_state, get_state


@logger.catch
def send_date_message(chat_id: int, text: str, calendar_name: str) -> None:
    """
    Отправляет сообщение с календарем пользователю.
    """

    logger.info(f"В чате - {chat_id} пользователь получил календарь с текстом '{text}'")
    now = datetime.now()
    bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=calendar.create_calendar(
            name=calendar_name,
            year=now.year,
            month=now.month,
        ),
    )
    set_state(chat_id=chat_id, states="calendar_choice")


@bot.message_handler(
    func=lambda message: "date_to"
    in get_state(chat_id=message.chat.id, column="states")
)
def to_date(message: Message) -> None:
    """
    Функция-хендлер предлагает пользователю выбрать дату выезда.
    """

    send_date_message(
        chat_id=message.chat.id,
        text="Выберите дату выезда из гостиницы",
        calendar_name=calendar_date_to.prefix,
    )


@bot.message_handler(
    func=lambda message: "date_from"
    in get_state(chat_id=message.chat.id, column="states")
)
def from_date(message: Message) -> None:
    """
    Функция-хендлер предлагает пользователю выбрать дату заезда.
    """

    send_date_message(
        chat_id=message.chat.id,
        text="Выберите дату въезда в гостиницу",
        calendar_name=calendar_date_from.prefix,
    )
