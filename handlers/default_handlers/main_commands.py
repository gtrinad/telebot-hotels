from typing import List

from loguru import logger
from telebot.types import Message

from bot_loader import bot
from config_data.config import DEFAULT_COMMANDS
from database.pw_db import User
from keyboards.reply.common_markup import markup_start
from utils.db_utils.current_requests import set_current_requests
from utils.db_utils.state import set_state


@bot.message_handler(commands=["cancel"])
@logger.catch
def cancel_command(message: Message) -> None:
    """Функция сбрасывает состояния пользователя."""

    chat_id: int = message.chat.id

    logger.info(f"В чате - {chat_id} пользователь {message.from_user.first_name} запустил команду /cancel")
    bot.send_message(chat_id=chat_id, text="Ваша команда отменена, чтобы начать заново введите /start")

    set_state(chat_id=chat_id, states="0")
    set_current_requests(chat_id=chat_id, default=True)


@bot.message_handler(commands=["start"])
@logger.catch
def bot_start(message: Message):
    chat_id: int = message.chat.id
    user_id: int = message.from_user.id
    username: str = message.from_user.username or "UnknownUsername"
    first_name: str = message.from_user.first_name or "UnknownFirstName"
    last_name: str = message.from_user.last_name or "UnknownLastName"
    full_name: str = message.from_user.full_name or "UnknownFullName"

    logger.info(f"В чате - {chat_id} пользователь {first_name} запустил команду /start")

    user, created = User.get_or_create(
        user_id=user_id,
        defaults={
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
        },
    )

    welcome_message = (
        f"Добро пожаловать {first_name}!" if created else f"Рад вас снова видеть {first_name}!"
    )

    bot.reply_to(message=message, text=welcome_message)
    bot.send_message(
        chat_id=chat_id,
        text="Я Бот, помогу тебе выбрать отель в нужном городе!\nВыберите команду:",
        reply_markup=markup_start(commands=DEFAULT_COMMANDS)
    )

    bot.send_message(chat_id=chat_id, text="Описание команд - /help")
    set_state(chat_id=chat_id, states="0")


@bot.message_handler(commands=["help"])
@logger.catch
def bot_help(message: Message) -> None:
    """Функция хэндлер отвечает на команду help."""

    chat_id: int = message.chat.id

    logger.info(f"В чате - {chat_id} пользователь {message.from_user.first_name} запустил команду /help")

    commands_list: List = [f"/{command} - {description}" for command, description in DEFAULT_COMMANDS]

    bot.reply_to(message=message, text="\n".join(commands_list))
    bot.send_message(chat_id=chat_id, text="Напишите /start чтобы начать.")
    set_state(chat_id=chat_id, states="0")


@logger.catch
def send_command(message: Message, command: str, description: str) -> None:
    """
    Функция-хэндлер отправляет сообщение при выборе команды /low, /high, /custom.
    """

    chat_id: int = message.chat.id

    logger.info(f"В чате - {chat_id} пользователь {message.from_user.first_name} запустил команду /{command}")
    set_state(chat_id=chat_id, states="city")
    set_current_requests(chat_id=chat_id, default=True, current_command=command)

    bot.send_message(chat_id=chat_id, text=f"Вы выбрали - {description}.\nВ каком городе ищем?")


@bot.message_handler(commands=["low"])
def send_lowprice(message: Message) -> None:
    """Функция-хэндлер предлагает ввести город для поиска топ самых дешёвых отелей."""

    send_command(message=message, command="low", description="узнать топ самых дешёвых отелей в городе")


@bot.message_handler(commands=["high"])
def send_highprice(message: Message) -> None:
    """Функция-хэндлер предлагает ввести город для поиска топ самых дорогих отелей."""

    send_command(message=message, command="high", description="узнать топ самых дорогих отелей в городе")


@bot.message_handler(commands=["custom"])
def send_custom(message: Message) -> None:
    """
    Функция-хэндлер предлагает ввести город для поиска отелей,
    наиболее подходящих по цене и расстоянию от центра города.
    """

    send_command(
        message=message,
        command="custom",
        description="узнать топ отелей, наиболее подходящих по цене и расстоянию от центра города"
    )
