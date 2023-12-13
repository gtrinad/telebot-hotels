from peewee import Model, IntegerField, CharField

from config_data.config import USER_DATABASE


class BaseModel(Model):
    class Meta:
        database = USER_DATABASE


class User(BaseModel):
    user_id: int = IntegerField(primary_key=True)
    username: str = CharField(max_length=255)
    first_name: str = CharField(max_length=255)
    last_name: str = CharField(max_length=255)
    full_name: str = CharField(max_length=255)


class Cities(BaseModel):
    """
    Класс Cities используется для создания таблицы хранящей сведения о найденных городах в БД "telebot_db".
    """

    destination_id: int = IntegerField(primary_key=True)
    name: str = CharField(max_length=255)
    latitude: str = CharField(max_length=100)
    longitude: str = CharField(max_length=100)


class UserStates(BaseModel):
    """
    Класс UserStates используется для создания таблицы хранящей сведения о состоянии пользователя в БД "telebot_db".
    """

    chat_id: int = IntegerField(primary_key=True)
    message_id: int = IntegerField()
    states: int = CharField(max_length=255)


class CurrentRequests(BaseModel):
    """
    Класс CurrentRequests используется для создания таблицы хранящей сведения о текущем запросе в БД "telebot_db".
    """

    chat_id: int = IntegerField(primary_key=True)
    current_command: str = CharField(max_length=255)
    destination_id: int = IntegerField()
    hotels_count: int = IntegerField()
    images_count: int = IntegerField()
    check_in: str = CharField()
    check_out: str = CharField()
    price_min: int = IntegerField()
    price_max: int = IntegerField()
    distance_min: int = IntegerField()
    distance_max: int = IntegerField()


class HotelsPagination(BaseModel):
    """
    Класс HotelsPagination используется для создания таблицы хранящей сведения истории в БД "telebot_db".
    """

    message_id: int = IntegerField(primary_key=True)
    command: str = CharField(max_length=255)
    city_id: int = IntegerField()


def create_models():
    USER_DATABASE.create_tables(models=BaseModel.__subclasses__(), safe=True)
