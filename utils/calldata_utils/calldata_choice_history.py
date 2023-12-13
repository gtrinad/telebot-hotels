from loguru import logger
from telebot.types import CallbackQuery

from bot_loader import bot
from config_data.config import DEFAULT_COMMANDS
from handlers.default_handlers.history import send_history
from keyboards.reply.common_markup import markup_start
from keyboards.reply.history_markup import show_search_hotel
from utils.db_utils.state import set_state


@logger.catch
def calldata_choice_history(call: CallbackQuery) -> None:
    """
    Функция обрабатывает кнопки от выбора показа истории команд.
    """

    call_data: str = call.data
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id

    commands_mapping = {
        "wol": "low",
        "hgih": "high",
        "motsuc": "custom",
    }

    if call_data in commands_mapping:
        command = commands_mapping.get(call_data)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"Вы выбрали историю поиска '{command}'.\nВыберите один из вариантов ниже:",
            reply_markup=show_search_hotel(command=command, chat_id=chat_id),
        )
    elif call_data == "close_history":
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_message(
            chat_id=chat_id,
            text="История закрыта, желаете продолжить?\n" "Выберите команду:",
            reply_markup=markup_start(commands=DEFAULT_COMMANDS),
        )
        bot.send_message(chat_id=chat_id, text="Описание команд - /help")
        set_state(chat_id=chat_id, states="0")
    else:
        # "close_hotels"
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        send_history(message=call.message)
