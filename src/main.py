from env import bot_config
import telebot

api = bot_config.API_TOKEN
bot = telebot.TeleBot(api)


@bot.message_handler(commands=['start', 'help'])
def responder(message):
    bot.reply_to(message, "Hello, I am a bot!")





bot.polling(none_stop=True)

