from typing import Dict, Union, List

from loguru import logger
from requests import Response
from telebot.types import Message

from bot_loader import bot
from config_data.config import RapidAPIConfig
from keyboards.reply.common_markup import city_markup, markup_choice_city
from utils.db_utils.state import get_state, set_state
from utils.misc.city_check import city_check
from utils.misc.get_api import get_api

site = RapidAPIConfig()


@bot.message_handler(
    func=lambda message: "city" == get_state(chat_id=message.chat.id, column="states")
)
@logger.catch
def find_a_city(message: Message) -> None:
    """
    Функция осуществляет поиск города и предоставляет пользователю выбрать из результатов поиска.
    """

    chat_id: int = message.chat.id

    logger.info(f"В чате - {chat_id} осуществляется поиск города.")

    url: str = f"https://{site.API_HOST}/locations/v3/search"
    querystring: Dict = {
        "q": message.text,
        "locale": "en_US",
        "langid": "1033",
        "siteid": "300000001",
    }
    response: Union[Response, bool] = get_api(url=url, querystring=querystring)
    logger.info(f"Получен ответ с сервера по поиску города.")
    result_check: Union[List, bool] = city_check(response_api=response)

    if result_check:
        set_state(
            chat_id=chat_id,
            states="choice_cities",
            message_id=bot.send_message(
                chat_id=chat_id,
                text="Уточните, пожалуйста:",
                reply_markup=city_markup(result_check),
            ).id,
        )
    else:
        set_state(
            chat_id=chat_id,
            states="choice_not_cities",
            message_id=bot.send_message(
                chat_id=chat_id,
                text="Увы ничего не нашлось, попробуем еще?",
                reply_markup=markup_choice_city(),
            ).id,
        )
