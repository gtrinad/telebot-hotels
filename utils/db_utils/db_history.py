import datetime
import shelve
from collections import OrderedDict
from typing import Dict, List, Optional

from config_data.config import DATA_HISTORY_FILE, NUMBER_HISTORY


def get_pickle(id_chat: int) -> Dict:
    """
    Функция получает из файла историю запросов пользователя.
    """

    key: str = str(id_chat)
    with shelve.open(DATA_HISTORY_FILE) as db:
        return db.get(key, {})


def set_pickle(
    id_chat: int,
    command: str,
    destination_id: int,
    hotel_info: str,
    images: Optional[List[str]] = None,
) -> None:
    """
    Функция записывает в файл историю запросов пользователя.
    """

    key: str = str(id_chat)
    with shelve.open(DATA_HISTORY_FILE) as db:
        data_new: Dict = db.get(key, {})

        if command in data_new:
            if len(data_new[command]) == NUMBER_HISTORY + 1:
                data_new[command].popitem(last=False)
        else:
            data_new[command] = OrderedDict()

        if destination_id not in data_new[command]:
            result_time: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            data_new[command][destination_id] = [result_time]

        data_new[command][destination_id].append((hotel_info, images))

        db[key] = data_new
