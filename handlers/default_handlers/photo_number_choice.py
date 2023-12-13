from loguru import logger
from telebot.types import Message

from bot_loader import bot
from utils.db_utils.current_requests import get_current_requests, set_current_requests
from utils.db_utils.state import get_state, set_state
from utils.misc.hotels_requests import request_hotels
from utils.misc.request_hotels_custom import request_hotels_custom


def get_photos_word(number: int) -> str:
    """
    Получение правильной формы слова "фотография" в зависимости от числа.
    """

    forms = [
        "Будет показана {number} фотография.",
        "Будут показаны {number} фотографии.",
        "Будут показаны {number} фотографий."
    ]
    remainder_100 = number % 100

    if remainder_100 in {11, 12, 13, 14}:
        return forms[2]
    else:
        remainder_10 = remainder_100 % 10
        if remainder_10 == 1:
            return forms[0]
        elif 1 < remainder_10 < 5:
            return forms[1]
        else:
            return forms[2]


@logger.catch
def handle_photo_number_input(chat_id: int, command: str, text: str) -> None:
    """
    Обработка ввода количества показываемых фотографий.
    """

    logger.info(f"В чате - {chat_id} пользователь выбирает кол-во показываемых фото.")

    set_state(chat_id=chat_id, states="send_result")
    max_images = 10

    if text.isdigit():
        max_images = min(max_images, max(1, int(text)))
        photos_word = get_photos_word(number=max_images)
        bot.send_message(chat_id=chat_id, text=photos_word.format(number=max_images))
    else:
        bot.send_message(chat_id=chat_id, text=f"Некорректный ввод.\nБудут показаны не более {max_images} фотографий.")

    set_current_requests(chat_id=chat_id, images_count=max_images)

    if command == "low":
        request_hotels(chat_id=chat_id, sort="PRICE_LOW_TO_HIGH")
    elif command == "high":
        request_hotels(chat_id=chat_id, sort="PRICE_HIGH_TO_LOW")
    elif command == "custom":
        request_hotels_custom(chat_id=chat_id)


@bot.message_handler(func=lambda message: "choice_photo_number" == get_state(chat_id=message.chat.id, column="states"))
def choice_photo_number(message: Message) -> None:
    """
    Функция-хэндлер устанавливает количество показываемых фотографий.
    """

    chat_id: int = message.chat.id
    command = get_current_requests(chat_id=chat_id, column="current_command")
    handle_photo_number_input(chat_id=chat_id, command=command, text=message.text)
