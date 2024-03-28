import asyncio
from aiogram import Bot
from config_reader import config
from handlers import weather, photo, quiz
from handlers.dispatcher import dispatcher
from utils.logger import logger
from database.engine import create_db, drop_db


bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
dp = dispatcher
dp.include_routers(weather.router, photo.router, quiz.router)


async def on_startup():
    logger.info('Бот начал работу')
    await create_db()


async def on_shutdown():
    logger.info('Бот завершил работу')
    await drop_db()


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
