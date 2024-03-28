from keyboards.to_main_menu import get_menu_kb
from keyboards.for_photo import get_photo_kb
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from utils.photo_frame import Frame
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class PhotoChoose(StatesGroup):
    choosing_photo = State()


router = Router()


@router.message(StateFilter(None), F.text.lower() == 'работа с фото')
async def photo_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Что сделать с фото?", reply_markup=get_photo_kb())
    await state.set_state(PhotoChoose.choosing_photo)


@router.message(PhotoChoose.choosing_photo, F.text.lower() == 'наложить рамку')
async def choosing_photo(message: Message, state: FSMContext) -> None:
    await message.answer("Жду вашу фотографию")


@router.message(F.photo, PhotoChoose.choosing_photo)
async def photoshop(message: Message, state: FSMContext) -> None:
    photo_data = message.photo[-1]
    framed_photo_path = await Frame(photo_data.file_id).create_frame()
    await message.answer("Вот ваша фотография")
    await message.answer_photo(FSInputFile(framed_photo_path),
                               reply_markup=get_menu_kb())
    Frame.img_delete(framed_photo_path)
    await state.clear()
