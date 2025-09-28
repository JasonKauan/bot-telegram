from env import bot_config
import telebot

api = bot_config.API_TOKEN
bot = telebot.TeleBot(api)


@bot.message_handler(commands = ["opc1"])
def opc1(message):
    bot.reply_to(message, "teste1")


@bot.message_handler(commands = ["opc2"])
def opc2(message):
    bot.reply_to(message, "teste2")

@bot.message_handler(commands = ["opc3"])
def opc3(message):
    bot.reply_to(message, "teste3")







def verificar(message):
    return True

@bot.message_handler(func = verificar)
def responder(message):
    texto = """
    Escolha uma opção(clique no item)
    /opc1 teste1
    /opc2 teste2
    /opc3 teste3
    
    """
    bot.reply_to(message, texto)





bot.polling(none_stop=True)

