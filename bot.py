import asyncio
from aiogram import Bot
from config_reader import config
from handlers import weather, photo
from handlers.dispatcher import dispatcher
from utils.logger import logger


bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
dp = dispatcher
dp.include_routers(weather.router, photo.router)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info('Бот начал работу')
    asyncio.run(main())
