from loguru import logger
from telebot import TeleBot
from telebot.types import BotCommand

from config_data.config import DEFAULT_COMMANDS


@logger.catch
def set_default_commands(bot: TeleBot = None) -> None:
    """
    Функция устанавливает команды бота по умолчанию.

    Parameters:
        bot (TeleBot, optional): Объект TeleBot. Defaults to None.
    """

    if bot is None:
        logger.warning("Не передан объект TeleBot. Команды бота не установлены.")
        return

    bot.set_my_commands([BotCommand(*command) for command in DEFAULT_COMMANDS])
    logger.info("Установлены команды бота по умолчанию.")
