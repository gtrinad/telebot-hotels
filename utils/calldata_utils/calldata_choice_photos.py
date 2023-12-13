import telebot
from loguru import logger
from telebot.types import CallbackQuery

from bot_loader import bot
from utils.db_utils.current_requests import set_current_requests, get_current_requests
from utils.db_utils.state import set_state
from utils.misc.hotels_requests import request_hotels
from utils.misc.request_hotels_custom import request_hotels_custom


@logger.catch
def calldata_choice_photos(call: CallbackQuery) -> None:
    """
    Функция обрабатывает кнопки выбора показа фото
    """

    call_data: str = call.data
    chat_id: int = call.message.chat.id
    message_id: int = call.message.message_id

    try:
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id)
    except telebot.apihelper.ApiTelegramException as error:
        logger.info(f"Ошибка - {error}")

    actions = {
        "choice_photo_yes": handle_choice_photo_yes,
        "choice_photo_no": handle_choice_photo_no,
    }

    handler = actions.get(call_data)
    if handler:
        handler(chat_id=chat_id)


def handle_choice_photo_yes(chat_id: int) -> None:
    bot.send_message(
        chat_id=chat_id,
        text="Вы выбрали 'Да'.\nНапишите количество фотографий для показа (1-10):",
    )
    set_state(chat_id=chat_id, states="choice_photo_number")


def handle_choice_photo_no(chat_id: int) -> None:
    bot.send_message(
        chat_id=chat_id, text="Вы выбрали 'Нет'.\nФотографии показываться не будут."
    )
    set_current_requests(chat_id=chat_id, images_count=0)
    set_state(chat_id=chat_id, states="send_result")
    command = get_current_requests(chat_id=chat_id, column="current_command")
    if command == "low":
        request_hotels(chat_id=chat_id, sort="PRICE_LOW_TO_HIGH")
    elif command == "high":
        request_hotels(chat_id=chat_id, sort="PRICE_HIGH_TO_LOW")
    elif command == "custom":
        request_hotels_custom(chat_id=chat_id)
