from time import gmtime, strftime
import threading
import requests
from loguru import logger
import config
import os
import time

global json_wt_req


timeout = 60 * 60  # Тайм-аут запроса погоды(сек)
current_file = os.path.basename(__file__)
logger.add(config.logger_path, format='{time} <{level}> {message}',
           rotation="10MB", compression="zip")

def wind_direction_to_word(count):
    count = int(count)
# На вход подаётся число от 0 до 360 (градусы), направление ветра
# На выход ожидается условное буквенное обозначение
    if count < 22:
        return 'Северо-Восток'
    elif count < 67:
        return 'Восток'
    elif count < 112:
        return 'Юго-Восток'
    elif count < 157:
        return 'Юг'
    elif count < 202:
        return 'Юго-Запад'
    elif count < 247:
        return 'Запад'
    elif count < 292:
        return 'Северо-Запад'
    elif count < 337:
        return 'Север'
    else:
        return 'Север'




def weather_response_text(json, last_update_time):
    global today_response_text
    global tomorrow_response_text
    global week_response_text
    global week2_response_text
    header = str(f'<b>Доброго утра и прекрасного настроения\n\n</b>'
                 f'Погода сегодня в славном городе <b>Краснодаре</b> \nпо данным сервиса open-meteo:\n\n'
                 f'Время МСК\n{last_update_time}\n\n')

    today_response_text = header + (
        f'00:00\n'
        f'    Температура: <b>{json["hourly"]["temperature_2m"][0]}</b>{json["hourly_units"]["temperature_2m"]}\n'
        f'    Ветер:                <b>{json["hourly"]["windspeed_10m"][0]}</b> {json["hourly_units"]["windspeed_10m"]}'
        f'\n    Направление: {wind_direction_to_word(json["hourly"]["winddirection_10m"][0])}\n'


        f'06:00\n'
        f'    Температура: <b>{json["hourly"]["temperature_2m"][6]}</b>{json["hourly_units"]["temperature_2m"]}\n'
        f'    Ветер:                <b>{json["hourly"]["windspeed_10m"][6]}</b> {json["hourly_units"]["windspeed_10m"]}'
        f'\n    Направление: {wind_direction_to_word(json["hourly"]["winddirection_10m"][6])}\n'

        f'09:00\n'
        f'    Температура: <b>{json["hourly"]["temperature_2m"][9]}</b>{json["hourly_units"]["temperature_2m"]}\n'
        f'    Ветер:                <b>{json["hourly"]["windspeed_10m"][9]}</b> {json["hourly_units"]["windspeed_10m"]}'
        f'\n    Направление: {wind_direction_to_word(json["hourly"]["winddirection_10m"][9])}\n'

        f'12:00\n'
        f'    Температура: <b>{json["hourly"]["temperature_2m"][12]}</b>{json["hourly_units"]["temperature_2m"]}\n'
        f'    Ветер:                <b>{json["hourly"]["windspeed_10m"][12]}</b> {json["hourly_units"]["windspeed_10m"]}'
        f'\n    Направление: {wind_direction_to_word(json["hourly"]["winddirection_10m"][12])}\n'

        f'15:00\n'
        f'    Температура: <b>{json["hourly"]["temperature_2m"][15]}</b>{json["hourly_units"]["temperature_2m"]}\n'
        f'    Ветер:                <b>{json["hourly"]["windspeed_10m"][15]}</b> {json["hourly_units"]["windspeed_10m"]}'
        f'\n    Направление: {wind_direction_to_word(json["hourly"]["winddirection_10m"][15])}\n'

        f'18:00\n'
        f'    Температура: <b>{json["hourly"]["temperature_2m"][18]}</b>{json["hourly_units"]["temperature_2m"]}\n'
        f'    Ветер:                <b>{json["hourly"]["windspeed_10m"][18]}</b> {json["hourly_units"]["windspeed_10m"]}'
        f'\n    Направление: {wind_direction_to_word(json["hourly"]["winddirection_10m"][18])}\n'

        f'21:00\n'
        f'    Температура: <b>{json["hourly"]["temperature_2m"][21]}</b>{json["hourly_units"]["temperature_2m"]}\n'
        f'    Ветер:                <b>{json["hourly"]["windspeed_10m"][21]}</b> {json["hourly_units"]["windspeed_10m"]}'
        f'\n    Направление: {wind_direction_to_word(json["hourly"]["winddirection_10m"][21])}\n'
    )
    tomorrow_response_text = f' '
    week_response_text = f' '
    week2_response_text = f' '



# @logger.catch
def request_weather():
    time.sleep(2)
    try:
        res = requests.get(
            'http://api.open-meteo.com/v1/forecast?latitude=45.04&longitude=38.98&hourly=temperature_2m,'
            'precipitation,windspeed_10m,winddirection_10m&daily=sunrise,sunset&timezone=Europe%2FMoscow'
            '&forecast_days=14')
        js_wt_req = res.json()
        last_update_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        logger.info(f"Weather = {js_wt_req}")
        weather_response_text(js_wt_req, last_update_time)
        logger.info(f'{current_file} code:{res.status_code} ')
    except Exception as e:
        logger.error(f'{e}')

    logger.info(f'Next weather request in an {timeout / 60} minutes')
    time.sleep(timeout)


t = threading.Thread(target=request_weather)
t.start()


def weather_get(timers):
    get_weather = {
        'today': today_response_text,
        'tomorrow': tomorrow_response_text,
        'week': week_response_text,
        'week2': week2_response_text
    }
    return get_weather[timers]
