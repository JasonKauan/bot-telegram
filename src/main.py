from env import bot_config
import telebot

api = bot_config.API_TOKEN
print(api)
bot = telebot.TeleBot(api)





