from utils.weather import Weather
from keyboards.for_weather import get_weather_kb
from keyboards.to_main_menu import get_menu_kb
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
# from middlewares.actions import IsItCityMiddleware

available_city_names = ['Москва', 'Санкт-Петербург']


class CityChoose(StatesGroup):
    choosing_city = State()


router = Router()
# router.message.middleware(IsItCityMiddleware())


@router.message(StateFilter(None), F.text.lower() == "погода")
async def start_weather(message: Message, state: FSMContext) -> None:
    await message.answer("Выберите город или введите свой", reply_markup=get_weather_kb())
    await state.set_state(CityChoose.choosing_city)


@router.message(CityChoose.choosing_city, F.text.in_(available_city_names))
async def city_in_list(message: Message, state: FSMContext) -> None:
    await state.clear()
    weather = Weather(f'{message.text}')
    await message.answer(await weather.answer(), reply_markup=get_menu_kb())


@router.message(CityChoose.choosing_city)
async def another_city(message: Message, state: FSMContext) -> None:
    try:
        weather = Weather(f'{message.text}')
        await message.answer(await weather.answer(), reply_markup=get_menu_kb())
        await state.clear()
    except Exception:
        await message.reply("Проверьте название города", reply_markup=get_weather_kb())
        await state.set_state(CityChoose.choosing_city)
