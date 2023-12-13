from typing import Dict, Union

import requests
from loguru import logger
from requests import Response

from config_data.config import RapidAPIConfig

site = RapidAPIConfig()


@logger.catch
def get_api(url: str, querystring: Dict) -> Union[Response, bool]:
    """
    Функция делает запрос к API Hotels и возвращает результат.
    """

    headers: Dict = {
        "X-RapidAPI-Host": site.API_HOST,
        "X-RapidAPI-Key": site.API_KEY.get_secret_value(),
    }

    try:
        for _ in range(3):
            logger.info(f"Отправляется {_ + 1} запрос на сервер на поиск города.")
            api_response: Response = requests.get(
                url=url, headers=headers, params=querystring, timeout=10
            )
            if api_response.status_code == requests.codes["ok"]:
                return api_response
    except (requests.exceptions.Timeout, ConnectionError) as error:
        logger.error(f"Ошибка: {error}")

    return False
