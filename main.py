import telebot
from telebot import types
from loguru import logger
import time
import weather_api
from config import *



bot = telebot.TeleBot(mconf('tg'))


@bot.message_handler(commands=['start'])
# start и инициализация кнопок под сообщением
def start_message(message):
    logger.info(f'{message.chat.username}, command = start')
    keyboard = types.InlineKeyboardMarkup()
    key_today = types.InlineKeyboardButton(text='Сегодня', callback_data='today')
    keyboard.add(key_today)
    key_tomorrow = types.InlineKeyboardButton(text='Завтра', callback_data='tomorrow')
    keyboard.add(key_tomorrow)
    key_week = types.InlineKeyboardButton(text='Неделя', callback_data='week')
    keyboard.add(key_week)
    key_month = types.InlineKeyboardButton(text='Две недели', callback_data='week2')
    keyboard.add(key_month)
    bot.send_message(message.from_user.id, 'Погода по данным open-meteo',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)  # присвоение группы
def callback_worker(call):
    call_dict = {'today': [weather_api.weather_get('today'), 'сегодня'],
                 'tomorrow': [weather_api.weather_get('tomorrow'), 'завтра'],
                 'week': [weather_api.weather_get('week'), 'неделю'],
                 'week2': [weather_api.weather_get('week2'), 'две недели']
                 }

    logger.info(f'{call.data}, {call.from_user.username}')

    bot.send_message(call.from_user.id, f'{call_dict[call.data][0]}', parse_mode="html")

@bot.message_handler(commands=['weather'])
def weather_message(message):
    start_message(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /start.")


import time
import asyncio
time.sleep(2)
logger.info(f"Application successful running")
asyncio.run(bot.polling())
