import telebot
from loguru import logger
from telebot.types import CallbackQuery, Message

from bot_loader import bot
from handlers.default_handlers.main_commands import send_lowprice, send_highprice, send_custom, cancel_command
from utils.db_utils.current_requests import get_current_requests
from utils.db_utils.state import set_state


@logger.catch
def cities_call(call: CallbackQuery) -> None:
    """
    Функция обрабатывает нажатия на кнопки выбора города.
    """

    call_data: str = call.data
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id
    message: Message = call.message

    try:
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id)
    except telebot.apihelper.ApiTelegramException as error:
        logger.info(f"Ошибка - {error}")

    response_messages = {
        "city_yes": "Вы выбрали 'Да'",
        "city_no": "Вы выбрали 'Нет'",
    }

    bot.send_message(chat_id=chat_id, text=response_messages.get(call_data, "Неизвестная команда"))

    if call_data == "city_yes":
        set_state(chat_id=chat_id, states="city")
        current_command = get_current_requests(chat_id=chat_id, column="current_command")
        command_mapping = {
            "low": send_lowprice,
            "high": send_highprice,
            "custom": send_custom,
        }

        handler_function = command_mapping.get(current_command)
        if handler_function:
            handler_function(message=message)
        else:
            logger.error(f"Неизвестная команда: {current_command}")
    elif call_data == "city_no":
        cancel_command(message=message)
