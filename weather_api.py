import time
import threading
import requests
from loguru import logger
import config
import os
import inspect
global json_wt_req
from time import gmtime, strftime
import text_response

timeout = 60*60  # Тайм-аут запроса погоды(сек)
current_file = os.path.basename(__file__)
logger.add(config.logger_path, format='{time} <{level}> {message}',
           rotation="10MB", compression="zip")


# @logger.catch
def request_weather():
    time.sleep(5)
    try:
        res = requests.get(
            'http://api.open-meteo.com/v1/forecast?latitude=45.04&longitude=38.98&hourly=temperature_2m,'
            'precipitation,windspeed_10m,winddirection_10m&daily=sunrise,sunset&timezone=Europe%2FMoscow'
            '&forecast_days=14')
        js_wt_req = res.json()
        last_update_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        logger.info(f"Weather = {js_wt_req}")
        text_response.weather_response_text(js_wt_req, last_update_time)
    except Exception as e:
        logger.error(f'{current_file} <{inspect.currentframe().f_code.co_name}> {e}')

    logger.info(f'{current_file} code:{res.status_code} ')
    logger.info(f'Next weather request in an {timeout/60} minutes')
    time.sleep(timeout)


t = threading.Thread(target=request_weather)
t.start()
