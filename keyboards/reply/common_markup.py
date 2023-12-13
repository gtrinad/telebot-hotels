from typing import List, Tuple

from loguru import logger
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


@logger.catch
def markup_choice_city() -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру подтверждения продолжить выбор города.
    """

    logger.info("Подтверждение продолжить выбор города.")
    buttons = [
        InlineKeyboardButton(text="Да", callback_data="city_yes"),
        InlineKeyboardButton(text="Нет", callback_data="city_no"),
    ]

    return InlineKeyboardMarkup().add(*buttons)


@logger.catch
def city_markup(cities: List) -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру подтверждения выбора города.
    """

    logger.info("Подтверждение выбора города.")
    buttons = [
        InlineKeyboardButton(
            text=index.get("city_name"),
            callback_data=f'id {index.get("destination_id")}',
        )
        for index in cities
    ]

    return InlineKeyboardMarkup(row_width=1).add(*buttons)


def markup_choice_date_to() -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру подтверждения выбора даты выезда.
    """

    buttons = [
        InlineKeyboardButton(text="Всё верно", callback_data="date_to_right"),
        InlineKeyboardButton(text="Изменить", callback_data="date_to_change"),
    ]

    return InlineKeyboardMarkup().add(*buttons)


def markup_to_cancel() -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру подтверждения продолжить выбор даты выезда.
    """

    buttons = [
        InlineKeyboardButton(text="Завершить", callback_data="date_to_cancel"),
        InlineKeyboardButton(text="Продолжить", callback_data="date_to_continue"),
    ]

    return InlineKeyboardMarkup().add(*buttons)


def markup_choice_date_from() -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру подтверждения выбора даты въезда.
    """

    buttons = [
        InlineKeyboardButton(text="Всё верно", callback_data="date_from_right"),
        InlineKeyboardButton(text="Изменить", callback_data="date_from_change"),
    ]

    return InlineKeyboardMarkup().add(*buttons)


def markup_from_cancel() -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру подтверждения продолжить выбор даты въезда.
    """

    buttons = [
        InlineKeyboardButton(text="Завершить", callback_data="date_from_cancel"),
        InlineKeyboardButton(text="Продолжить", callback_data="date_from_continue"),
    ]

    return InlineKeyboardMarkup().add(*buttons)


@logger.catch
def markup_start(commands: Tuple) -> InlineKeyboardMarkup:
    """Функция генерирует клавиатуру выбора команд."""

    excluded_commands = {"start", "help", "cancel"}

    logger.info("Выбор основных команд: /low, /high, /custom, /history.")
    buttons = [
        InlineKeyboardButton(text=command[0], callback_data=command[0])
        for command in commands
        if command[0] not in excluded_commands
    ]

    return InlineKeyboardMarkup(row_width=2).add(*buttons)


@logger.catch
def markup_choice_photo() -> InlineKeyboardMarkup:
    """
    Функция генерирует клавиатуру подтверждения выбора фото.
    """

    logger.info("Подтверждение выбора фото.")
    buttons = [
        InlineKeyboardButton(text="Да", callback_data="choice_photo_yes"),
        InlineKeyboardButton(text="Нет", callback_data="choice_photo_no"),
    ]

    return InlineKeyboardMarkup().add(*buttons)
