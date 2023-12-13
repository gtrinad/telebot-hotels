from typing import Dict, Union

import requests
from loguru import logger
from requests import Response

from config_data.config import RapidAPIConfig

site = RapidAPIConfig()
RAPID_API_HOST = site.API_HOST
RAPID_API_KEY = site.API_KEY.get_secret_value()

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": RAPID_API_HOST,
}


@logger.catch
def get_prop_list(url: str, payload: Dict) -> Union[Response, bool]:
    """
    Функция делает запрос к API Hotels и возвращает результат.
    """

    for _ in range(3):
        logger.info(f"Отправляется запрос {_ + 1} к API Hotels.")
        try:
            api_response: Response = requests.post(
                url=url, headers=headers, json=payload, timeout=10
            )
            if api_response.ok:
                return api_response
        except (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
        ) as error:
            logger.error(f"Ошибка {type(error).__name__}: {error}")

    return False
