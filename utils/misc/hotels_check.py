import re
from typing import Union, List

from loguru import logger
from requests import Response

from utils.db_utils.current_requests import get_current_requests
from utils.misc.check_distance import check_distance
from utils.misc.hotels_summary import get_summary
from utils.re_patterns import PATTERN_PROPERTY


@logger.catch
def hotels_check(
    response_api: Union[Response, bool],
    show_photo: int,
    hotels_count: int,
    chat_id: int = None,
) -> Union[List, bool]:
    """
    Функция выбирает необходимую информацию и возвращает список отелей.
    """

    distance_min: int = (
        get_current_requests(chat_id=chat_id, column="distance_min") if chat_id else 0
    )
    distance_max: int = (
        get_current_requests(chat_id=chat_id, column="distance_max") if chat_id else 100
    )

    pattern = re.compile(pattern=PATTERN_PROPERTY)

    matches = pattern.finditer(string=response_api.text)
    if not matches:
        return False

    hotels = []
    hotels_added = 0  # Счетчик добавленных отелей

    for match in matches:
        if hotels_added >= hotels_count:
            break  # Прерывание цикла, если достигнуто указанное количество отелей

        data = match.groupdict()

        property_id = data["Property_id"]
        name = data["name"]
        distance_from_center = float(data["distanceFromDestination"])
        latitude = data["latitude"]
        longitude = data["longitude"]
        day_price = float(data["amount"])

        if chat_id and not check_distance(
            landmark=distance_from_center,
            distance_min=distance_min,
            distance_max=distance_max,
        ):
            continue

        hotel_summary = get_summary(hotel_id=property_id, show_photo=show_photo)
        logger.info("Получен ответ get_summary.")
        if hotel_summary:
            star_rating = hotel_summary.get("star_rating", "")
            review_info = hotel_summary.get("review_info", "")
            address = hotel_summary.get("address", "")
            images = hotel_summary.get("images", "")

            result = {
                "hotel_name": name,
                "hotel_id": property_id,
                "day_price": day_price,
                "latitude": latitude,
                "longitude": longitude,
                "distance": distance_from_center,
                "star_rating": star_rating,
                "review_info": review_info,
                "address": address,
                "images": images,
            }

            if result["hotel_id"] not in {
                structure["hotel_id"] for structure in hotels
            }:
                hotels.append(result)
                hotels_added += 1

            logger.info(result)

    return hotels if hotels else False
