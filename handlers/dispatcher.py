from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.for_start import get_start_kb
from middlewares.actions import SaveMessageInLogMiddleware
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from middlewares.db import DataBaseSession
from database.engine import session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_add_user, orm_get_user
# from aiogram.fsm.state import StatesGroup, State


dispatcher = Dispatcher()
dispatcher.message.middleware(SaveMessageInLogMiddleware())
dispatcher.update.middleware(DataBaseSession(session_pool=session_maker))
#   dispatcher.message.middleware(ChatActionMiddleware())


@dispatcher.message(F.text.lower() == "главное меню")
@dispatcher.message(Command("start"))
async def start(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.clear()
    check_user = await orm_get_user(session, message.from_user.id)
    if check_user is None:
        await orm_add_user(
            id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username
        )
        await session.commit()
    await message.answer("Выберите действие:", reply_markup=get_start_kb())


@dispatcher.callback_query(F.data == "Главное меню")
async def start_callback(callback: CallbackQuery) -> None:
    await callback.message.answer("Выберите действие:", reply_markup=get_start_kb())


@dispatcher.message(StateFilter(None), Command(commands=["cancel"]))
@dispatcher.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(text="Нечего отменять")
    await message.answer("Выберите действие:", reply_markup=get_start_kb())


@dispatcher.message(Command(commands=["cancel"]))
@dispatcher.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Действие отменено")
    await message.answer("Выберите действие:", reply_markup=get_start_kb())
