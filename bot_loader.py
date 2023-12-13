from telebot import TeleBot

from config_data.config import BotConfig


bot: TeleBot = TeleBot(token=BotConfig().BOT_TOKEN.get_secret_value())
