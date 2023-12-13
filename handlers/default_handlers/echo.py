from loguru import logger
from telebot.types import Message

from bot_loader import bot
from handlers.default_handlers.main_commands import bot_start


@logger.catch
@bot.message_handler(content_types=["text"])
def bot_echo(message: Message) -> None:
    """
    Функция хендлер, перехватывает текстовые сообщения без указанного состояния.
    """

    logger.info(f"В чате - {message.chat.id} пользователь {message.from_user.first_name} набрал текст: {message.text}")
    if message.text.lower() in ("ghbdtn", "привет", "hello-world", "hello world", "hello", "hi"):
        bot_start(message=message)
    else:
        bot.reply_to(message=message, text="Я тебя не понимаю. Напиши /help.")


@logger.catch
@bot.message_handler(content_types=[
    "audio", "document", "photo", "sticker", "video", "video_note",
    "voice", "location", "contact", "venue", "animation", "poll"
])
def message_reply(message: Message) -> None:
    """
    Функция отвечает на отличные от текстовых сообщения пользователя.
    """

    logger.info(f"В чате - {message.chat.id} пользователь {message.from_user.first_name} отправил: {message.content_type}")
    bot.reply_to(message=message, text="Я тебя не понимаю. Напиши /help.")
