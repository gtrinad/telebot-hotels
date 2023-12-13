import telebot
from loguru import logger
from telebot.types import CallbackQuery, Message

from bot_loader import bot
from handlers.default_handlers.history import send_character_page
from handlers.default_handlers.in_out import from_date
from keyboards.other.calendar import calendar_date_from, calendar_date_to
from keyboards.reply.common_markup import (
    markup_choice_date_from,
    markup_from_cancel,
    markup_choice_date_to,
    markup_to_cancel,
)
from utils.db_utils.cities import get_cities
from utils.db_utils.current_requests import set_current_requests, get_current_requests
from utils.db_utils.state import set_state
from utils.misc.calendar_call import calendar_call


@logger.catch
def calendar_calldata(call: CallbackQuery) -> None:
    """
    Функция обрабатывает нажатия кнопок календаря, выбора города.
    """

    call_data: str = call.data
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id
    message: Message = call.message

    def delete_message():
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except telebot.apihelper.ApiTelegramException as error:
            logger.info(f"Ошибка - {error}")

    if call_data.startswith(calendar_date_from.prefix):
        text_choice: str = "Вы выбрали дату въезда:"
        calendar_call(
            call=call,
            sep=calendar_date_from.sep,
            text_choice=text_choice,
            markup_day=markup_choice_date_from(),
            markup_cancel=markup_from_cancel(),
            edit_column="check_in",
        )

    elif call_data.startswith(calendar_date_to.prefix):
        text_choice: str = "Вы выбрали дату выезда:"
        calendar_call(
            call=call,
            sep=calendar_date_to.sep,
            text_choice=text_choice,
            markup_day=markup_choice_date_to(),
            markup_cancel=markup_to_cancel(),
            edit_column="check_out",
        )

    elif call_data.startswith("id"):
        delete_message()

        command, city_id = call_data.split()
        city_id: int = int(city_id)

        result: str = get_cities(destination_id=city_id, column="name")
        bot.send_message(chat_id=chat_id, text=f"Вы выбрали:\n{result}")
        set_current_requests(chat_id=chat_id, destination_id=city_id)
        if get_current_requests(chat_id=chat_id, column="current_command") == "custom":
            set_state(chat_id=chat_id, states="price_min")
            bot.send_message(chat_id=chat_id, text="Введите желаемую минимальную стоимость за ночь, (USD):")
        else:
            set_state(chat_id=chat_id, states="date_from")
            from_date(message=message)

    else:
        # "final"
        delete_message()

        *info_all, command, city_id = call_data.split()
        send_character_page(message=message, command=command, city_id=int(city_id))
