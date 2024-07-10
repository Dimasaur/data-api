# pylint: disable=missing-module-docstring

import sys
import urllib.parse
import requests

BASE_URI = "https://weather.lewagon.com/"
Geo_Directive = "geo/1.0/direct?q="
Weather_Forecast = "/data/2.5/forecast?"


def search_city(query):
    '''
    Look for a given city. If multiple options are returned, have the user choose between them.
    Return one city (or None)
    '''
    response = requests.get(f"{BASE_URI}{Geo_Directive}{query}&limit=5",params={'name': query, 'format': 'json', 'jscmd':'data'},).json()
    for i, x in enumerate(range(len(response)),start=1):
        city = response[x]['name']+ ", " + response[x]['country']
        print(f"{i} - {city}")

    if not response:
        return None

    if len(response) == 1:
        choice = 1
        chosen_city = response[choice-1]
        return chosen_city
    else:
        while True:
            try:
                choice = int(input("Select a city from the options (number): "))
                if 1 <= choice <= len(response):
                    print(f"You have chosen option {choice}! This is {response[choice-1]['name']}, {response[x]['country']}")
                    chosen_city = response[choice-1]
                    return chosen_city
                else:
                    print("Invalid choice. Please enter a number that corresponds to a city")
            except ValueError:
                print("Invalid input. Please enter a valid number")


def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''
    forecast = requests.get(f"{BASE_URI}{Weather_Forecast}lat={lat}&lon={lon}", params={'format': 'json', 'jscmd':'data'},).json()
    return forecast['list']



def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    chosen_city = search_city(query)
    lat = chosen_city['lat']
    lon = chosen_city['lon']
    forecast = weather_forecast(lat,lon)
    for x in range(0,40,8):
        if "15:00:00" in forecast[x]['dt_txt']:
            print(f"{forecast[x]['dt_txt'][0:10]}: {forecast[x]['weather'][0]['description'].capitalize()}, {round(forecast[x]['main']['temp_max']-273,1)}")


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
