from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_weather_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Москва")
    kb.button(text="Санкт-Петербург")
    kb.button(text='Отмена')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True,
                        input_field_placeholder='Выберите город или введите свой', one_time_keyboard=True)
