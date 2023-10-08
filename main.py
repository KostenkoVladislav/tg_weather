import telebot
from telebot import types
import datetime
import pprint
import json
from config import *
from loguru import logger
import time
import weather_api






def today_send():
    print('')


def tomorrow_send():
    print('')


def week_send():
    print('')


def month_send():
    print('')


def moon_send():
    print('')


bot = telebot.TeleBot(mconf('tg'))



@bot.message_handler(commands=['weather'])
def weather_msg(message):
    now = datetime.datetime.now()
    current_time = str(now.strftime("%d/%m/ %H:%M"))
    data = ''
    try:
        res = requests.get(
            'http://api.open-meteo.com/v1/forecast?latitude=45.04&longitude=38.98&hourly=temperature_2m,'
            'precipitation,windspeed_10m,winddirection_10m&daily=sunrise,sunset&timezone=Europe%2FMoscow')
        data = res.json()
        weather_today = {
            'weather_0': data['hourly']['temperature_2m'][0],
            'weather_6': data['hourly']['temperature_2m'][6],
            'weather_9': data['hourly']['temperature_2m'][9],
            'weather_12': data['hourly']['temperature_2m'][12],
            'weather_15': data['hourly']['temperature_2m'][15],
            'weather_18': data['hourly']['temperature_2m'][18],
            'weather_21': data['hourly']['temperature_2m'][21],
        }
    except Exception as e:
        print("Exception (find):", e)
    data = str(data)
    len_data = len(data)
    while len_data > 4096:
        bot.send_message(message.from_user.id, data[len_data - 4096:len_data])
        len_data -= 4096

    bot.send_message(message.from_user.id, len(data))

    # bot.send_message(message.from_user.id, str(data))
    pprint.pprint(res.json())
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
    bot.send_message(759333833, f'Hey, new start user.\n Id= {iid}')

@bot.message_handler(commands=['start'])
# start и инициализация кнопок под сообщением
def start_message(message):
    adm(message.chat.username)
    #   bot.send_message(message.from_user.id, )
    keyboard = types.InlineKeyboardMarkup()
    # наша клавиатура
    key_1_1 = types.InlineKeyboardButton(text='Сегодня', callback_data='today')
    keyboard.add(key_1_1)  # добавляем кнопку в клавиатуру
    key_1_2 = types.InlineKeyboardButton(text='Завтра', callback_data='tomorrow')
    keyboard.add(key_1_2)
    key_2_1 = types.InlineKeyboardButton(text='Неделя', callback_data='week')
    keyboard.add(key_2_1)
    key_2_2 = types.InlineKeyboardButton(text='Месяц', callback_data='month')
    keyboard.add(key_2_2)
    key_19_03 = types.InlineKeyboardButton(text='ЮФ-1903', callback_data='moon')
    keyboard.add(key_19_03)
    bot.send_message(message.from_user.id, 'Погода по данным open-meteo',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)  # присвоение группы
def callback_worker(call):
    call_dict = dict(today=today_send(),
                     tomorrow=tomorrow_send(),
                     week=week_send(),
                     moon=moon_send()
                     )
    call_dict[call]


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /start.")


import asyncio
logger.info(f"Application successful running")
asyncio.run(bot.polling())

