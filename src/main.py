from env import bot_config
import telebot

api = bot_config.API_TOKEN
bot = telebot.TeleBot(api)

@bot.message_handler(commands=["opc1"])
def opc1(message):
    print(message)
    bot.reply_to(message, "teste1")
    # bot.send_message(message.chat.id, "teste1")
    # bot.send_message envia uma mensagem para o usuario, diferente do reply, que responde.
    # bot.send_message precisa do parametro de chat e id para enviar, alem da message



# Enviar documento
@bot.message_handler(commands=['opc2'])
def enviar_doc(message):
    with open("C:\\Users\\rapha\OneDrive\Projetos\env\Livro_antiotario\capa.jpg", "rb") as img:
        bot.send_photo(message.chat.id, img)
    with open("C:\\Users\\rapha\OneDrive\Projetos\env\Livro_antiotario\Antiotario-Um-caminho-sem-volta-Rafael-Aires.pdf", "rb") as doc:
        bot.send_document(message.chat.id, doc)
    bot.send_message(message.chat.id, "Aqui está seu arquivo 📄")



@bot.message_handler(commands=["opc3"])
def opc3(message):
    print(message)
    bot.reply_to(message, "teste3")


# mensagem que o bot responde a qualquer mensagem enviada á ele.

def verificar(message):
    return True


@bot.message_handler(func=verificar)
def responder(message):
    texto = """
    Escolha uma opção(clique no item)
    /opc1 teste1
    /opc2 teste2
    /opc3 teste3

    """
    bot.reply_to(message, texto)





bot.polling(none_stop=True)

