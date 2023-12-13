import re
from typing import Union, List

from loguru import logger
from requests import Response

from utils.db_utils.cities import add_cities
from utils.re_patterns import PATTERN_CITY


@logger.catch
def city_check(response_api: Union[Response, bool]) -> Union[List[dict], bool]:
    """
    Функция осуществляет поиск значений в полученном ответе API.
    """

    if not response_api:
        logger.error("Пустой ответ API")
        return False

    response_text = response_api.text

    matches = re.finditer(pattern=PATTERN_CITY, string=response_text)

    cities: List[dict] = []

    for match in matches:
        city_data = {
            "city_name": match.group("fullName"),
            "destination_id": int(match.group("sourceId")),
            "latitude": match.group("latitude"),
            "longitude": match.group("longitude"),
        }
        cities.append(city_data)

    if cities:
        add_cities(cities=cities)
        return cities
    else:
        logger.warning("В ответе API отсутствуют данные о городах")
        return False
