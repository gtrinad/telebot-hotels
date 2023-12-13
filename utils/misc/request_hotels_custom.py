from loguru import logger
from requests import Response

from bot_loader import bot
from config_data.config import RapidAPIConfig
from utils.db_utils.current_requests import get_current_requests
from utils.misc.check_date import check_date
from utils.misc.get_distance import get_distance_for_center
from utils.misc.get_prop_list import get_prop_list
from utils.misc.hotels_check import hotels_check
from utils.misc.hotels_requests import (
    format_star_rating,
    handle_no_results,
    send_hotel_info,
    finish_search,
)


@logger.catch
def request_hotels_custom(chat_id: int) -> None:
    """
    Функция осуществляет поиск отелей по заданным пользователем параметрам и отправляет результаты.
    """

    bot.send_message(chat_id, text="Ищем отели, подходящие вашему запросу...")

    url: str = f"https://{RapidAPIConfig().API_HOST}/properties/v2/list"
    (
        destination_id,
        check_in,
        check_out,
        hotels_count,
        user_command,
        show_photo,
        price_min,
        price_max,
    ) = (
        get_current_requests(chat_id=chat_id, column=column)
        for column in [
            "destination_id",
            "check_in",
            "check_out",
            "hotels_count",
            "current_command",
            "images_count",
            "price_min",
            "price_max",
        ]
    )

    check_in_data, check_out_data = map(
        lambda s: list(map(int, s.split("-"))), [check_in, check_out]
    )

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": f"{str(destination_id)}"},
        "checkInDate": {
            "day": int(check_in_data[2]),
            "month": int(check_in_data[1]),
            "year": int(check_in_data[0]),
        },
        "checkOutDate": {
            "day": int(check_out_data[2]),
            "month": int(check_out_data[1]),
            "year": int(check_out_data[0]),
        },
        "rooms": [{"adults": 1, "children": []}],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {"max": price_max, "min": price_min}},
    }

    response_api: Response = get_prop_list(url=url, payload=payload)

    logger.info(
        f"Чат - {chat_id}, по команде {user_command} получен ответ по поиску отелей."
    )

    if not response_api or not (
        hotels := hotels_check(
            response_api=response_api,
            show_photo=show_photo,
            chat_id=chat_id,
            hotels_count=hotels_count,
        )
    ):
        logger.info(f"Чат - {chat_id}, по команде {user_command} ничего не найдено")
        handle_no_results(chat_id)
        return
    logger.info(f"Чат - {chat_id}, по команде {user_command} получен response_api")
    days_all: int = check_date(check_in, check_out)
    count_hotels: int = 0

    logger.info(
        f"Чат - {chat_id}, по команде {user_command} отправляются результаты поиска"
    )
    logger.info(
        f"Чат - {chat_id}, по команде {user_command} найдено {len(hotels)} отелей."
    )

    for hotel in hotels:
        if count_hotels == hotels_count:
            break
        price: float = hotel.get("day_price")
        hotel_star_rating: str = hotel.get("star_rating")
        hotel_distance: str = hotel.get("distance")

        formatted_rating = format_star_rating(hotel_star_rating)
        more_than_day: str = (
            ""
            if days_all in [0, 1]
            else f"Цена за весь период: ${days_all * price:.2f}."
        )
        star_rating: str = (
            f"Рейтинг: {formatted_rating}"
            if formatted_rating and formatted_rating != "0.0"
            else ""
        )
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
        send_hotel_info(
            chat_id=chat_id,
            user_command=user_command,
            destination_id=destination_id,
            hotel_info=hotel_info,
            show_photo=show_photo,
            images=hotel.get("images"),
        )
        count_hotels += 1

    finish_search(chat_id=chat_id, hotels_count=count_hotels)
