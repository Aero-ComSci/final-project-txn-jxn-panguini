import requests

API_KEY = "c995b59bdfc34f3297c174427252805 "
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def get_weather_data(city):
    if not city:
        raise ValueError("City name must be provided.")
    
    params = {"key": API_KEY, "q": city}
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather = data["current"]["condition"]["text"]
        temp = data["current"]["temp_f"]
        name = data["location"]["name"]
        country = data["location"]["country"]
        weathericon = data["current"]["condition"]["icon"]
        windspeed = data["current"]["wind_mph"]
        region = data["location"]["region"]

        print(data)
        return weather, temp, name, country, weathericon, windspeed, region
    else:
        raise Exception("City not found!")
