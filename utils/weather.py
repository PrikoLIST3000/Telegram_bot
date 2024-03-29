from config_reader import config
from aiohttp import ClientSession
from utils.logger import logger


class WeatherException(Exception):
    ...


class Weather:

    def __init__(self, city: str) -> None:
        self.url = config.weather_url.replace('city', city)

    async def __http_get(self, url: str) -> dict:
        async with ClientSession() as session:
            response = await session.get(url=url)

            if response.status == 200:
                return await response.json()
            else:
                error_text = (
                    f"Error during GET request to address {url}."
                    f"Error code: {response.status}"
                    f"Reason: {response.reason}"
                )
                logger.error(error_text)
                raise WeatherException(error_text)

    async def __temperature_info(self) -> tuple:
        weather_data = await self.__http_get(self.url)
        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])
        if temperature > 0:
            temperature = f'+{temperature}'
        if temperature_feels > 0:
            temperature_feels = f'+{temperature_feels}'
        return str(temperature), str(temperature_feels)

    async def answer(self) -> str:
        temperature, temperature_feels = await self.__temperature_info()
        return f"Температура <b>{temperature}</b>, \nОщущается как <b>{temperature_feels}</b>"
