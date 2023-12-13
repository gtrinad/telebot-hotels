from typing import Tuple

from telebot.types import CallbackQuery, Message

from bot_loader import bot
from handlers.default_handlers.history import send_character_page, send_history
from keyboards.other.calendar import calendar_date_from, calendar_date_to
from utils.calldata_utils.calldata_choice_history import calldata_choice_history
from utils.calldata_utils.calldata_choice_photos import calldata_choice_photos
from utils.calldata_utils.calldata_cities import cities_call
from utils.calldata_utils.calldata_commands import commands_call
from utils.calldata_utils.calldata_dates import calldata_dates
from utils.calldata_utils.calldata_prefix import calendar_calldata


COMMANDS: Tuple = ("low", "high", "custom", "history")
USER_DATES: Tuple = (
    "date_from_right", "date_from_change", "date_from_cancel", "date_from_continue",
    "date_to_right", "date_to_change", "date_to_cancel", "date_to_continue"
)
CHOICE_PHOTOS: Tuple = ("choice_photo_yes", "choice_photo_no")
HISTORY: Tuple = ("wol", "hgih", "motsuc", "close_history", "close_hotels")
CITIES: Tuple = ("city_yes", "city_no")
PREFIX: Tuple = (calendar_date_from.prefix, calendar_date_to.prefix, "id", "final")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call: CallbackQuery) -> None:
    """
    Функция обрабатывает нажатия на кнопки пользователем и вызывает нужную функцию.
    """

    call_data: str = call.data
    message: Message = call.message

    if call_data in COMMANDS:
        commands_call(call=call)
    elif call_data in CITIES:
        cities_call(call=call)
    elif call_data.startswith(PREFIX):
        calendar_calldata(call=call)
    elif call_data in USER_DATES:
        calldata_dates(call=call)
    elif call_data in CHOICE_PHOTOS:
        calldata_choice_photos(call=call)

    elif call_data in HISTORY:
        calldata_choice_history(call=call)

    elif call_data.startswith("character#"):
        page = int(call_data.split("#")[1])
        send_character_page(message=message, page=page)
    else:
        # "back"
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        send_history(message=message)
