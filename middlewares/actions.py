from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from utils.logger import logger


class SaveMessageInLogMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """Сохранение сообщений пользователя в лог"""
        logger.info(f'Сообщение от пользователя: {event.from_user.username}/{event.from_user.id}')
        if True:
            logger.info(f'{event.from_user.username}/BOT: {event.html_text}')
            await handler(event, data)
        else:
            return await handler(event, data)

# class IsItCityMiddleware(BaseMiddleware):
#
#    async def __call__(
#        self,
#        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
#        event: CallbackQuery,
#        data: Dict[str, Any]
#    ) -> Any:
#        if Weather.is_exists(f'{event.html_text}'):
#            await handler(event, data)
#        else:
#            return await handler(event, data)
