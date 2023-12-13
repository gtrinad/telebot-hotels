from typing import Any

from telebot_calendar import Calendar, RUSSIAN_LANGUAGE, CallbackData

calendar: Any = Calendar(language=RUSSIAN_LANGUAGE)
calendar_date_from: Any = CallbackData(
    "calendar_date_from", "action", "year", "month", "day"
)
calendar_date_to: Any = CallbackData(
    "calendar_date_to", "action", "year", "month", "day"
)
