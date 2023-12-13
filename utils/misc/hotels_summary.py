import re
from typing import Union, Dict, Any, List

from loguru import logger

from config_data.config import RapidAPIConfig
from utils.misc.get_prop_list import get_prop_list
from utils.re_patterns import PATTERN_SUMMARY, PATTERN_IMAGES


@logger.catch
def get_summary(
    hotel_id: str, show_photo: int = 0
) -> Union[bool, Dict[str, Union[str, List[str]]]]:
    """
    Функция получает на вход ID отеля и возвращает информацию по отелю, включая фотографии (при наличии show_photo).
    """

    url = f"https://{RapidAPIConfig().API_HOST}/properties/v2/get-summary"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": f"{str(hotel_id)}",
    }

    response_api: Any = get_prop_list(url=url, payload=payload)
    logger.info(
        f"Получен ответ от API Hotels (get-summary) по гостинице: ID_{hotel_id}."
    )
    if not response_api:
        logger.info("Получен пустой ответ от API Hotels (get-summary).")
        return False

    response = response_api.text
    summary_pattern = re.compile(pattern=PATTERN_SUMMARY)

    summary_match = summary_pattern.search(string=response)

    if summary_match:
        rating, address, review_info = summary_match.groups()

        result = {"star_rating": rating, "address": address, "review_info": review_info}

        # Добавим фотографии только при наличии указания show_photo
        if show_photo:
            images_pattern = re.compile(pattern=PATTERN_IMAGES)
            images_matches = images_pattern.findall(string=response)[:show_photo]
            if images_matches:
                url_images = [url.replace("{size}", "y") for url in images_matches]
                result["images"] = url_images
        logger.info(result)
        return result
    else:
        return False
