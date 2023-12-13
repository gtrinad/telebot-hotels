from typing import Dict, List

import telebot
from loguru import logger
from telebot.types import Message, InlineKeyboardMarkup
from telegram_bot_pagination import InlineKeyboardPaginator, InlineKeyboardButton

from bot_loader import bot
from keyboards.reply.history_markup import show_commands
from utils.db_utils.db_history import get_pickle
from utils.db_utils.pagination import get_pagination, set_pagination
from utils.db_utils.state import set_state, get_state


@bot.message_handler(commands=["history"])
@logger.catch
def send_history(message: Message) -> None:
    """
    Функция-хэндлер отправляет пользователю историю запросов.
    """

    chat_id: int = message.chat.id

    logger.info(f"В чате - {chat_id} пользователь {message.from_user.first_name} запустил команду /history")

    data: Dict = get_pickle(chat_id)
    if not data:
        bot.send_message(chat_id=chat_id, text="История поиска пуста.")
    else:
        markup: InlineKeyboardMarkup = show_commands(commands=list(data.keys()))
        bot.send_message(chat_id=chat_id, text="Выберите историю поиска, которую показать:", reply_markup=markup)
        set_state(chat_id=chat_id, states="choice_history")


@logger.catch
def send_character_page(message: Message, page: int = 1, command: str = None, city_id: int = None):
    """
    Функция предоставляет историю отелей пагинацией.
    """

    chat_id: int = message.chat.id

    logger.info(f"В чате - {chat_id} пользователь {message.from_user.first_name} получил историю отелей пагинацией.")

    command_pickle, city_id_pickle = get_pagination(message.id) if not command else (command, city_id)
    data: Dict = get_pickle(chat_id)
    hotels_pages: List = data[command_pickle][city_id_pickle][1:]

    paginator: InlineKeyboardPaginator = InlineKeyboardPaginator(
        page_count=len(hotels_pages),
        current_page=page,
        data_pattern="character#{page}"
    )
    paginator.add_after(InlineKeyboardButton("Закрыть", callback_data="back"))

    if command:
        current_message: Message = bot.send_message(
            chat_id=chat_id,
            text=hotels_pages[page - 1][0],
            reply_markup=paginator.markup,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        set_pagination(message_id=current_message.id, city_id=city_id, command=command)
        set_state(chat_id=chat_id, message_id=current_message.id)
    else:
        try:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=get_state(chat_id=chat_id, column="message_id"),
                text=hotels_pages[page - 1][0],
                reply_markup=paginator.markup,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )

        except telebot.apihelper.ApiTelegramException:
            pass
