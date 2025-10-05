from env import bot_config
import telebot
from telebot import types
import os # Usaremos a biblioteca OS para lidar com os caminhos dos arquivos

api = bot_config.API_TOKEN
bot = telebot.TeleBot(api)

# --- CONFIGURAÇÃO DOS PRODUTOS E TOKEN ---

# ATENÇÃO: Coloque o caminho completo para os seus arquivos aqui.
# Usar os.path.join é uma boa prática para que funcione em diferentes sistemas operacionais.
BASE_DIR = "C:\\Users\\rapha\\OneDrive\\Projetos\\env\\Livro_antiotario"
CAPA_LIVRO_PATH = os.path.join(BASE_DIR, "capa.jpg")
PDF_LIVRO_PATH = os.path.join(BASE_DIR, "Antiotario-Um-caminho-sem-volta-Rafael-Aires.pdf")

# Seu token de pagamento (pode ser o de teste para continuar testando, ou o de produção no futuro)
PAYMENT_PROVIDER_TOKEN = bot_config.TOKEN_PAGAMENTO


# --- FUNÇÃO DE ENTREGA DO PRODUTO ---

def entregar_produto(chat_id):
    """
    Função dedicada a enviar os arquivos do produto para o usuário.
    """
    try:
        bot.send_message(chat_id, "Pagamento confirmado! ✅\n\nEnviando seu livro agora mesmo...")
        # Envia o arquivo PDF
        with open(PDF_LIVRO_PATH, "rb") as doc:
            bot.send_document(chat_id, doc)
        bot.send_message(chat_id, "Aqui está! Esperamos que goste da leitura. Obrigado pela confiança!")
    except Exception as e:
        # Mensagem de erro caso o bot não consiga encontrar os arquivos
        print(f"ERRO CRÍTICO ao entregar o produto para o chat {chat_id}: {e}")
        bot.send_message(chat_id, "Houve um problema ao tentar enviar seu arquivo. 😥 Por favor, entre em contato com o suporte para receber seu produto.")


# --- FLUXO DE PAGAMENTO E COMANDOS DO BOT ---

# 1. Comando principal para iniciar a compra do livro
@bot.message_handler(commands=["comprar_livro"])
def comando_comprar_livro(message):
    # Primeiro, enviamos a imagem do produto para o usuário ver o que está comprando
    try:
        with open(CAPA_LIVRO_PATH, "rb") as img:
            bot.send_photo(message.chat.id, img, caption="Você está prestes a adquirir o livro 'Antiotário: Um caminho sem volta'.")
    except Exception as e:
        print(f"Erro ao enviar a imagem da capa: {e}")
        bot.send_message(message.chat.id, "Não consegui carregar a imagem do produto, mas podemos continuar.")

    # Em seguida, enviamos a fatura para pagamento
    title = "Livro: Antiotário"
    description = "Um guia prático para o desenvolvimento pessoal e financeiro."
    payload = "livro-antiotario-v1"
    currency = "BRL"
    price = 1990  # Preço em centavos. Ex: R$ 19,90 = 1990
    prices = [types.LabeledPrice(label="Livro Digital (PDF)", amount=price)]

    bot.send_invoice(
        chat_id=message.chat.id,
        title=title,
        description=description,
        invoice_payload=payload,
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency=currency,
        prices=prices,
    )

# 2. Comando "reserva" para planos futuros
@bot.message_handler(commands=["planos_futuros"])
def comando_planos_futuros(message):
    bot.reply_to(message, "Em breve teremos novos produtos e planos disponíveis. Fique de olho! 👀")


# 3. Handler para a verificação pré-checkout (OBRIGATÓRIO)
@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout_process(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    print("PreCheckoutQuery respondido com sucesso!")


# 4. Handler para o pagamento bem-sucedido -> AQUI A MÁGICA ACONTECE!
@bot.message_handler(content_types=['successful_payment'])
def successful_payment_process(message):
    print(f"✅ Pagamento recebido com sucesso! Payload: {message.successful_payment.invoice_payload}")
    # Chama a função para entregar o PDF ao usuário
    entregar_produto(message.chat.id)


# 5. Mensagem de boas-vindas e menu principal
def exibir_menu(message):
    texto = """
Olá! Seja bem-vindo(a).

Aqui você pode adquirir seu guia para o desenvolvimento.

Escolha uma opção para começar:
/comprar_livro - Adquirir o livro 'Antiotário'.
/planos_futuros - Ver novidades futuras.
"""
    bot.reply_to(message, texto)

@bot.message_handler(commands=['start', 'ajuda'])
def comando_start(message):
    exibir_menu(message)

# 6. Resposta para qualquer outra mensagem não reconhecida
@bot.message_handler(func=lambda message: True)
def responder_default(message):
    # Apenas exibe o menu principal como resposta padrão para qualquer mensagem.
    exibir_menu(message)


# --- INICIA O BOT ---
print("🚀 Bot em execução...")
bot.polling(none_stop=True)