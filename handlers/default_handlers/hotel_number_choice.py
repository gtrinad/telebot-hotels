from loguru import logger
from telebot.types import Message

from bot_loader import bot
from keyboards.reply.common_markup import markup_choice_photo
from utils.db_utils.current_requests import set_current_requests
from utils.db_utils.state import get_state, set_state


def get_hotels_word(number: int) -> str:
    """
    Получение правильной формы слова "отель" в зависимости от числа.
    """

    forms = [
        "Будет показан {number} отель.",
        "Будут показаны {number} отеля.",
        "Будут показаны {number} отелей."
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


@bot.message_handler(func=lambda message: "hotels_number" in get_state(chat_id=message.chat.id, column="states"))
@logger.catch
def hotels_number_choice(message: Message) -> None:
    """
    Функция-хэндлер устанавливает количество показываемых отелей.
    """

    chat_id = message.chat.id

    logger.info(f"В чате - {chat_id} пользователь {message.from_user.first_name} выбирает кол-во показываемых отелей.")

    max_hotels = 25
    text = message.text

    if text.isdigit():
        max_hotels = min(max_hotels, max(1, int(text)))
        hotels_word = get_hotels_word(number=max_hotels)
        bot.send_message(chat_id=chat_id, text=hotels_word.format(number=max_hotels))
    else:
        bot.send_message(chat_id=chat_id, text=f"Некорректный ввод.\nБудут показаны не более {max_hotels} отелей.")

    set_current_requests(chat_id=chat_id, hotels_count=max_hotels)

    current_id_message = bot.send_message(
        chat_id=chat_id, text="Показывать фотографии отелей?", reply_markup=markup_choice_photo()
    )
    set_state(chat_id=chat_id, states="images_choice", message_id=current_id_message.id)
