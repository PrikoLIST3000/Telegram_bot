from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(
        KeyboardButton(text="Погода"),
        KeyboardButton(text="Работа с фото")
    )
#    kb.row(KeyboardButton(text="Прохождение теста"))
    return kb.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите действие',
        one_time_keyboard=True
    )
