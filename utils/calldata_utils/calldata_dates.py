import telebot
from loguru import logger
from telebot.types import CallbackQuery, Message

from bot_loader import bot
from handlers.default_handlers.in_out import to_date, from_date
from handlers.default_handlers.main_commands import cancel_command
from utils.db_utils.state import set_state
from utils.misc.check_dates import check_dates


@logger.catch
def calldata_dates(call: CallbackQuery) -> None:
    """
    Функция обрабатывает нажатие кнопок от выбора даты въезда и выезда.
    """

    call_data: str = call.data
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id
    message: Message = call.message

    try:
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id)
    except telebot.apihelper.ApiTelegramException as error:
        logger.info(f"Ошибка - {error}")

    if call_data.startswith("date_from"):
        handle_date_from(call_data=call_data, message=message)
    elif call_data.startswith("date_to"):
        handle_date_to(call_data=call_data, message=message)
    else:
        logger.warning(f"Unknown call_data: {call_data}")


def handle_date_from(call_data: str, message: Message) -> None:
    if call_data == "date_from_right":
        set_state(chat_id=message.chat.id, states="date_to")
        to_date(message=message)
    elif call_data == "date_from_change" or call_data == "date_from_continue":
        from_date(message=message)
    elif call_data == "date_from_cancel":
        cancel_command(message=message)


def handle_date_to(call_data: str, message: Message) -> None:
    if call_data == "date_to_right":
        check_dates(chat_id=message.chat.id)
    elif call_data == "date_to_change" or call_data == "date_to_continue":
        to_date(message=message)
    elif call_data == "date_to_cancel":
        cancel_command(message=message)
