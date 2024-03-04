import telebot   
from extensions import API, APIException
from config_bot import TOKEN

bot = telebot.TeleBot(TOKEN)


# Обрабатывается при команде /start и приветствует пользователя
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Добро пожаловать, {message.chat.first_name} {message.chat.last_name} !')

# Обрабатывается при команде /help и даёт инструкции по использование телеграмм бота
@bot.message_handler(commands=['help'])
def help(message):
    text = 'Чтобы начать работу введите команду боту в следующим формате:\n <имя валюты> <в какую валюту перевести> <количество валюты>.\n Пользователь может увидить список доступных валют с помощью команды /values'
    bot.reply_to(message, text)

# Выводит доступный список валют при команде /values
@bot.message_handler(commands=['values'])
def values(message):
    api = API()
    text = api.get_values()
    bot.reply_to(message, text)


# Обрабатывает запрос пользователя и выдаёт информацию по определенным атрибутам.
@bot.message_handler(content_types=['text',])
def convert(message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
                raise APIException('Слишком много параметров!')
        quote, base, amount = values
        total_base = API.get_price(base, quote, amount)
    except APIException as e:
         bot.reply_to(message, f'Ошибка пользователя. \n {e}')
    except Exception as e:
         bot.send_message(message, f'Не удалось обработь команду\n{e}')
    else:
         text = f'Цена {amount} {quote} в {base} - {float(total_base) * float(amount) }'
         bot.send_message(message.chat.id, text)
         
    





bot.polling(none_stop=True)

