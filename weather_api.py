import time
import threading
import requests
from loguru import logger
import config
import os
import inspect
current_file = os.path.basename(__file__)
global weather_today
global weather_tomorrow
global weather_week
global weather_2week

logger.add(config.logger_path, format='{time} <{level}> {message}',
           rotation="10MB", compression="zip")
@logger.catch

def request_weather():
    time.sleep(5)
    try:
        res = requests.get(
            'http://api.open-meteo.com/v1/forecast?latitude=45.04&longitude=38.98&hourly=temperature_2m,'
            'precipitation,windspeed_10m,winddirection_10m&daily=sunrise,sunset&timezone=Europe%2FMoscow'
            '&forecast_days=14')
        data = res.json()
        weather_today={
            'weather_0': data['hourly']['temperature_2m'][0],
            'weather_6': data['hourly']['temperature_2m'][6],
            'weather_9': data['hourly']['temperature_2m'][9],
            'weather_12': data['hourly']['temperature_2m'][12],
            'weather_15': data['hourly']['temperature_2m'][15],
            'weather_18': data['hourly']['temperature_2m'][18],
            'weather_21': data['hourly']['temperature_2m'][21],
        }
        logger.info(f"Weather_today = {weather_today}, {res} ")
    except Exception as e:
        logger.error(f'{current_file} <{inspect.currentframe().f_code.co_name}> {e}')
    logger.info(f'{current_file} code:{res.status_code} ')




    time.sleep(1 * 60 * 60)


t = threading.Thread(target=request_weather)
t.start()
