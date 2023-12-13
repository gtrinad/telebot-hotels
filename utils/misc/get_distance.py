from typing import Dict, Union

from geopy.distance import distance
from loguru import logger

from utils.db_utils.cities import get_cities
from utils.db_utils.current_requests import get_current_requests


@logger.catch
def get_distance_for_center(structure: Dict, chat_id: int) -> Union[int, float]:
    hotel_latitude, hotel_longitude = structure.get("latitude"), structure.get("longitude")
    if hotel_latitude != 0 and hotel_longitude != 0:
        city_current_id = get_current_requests(chat_id=chat_id, column="destination_id")
        city_latitude, city_longitude = (
            get_cities(destination_id=city_current_id, column=column)
            for column in ["latitude", "longitude"]
        )
        city_coordinates = (city_latitude, city_longitude)

        try:
            result = distance(city_coordinates, (hotel_latitude, hotel_longitude)).km
            return result
        except ValueError as e:
            logger.warning(f"Error calculating distance: {e}")
            return 0
    else:
        return 0
