from telebot.types import CallbackQuery

from bot_loader import bot
from keyboards.other.calendar import calendar
from utils.db_utils.current_requests import set_current_requests


def calendar_call(
    call: CallbackQuery,
    sep,
    text_choice: str,
    markup_day,
    markup_cancel,
    edit_column: str,
) -> None:
    """
    Функция обрабатывает call календаря.
    """

    chat_id: int = call.message.chat.id
    name, action, year, month, day = call.data.split(sep)
    date_choice = calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )

    if action == "DAY":
        date_str: str = date_choice.strftime("%Y-%m-%d")
        bot.send_message(
            chat_id=chat_id, text=f"{text_choice} {date_str}", reply_markup=markup_day
        )
        if edit_column in ("check_in", "check_out"):
            set_current_requests(chat_id=chat_id, **{f"{edit_column}": date_str})
    elif action == "CANCEL":
        bot.send_message(
            chat_id=chat_id, text="Хотите завершить?", reply_markup=markup_cancel
        )
