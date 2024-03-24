from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Главное меню", callback_data="Главное меню")
    return kb.as_markup(resize_keyboard=True)
