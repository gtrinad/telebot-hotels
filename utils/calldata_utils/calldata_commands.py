from typing import Dict

import telebot
from loguru import logger
from telebot.types import CallbackQuery, Message

from bot_loader import bot
from handlers.default_handlers.history import send_history
from handlers.default_handlers.main_commands import send_lowprice, send_highprice, send_custom


@logger.catch
def commands_call(call: CallbackQuery) -> None:
    """
    Функция обрабатывает нажатия кнопок от выбора команд.
    """

    call_data: str = call.data
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id
    message: Message = call.message

    try:
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id)
    except telebot.apihelper.ApiTelegramException as error:
        logger.info(f"Ошибка - {error}")

    bot.send_message(chat_id=chat_id, text=f"Вы выбрали /{call_data}")

    commands_mapping: Dict = {
        "low": send_lowprice,
        "high": send_highprice,
        "custom": send_custom,
        "history": send_history,
    }

    handler = commands_mapping.get(call_data)
    if handler:
        handler(message=message)
