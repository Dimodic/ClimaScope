import requests
import aiohttp
import asyncio

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_current_temperature_sync(city, api_key, units = "metric"):
    """
    Синхронно запрашивает текущую температуру через OpenWeatherMap API.
    """
    params = {"q": city, "appid": api_key, "units": units}
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if response.status_code != 200:
        return {"error": data.get("message", "Ошибка запроса")}
    temperature = data["main"]["temp"]
    return {"temperature": temperature}

async def get_current_temperature_async(city, api_key, units = "metric"):
    """
    Асинхронно запрашивает текущую температуру через OpenWeatherMap API.
    """
    params = {"q": city, "appid": api_key, "units": units}
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, params=params) as response:
            data = await response.json()
            if response.status != 200:
                return {"error": data.get("message", "Ошибка запроса")}
            temperature = data["main"]["temp"]
            return {"temperature": temperature}

def get_current_temperature(city, api_key, method = "sync", units = "metric"):
    """
    Выбирает синхронный или асинхронный способ получения текущей температуры.
    """
    if method == "sync":
        return get_current_temperature_sync(city, api_key, units)
    elif method == "async":
        return asyncio.run(get_current_temperature_async(city, api_key, units))
    else:
        return {"error": "Неверный метод запроса"}
