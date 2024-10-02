import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

# Создание клавиатуры с кнопками
markup = ReplyKeyboardMarkup(resize_keyboard=True)
help_button = KeyboardButton('/help')
values_button = KeyboardButton('/values')
markup.add(help_button, values_button)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ('Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> '
            '<в какую валюту перевести> '
            '<количество переводимой валюты>\nМожно увидеть список всех доступных валют, введя команду /values')
    bot.reply_to(message, text, reply_markup=markup)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text, reply_markup=markup)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введите правильное количество параметров')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}', reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}', reply_markup=markup)
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text, reply_markup=markup)


bot.polling(non_stop=True)