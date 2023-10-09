global today_response_text
global tomorrow_response_text
global week_response_text
global week2_response_text
import weather_api


def weather_response_text(json, last_update_time):
    header = str(f'<b>Доброго утра и прекрасного настроения\n\n</b>',
                 f'Погода сегодня в славном городе <b>Краснодаре</b> \nпо данным сервиса open-meteo.\n\n'
                 f'{last_update_time}\n')

    today_response_text = str(header +
                              f'<b>00:00   </b>{json["weather_0"]} {json["hourly_units"]["temperature_2m"]}\n'
                              f'<b>06:00   </b>{json["weather_6"]} °C\n'
                              f'<b>09:00   </b>{json["weather_9"]} °C\n'
                              f'<b>12:00   </b>{json["weather_12"]} °C\n'
                              f'<b>15:00   </b>{json["weather_15"]} °C\n'
                              f'<b>18:00   </b>{json["weather_18"]} °C\n'
                              f'<b>21:00   </b>{json["weather_21"]} °C\n')

    tomorrow_response_text = f''

    week_response_text = f''

    week2_response_text = f''
