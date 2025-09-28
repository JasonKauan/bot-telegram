from env import bot_config
import telebot

api = bot_config.API_TOKEN
bot = telebot.TeleBot(api)





def verificar(message):
    return True

@bot.message_handler(func = verificar)
def responder(message):
    bot.reply_to(message, "Jason é corno")





bot.polling(none_stop=True)

