from PIL import ImageOps, Image
from config_reader import config
from aiohttp import ClientSession
import io
import os
from faker import Faker
from utils.logger import logger


class Frame:

    def __init__(self, img_id) -> None:
        self.img_id = img_id
        self.img_name = Faker("ru_RU").postcode()

    async def _get_dict(self, url: str) -> dict:
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
                raise Exception(error_text)

    async def _get_content(self, url: str) -> bytes:
        async with ClientSession() as session:
            response = await session.get(url=url)

            if response.status == 200:
                buffer = b''
                async for data in response.content.iter_chunked(1024):
                    buffer += data
                return buffer
            else:
                error_text = (
                    f"Error during GET request to address {url}."
                    f"Error code: {response.status}"
                    f"Reason: {response.reason}"
                )
                logger.error(error_text)
                raise Exception(error_text)

    async def __get_image_path(self) -> str:
        print('Вошел')
        img_path = await self._get_dict(
            url=config.uri_info.replace(
                'BOT_TOKEN',
                config.bot_token.get_secret_value()
            ) + self.img_id
        )
        return img_path['result']['file_path']

    async def __get_image_info(self, img_path) -> bytes:
        print('Вошел')
        img = await self._get_content(
            url=config.uri.replace(
                'BOT_TOKEN',
                config.bot_token.get_secret_value()
            ) + img_path
        )
        return img

    async def __get_image(self):
        path = await self.__get_image_path()
        info = await self.__get_image_info(path)
        return info

    def __img_save(self, img: bytes) -> str:
        img = Image.open(io.BytesIO(img))
        img = ImageOps.expand(img, border=25, fill='#ff0000cc')
        os.makedirs("photos", exist_ok=True)
        img_path = f'photos/{self.img_name}.png'
        img.save(img_path, format="PNG")
        return img_path

    async def create_frame(self) -> str:
        img = await self.__get_image()
        img_path = self.__img_save(img)
        return img_path
