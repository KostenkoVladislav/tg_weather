import telebot
from telebot import types
from loguru import logger
import time
import text_response
import weather_api
from config import *

bot = telebot.TeleBot(mconf('tg'))


def today_send(call):
    bot.send_message(call.from_user.id, text_response.today_response_text)
    return


def tomorrow_send(call):
    bot.send_message(call.from_user.id, 'завтра')
    return

def week_send(call):
    bot.send_message(call.from_user.id, 'неделя')
    return

def week2_send(call):
    bot.send_message(call.from_user.id, 'две недели')
    return

def moon_send(call):
    bot.send_message(call.from_user.id, 'луна')
    return


def response_weather(message):
    bot.send_message(message.from_user.id,'')




'''
                     f'<b>Доброго утра и прекрасного настроения\n\n</b>'
                             f'Погода сегодня в славном городе <b>Краснодаре</b> \nпо данным сервиса open-meteo.\n\n'
                             f'{current_time}\n'
                             f'<b>00:00   </b>{weather_today["weather_0"]} °C\n'
                             f'<b>06:00   </b>{weather_today["weather_6"]} °C\n'
                             f'<b>09:00   </b>{weather_today["weather_9"]} °C\n'
                             f'<b>12:00   </b>{weather_today["weather_12"]} °C\n'
                             f'<b>15:00   </b>{weather_today["weather_15"]} °C\n'
                             f'<b>18:00   </b>{weather_today["weather_18"]} °C\n'
                             f'<b>21:00   </b>{weather_today["weather_21"]} °C\n',
                     parse_mode="html")
'''


# print(data, res)

def adm(iid):
    bot.send_message(759333833, f'Hey, new \'/start\' user.\n Id= @{iid}')


@bot.message_handler(commands=['start'])
# start и инициализация кнопок под сообщением
def start_message(message):
    adm(message.chat.username)
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
    call_dict = {'today': today_send,
                 'tomorrow': tomorrow_send,
                 'week': week_send,
                 'week2': week2_send,
                 'moon': moon_send
                 }

    call_dict[call.data](call)


@bot.message_handler(commands=['weather'])
def weather_message(message):
    start_message(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /start.")


import asyncio
# time.sleep(5)
logger.info(f"Application successful running")
asyncio.run(bot.polling())
