from datetime import date

from loguru import logger


@logger.catch
def get_date(convert_date: str) -> date:
    """
    Функция конвертирует полученную дату в строковом выражении и возвращает объект класса date.
    """

    logger.info("Конвертируем дату в объект 'date'.")
    return date(*map(int, convert_date.split("-")))


@logger.catch
def check_date(date_start: str, date_end: str) -> int:
    """
    Функция сравнивает две даты.
    """

    logger.info("Сравниваем даты.")
    return (get_date(convert_date=date_end) - get_date(convert_date=date_start)).days
