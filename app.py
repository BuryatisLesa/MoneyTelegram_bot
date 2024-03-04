import telebot   
import requests
import json

TOKEN = '6873314876:AAFohVU_HxqF-f5KTh92JVxtH_m9hWzc8do'

keys = {'евро': 'EUR',
        'биткоин':'BTC',
        'эфириум': 'ETH',
        'доллар': 'USD'}

bot = telebot.TeleBot(TOKEN)

# Обрабатывается при команде /start и приветствует пользователя
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Добро пожаловать, {message.chat.first_name} {message.chat.last_name} !')


@bot.message_handler(commands=['help'])
def help(message):
    text = 'Чтобы начать работу введите команду боту в следующим формате:\n <имя валюты> <в какую валюту перевести> <количество валюты>.\n Пользователь может увидить список доступных валют с помощью команды /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys:
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text',])
def convert(message):
    quote, base, amount = message.text.split(' ')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
    total_base = json.loads(r.content)[keys[base]]
    text = f'Цена {amount} {quote} в {base} - {float(total_base) * float(amount) } {keys[base]}'
    bot.send_message(message.chat.id, text)




bot.polling(none_stop=True)

