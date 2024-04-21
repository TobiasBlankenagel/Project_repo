import requests
import datetime

def get_temperature(city):
    api_key = "5609e5c95ae59033e36538f65e15b9da"
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    temperature = data["main"]["temp"]
    time = datetime.datetime.now()

    return f"Die Temperatur in {city} um {time} ist {temperature} Grad Celsius."

print(get_temperature("Berlin"))