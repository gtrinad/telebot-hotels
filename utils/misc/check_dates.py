from datetime import datetime, timedelta

from bot_loader import bot
from utils.db_utils.current_requests import get_current_requests, set_current_requests
from utils.db_utils.state import set_state
from utils.misc.check_date import check_date, get_date


def check_dates(chat_id: int) -> None:
    """
    Функция проверяет введенные пользователем даты.
    """

    bot.send_message(chat_id=chat_id, text="Проверяю даты...")
    date_today: str = datetime.today().strftime("%Y-%m-%d")

    date_in, date_out = (
        get_current_requests(chat_id=chat_id, column=column)
        for column in ["check_in", "check_out"]
    )

    if check_date(date_start=date_today, date_end=date_in) < 0:
        bot.send_message(
            chat_id=chat_id,
            text=f"Дата въезда установлена на сегодня: {date_today},\n"
            f"т.к. вы указали дату предшествующую сегодняшнему дню.",
        )
        set_current_requests(chat_id=chat_id, check_in=date_today)
        date_in = date_today

    if check_date(date_start=date_in, date_end=date_out) <= 0:
        date_out = get_date(convert_date=date_in) + timedelta(days=1)
        set_current_requests(chat_id=chat_id, check_out=date_out.strftime("%Y-%m-%d"))
        bot.send_message(
            chat_id=chat_id,
            text=f'Дата выезда установлена на следующий день дня заезда: {date_out.strftime("%Y-%m-%d")},\n'
            f"т.к. вы указали дату выезда равную предшествующему или дню заезда.",
        )

    bot.send_message(chat_id=chat_id, text=f"Дата въезда: {date_in}")
    bot.send_message(chat_id=chat_id, text=f"Дата выезда: {date_out}")

    bot.send_message(chat_id=chat_id, text="Все ок.")
    bot.send_message(
        chat_id=chat_id, text="Выберите количество отелей для показа (1-25):"
    )
    set_state(chat_id=chat_id, states="hotels_number")
