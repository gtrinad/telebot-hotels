from loguru import logger
from telebot.types import Message

from bot_loader import bot
from handlers.default_handlers.main_commands import cancel_command
from utils.db_utils.current_requests import get_current_requests
from utils.db_utils.state import get_state, set_state
from utils.misc.hotels_requests import request_hotels
from utils.misc.request_hotels_custom import request_hotels_custom


@bot.message_handler(
    func=lambda message: get_state(chat_id=message.chat.id, column="states")
    in {"choice_cities", "calendar_choice"}
)
@logger.catch
def send_city_or_calendar_outside(message: Message) -> None:
    """
    Функция обрабатывает сообщения для состояний choice_cities и calendar_choice.
    """

    state = get_state(chat_id=message.chat.id, column="states")
    if state == "choice_cities":
        bot.send_message(
            chat_id=message.chat.id,
            text="Пожалуйста, выберите город из предложенного списка.",
        )
        logger.info(
            f"В чате - {message.chat.id} пользователь {message.from_user.first_name} "
            f"получил сообщение, что следует выбрать город из предоставленного списка."
        )
    elif state == "calendar_choice":
        bot.send_message(
            chat_id=message.chat.id, text="Воспользуйтесь предложенным выбором."
        )
        logger.info(
            f"В чате - {message.chat.id} пользователь {message.from_user.first_name} "
            f"получил сообщение, что следует воспользоваться предложенным интерактивным календарём."
        )


@bot.message_handler(
    func=lambda message: get_state(chat_id=message.chat.id, column="states")
    == "choice_history"
)
@logger.catch
def send_choice_history(message: Message) -> None:
    """
    Функция перехватывает сообщения при работе пользователя с историей.
    """

    bot.send_message(
        chat_id=message.chat.id, text="Воспользуйтесь предложенным выбором."
    )
    logger.info(
        f"В чате - {message.chat.id} пользователь {message.from_user.first_name} "
        f"получил предупреждение, что следует воспользоваться предложенным выбором истории поиска."
    )


@bot.message_handler(
    func=lambda message: get_state(chat_id=message.chat.id, column="states")
    == "choice_not_cities"
)
@logger.catch
def send_not_city_outside(message: Message) -> None:
    """
    Функция обрабатывает сообщения для состояния choice_not_cities.
    """

    chat_id: int = message.chat.id
    message_id: int = get_state(chat_id=chat_id, column="message_id")
    user_input = message.text.lower()

    if user_input in {"да", "lf", "нуы", "yes"}:
        bot.send_message(chat_id=chat_id, text="Вы выбрали 'Да'")
    elif user_input in {"нет", "ytn", "тщ", "no"}:
        bot.send_message(chat_id=chat_id, text="Вы выбрали 'Нет'")
        cancel_command(message)
    else:
        bot.send_message(chat_id=chat_id, text="Выберите или напишите 'Да/Нет'")

    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id)
    logger.info(
        f"В чате - {message.chat.id} пользователь {message.from_user.first_name} "
        f"получил сообщение, что следует следовать инструкции по выбору города."
    )


@bot.message_handler(
    func=lambda message: get_state(chat_id=message.chat.id, column="states")
    == "images_choice"
)
@logger.catch
def send_choice_photo_outside(message: Message) -> None:
    """
    Функция обрабатывает сообщения для состояния images_choice.
    """

    chat_id: int = message.chat.id

    logger.info(
        f"В чате - {chat_id} пользователь {message.from_user.first_name} "
        f"выбирает кол-во фото для показа."
    )
    command: str = get_current_requests(chat_id=chat_id, column="current_command")
    message_id: int = get_state(chat_id=chat_id, column="message_id")
    user_input = message.text.lower()

    if user_input in {"да", "lf", "нуы", "yes"}:
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id)
        bot.send_message(
            chat_id=chat_id,
            text="Вы выбрали 'Да'.\nНапишите количество фотографий для показа (1-10):",
        )
        set_state(chat_id=chat_id, states="choice_photo_number")
    elif user_input in {"нет", "ytn", "тщ", "no"}:
        bot.send_message(
            chat_id=chat_id, text="Вы выбрали 'Нет'.\nФотографии показываться не будут."
        )
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id)
        set_state(chat_id=chat_id, states="send_result")
        if command == "low":
            request_hotels(chat_id=chat_id, sort="PRICE_LOW_TO_HIGH")
        elif command == "high":
            request_hotels(chat_id=chat_id, sort="PRICE_HIGH_TO_LOW")
        elif command == "custom":
            request_hotels_custom(chat_id=chat_id)
    else:
        bot.send_message(chat_id=chat_id, text="Выберите или напишите 'Да/Нет'")
        logger.info(
            f"В чате - {message.chat.id} пользователь {message.from_user.first_name} "
            f"получил сообщение, что следует следовать инструкции по выбору кол-ва фото."
        )
