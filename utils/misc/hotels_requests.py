from typing import Dict, Union, List, Optional

import requests
import telebot
from loguru import logger
from requests import Response
from telebot.types import InputMediaPhoto
from validator_collection import checkers

from bot_loader import bot
from config_data.config import RapidAPIConfig, DEFAULT_COMMANDS
from keyboards.reply.common_markup import markup_start
from utils.db_utils.current_requests import get_current_requests, set_current_requests
from utils.db_utils.db_history import set_pickle
from utils.db_utils.state import get_state
from utils.misc.check_date import check_date
from utils.misc.get_distance import get_distance_for_center
from utils.misc.get_prop_list import get_prop_list
from utils.misc.hotels_check import hotels_check


def get_star_suffix(star_rating):
    if star_rating == 1:
        return "звезда"
    elif 1 < star_rating < 5:
        return "звезды"
    else:
        return "звёзд"


def format_star_rating(hotel_star_rating):
    try:
        rating = float(hotel_star_rating)
        formatted_rating = f"{rating:.1f}" if rating % 1 != 0 else f"{int(rating)}"
        suffix = get_star_suffix(int(rating))
        return f"{formatted_rating} {suffix}"
    except ValueError:
        return ""


def get_hotels_find_word(number: int) -> str:
    """
    Получение правильной формы слова "отель" в зависимости от числа.
    """

    forms = [
        "найден {number} отель.",
        "найдено {number} отеля.",
        "найдено {number} отелей."
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
def request_hotels(chat_id: int, sort: str) -> None:
    """
    Функция осуществляет поиск отелей по заданным пользователем параметрам и отправляет результаты.
    """

    bot.send_message(chat_id=chat_id, text="Ищем отели, подходящие вашему запросу...")

    url: str = f"https://{RapidAPIConfig().API_HOST}/properties/v2/list"
    destination_id, check_in, check_out, hotels_count, user_command, show_photo = (
        get_current_requests(chat_id=chat_id, column=column)
        for column in
        ["destination_id", "check_in", "check_out", "hotels_count", "current_command", "images_count"]
    )

    check_in_data, check_out_data = map(lambda s: list(map(int, s.split("-"))), [check_in, check_out])

    payload: Dict = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": f"{str(destination_id)}"},
        "checkInDate": {
            "day": int(check_in_data[2]),
            "month": int(check_in_data[1]),
            "year": int(check_in_data[0])
        },
        "checkOutDate": {
            "day": int(check_out_data[2]),
            "month": int(check_out_data[1]),
            "year": int(check_out_data[0])
        },
        "rooms": [
            {
                "adults": 1,
                "children": []
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": sort,
        "filters": {"price": {
            "max": 1000000,
            "min": 1
        }}
    }

    response_api: Response = get_prop_list(url=url, payload=payload)

    logger.info(f"Чат - {chat_id}, по команде {user_command} получен ответ по поиску отелей.")

    if not response_api or not (hotels := hotels_check(
            response_api=response_api, show_photo=show_photo, chat_id=chat_id, hotels_count=hotels_count)
    ):
        logger.info(f"Чат - {chat_id}, по команде {user_command} ничего не найдено")
        handle_no_results(chat_id)
        return
    logger.info(f"Чат - {chat_id}, по команде {user_command} получен response_api")
    days_all: int = check_date(check_in, check_out)
    count_hotels: int = 0

    logger.info(f"Чат - {chat_id}, по команде {user_command} отправляются результаты поиска")
    logger.info(f"Чат - {chat_id}, по команде {user_command} найдено {len(hotels)} отелей.")

    for hotel in hotels:
        price: float = hotel.get("day_price")
        hotel_star_rating: str = hotel.get("star_rating")
        hotel_distance: str = hotel.get("distance")

        formatted_rating = format_star_rating(hotel_star_rating)
        more_than_day: str = "" if days_all in [0, 1] else f"Цена за весь период: ${days_all * price:.2f}."
        star_rating: str = f"Рейтинг: {formatted_rating}" if formatted_rating and formatted_rating != "0.0" else ""
        distance_for_center: str = (
            f"\nРасстояние до центра: {hotel_distance} км."
            if hotel_distance
            else f" {get_distance_for_center(structure=hotel, chat_id=chat_id):.1f} км."
        )

        hotel_info = (
            f"Название отеля: {hotel.get('hotel_name')}.\n"
            f"{star_rating}\n"
            f"Отзывы: {hotel['review_info']}.\n"
            f"Адрес: {hotel['address']}.\n"
            f"{distance_for_center}\n\n"
            f"Период пребывания: {check_in} - {check_out}\n"
            f"Цена за ночь: ${price}.\n"
            f"{more_than_day}"
        )
        send_hotel_info(chat_id=chat_id, user_command=user_command, destination_id=destination_id,
                        hotel_info=hotel_info, show_photo=show_photo, images=hotel.get("images"))
        count_hotels += 1

    logger.info(f"Чат - {chat_id}, по команде {user_command} отправлено информации о {count_hotels} отелях.")

    finish_search(chat_id=chat_id, hotels_count=count_hotels)


def handle_no_results(chat_id: int) -> None:
    bot.send_message(
        chat_id=chat_id,
        text="В городе ничего не найдено, желаете продолжить?",
        reply_markup=markup_start(commands=DEFAULT_COMMANDS)
    )
    bot.send_message(chat_id=chat_id, text="Описание команд - /help")


def send_hotel_info(chat_id: int, user_command: str, destination_id: int, hotel_info: str, show_photo: int, images: Optional[list[str]]):
    if show_photo > 0:
        result_images: Union[bool, List] = images
        if result_images:
            medias: List = []
            count = False
            for url in result_images[0:show_photo]:
                if checkers.is_url(url):
                    if not count:
                        medias.append(InputMediaPhoto(media=url, caption=hotel_info))
                        count = True
                    else:
                        medias.append(InputMediaPhoto(media=url))
            if get_state(chat_id=chat_id, column="states") == "send_result":
                set_pickle(id_chat=chat_id, command=user_command, destination_id=destination_id, hotel_info=hotel_info,
                           images=result_images)
                try:
                    bot.send_media_group(chat_id=chat_id, media=medias)
                except (telebot.apihelper.ApiTelegramException, requests.exceptions.ReadTimeout):
                    bot.send_message(
                        chat_id=chat_id,
                        text="Упс что-то пошло не так. Фото не загрузилось\n" + hotel_info,
                        disable_web_page_preview=True
                    )
            else:
                return
    else:
        if get_state(chat_id=chat_id, column="states") == "send_result":
            set_pickle(id_chat=chat_id, command=user_command, destination_id=destination_id, hotel_info=hotel_info)
            bot.send_message(chat_id=chat_id, text=hotel_info, disable_web_page_preview=True)
        else:
            return


def finish_search(chat_id: int, hotels_count: int):
    if get_state(chat_id=chat_id, column="states") == "send_result":
        set_current_requests(chat_id=chat_id, default=True)
        hotels_word = get_hotels_find_word(number=hotels_count)
        bot.send_message(
            chat_id=chat_id,
            text=f"Поиск окончен, по вашему запросу {hotels_word.format(number=hotels_count)}, желаете продолжить?",
            reply_markup=markup_start(DEFAULT_COMMANDS)
        )
        bot.send_message(chat_id=chat_id, text="Описание команд - /help")
