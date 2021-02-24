import os
import requests
from datetime import datetime


url = 'https://api.openweathermap.org/data/2.5/forecast'


def main():
    key = os.environ.get('WEATHER_KEY')
    location = get_location()
    unit = get_unit_of_measurement()
    if unit == 'imperial':
        readable_temp_unit = 'F'
    elif unit == 'metric':
        readable_temp_unit = 'C'
    else:
        readable_temp_unit = 'K'

    list_of_forecasts = get_forecast(location, unit, key)

    for forecast in list_of_forecasts:
        temp = forecast['main']['temp']
        windspeed = forecast['wind']['speed']
        timestamp = forecast['dt']
        forecast_date = datetime.fromtimestamp(timestamp)
        print(f'At {forecast_date} the temperature will be {temp}{readable_temp_unit}'
              f' and the wind speed will be {windspeed} Knots')


def get_location():
    city, country = '', ''
    while len(city) == 0:
        city = input('Please enter the city: ').strip()
    while len(country) != 2 or not country.isalpha():
        country = input('Please enter the two-letter country code: ').strip()
    location = f'{city},{country}'
    return location


def get_unit_of_measurement():
    units = input('For results in F: enter "1", for results in C: enter "2", for results in K: enter 3 ')
    while not units.isdigit() and int(units) in range(1, 3):
        units = input('For results in F: enter "1", for results in C: enter "2", for results in K: enter 3 ')

    units = int(units)
    if units == 1:
        unit = 'imperial'
    elif units == 2:
        unit = 'metric'
    else:
        unit = None
    return unit


def get_forecast(location, unit, key):
    try:
        query = {'q': location, 'units': unit, 'appid': key}
        response = requests.get(url, params=query)
        response.raise_for_status()  # Raise exception for 400 or 500 errors
        data = response.json()  # Will error also if response is not JSON
        weather_data = data['list']
        return weather_data

    except Exception as e:
        print(e)
        print(response.text)
        return None, e


def get_temp(weather_data):
    try:
        temp = weather_data['main']['temp']
        return temp
    except KeyError:
        print('This data is not in the format expected ')
        return 'Unknown'


if __name__ == '__main__':
    main()
