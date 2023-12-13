import time

from loguru import logger

import handlers
from bot_loader import bot
from database.pw_db import create_models
from utils.set_bot_commands import set_default_commands


@logger.catch
def main() -> None:
    """Функция запускает бота."""

    # Настройка логирования
    logger.add(
        "logs/logs.log",
        level="DEBUG",
        format="{time} {level} {message}",
        rotation="1 week",
        retention="1 week",
        compression="zip",
    )

    # Установка команд бота и создание таблиц в базе данных
    set_default_commands(bot=bot)
    create_models()

    while True:
        try:
            # Запуск бота с обработкой исключений
            logger.info("Запуск бота.")
            bot.polling(skip_pending=True)
        except KeyboardInterrupt:
            # Обработка прерывания клавишей
            logger.info("Завершение работы.")
            exit()
        except SystemExit:
            # Обработка исключения SystemExit
            logger.info("Программа завершена по запросу.")
            break
        except Exception as error:
            # Обработка других исключений
            logger.debug(f"Ошибка - {error}.")
            bot.stop_polling()
            time.sleep(1)


if __name__ == "__main__":
    main()
