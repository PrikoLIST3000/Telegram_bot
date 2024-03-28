from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_start_quiz_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text='Начать')
    kb.button(text='Отмена')
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
