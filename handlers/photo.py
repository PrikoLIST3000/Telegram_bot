from keyboards.to_main_menu import get_menu_kb
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from utils.photo_frame import Frame


router = Router()


@router.message(F.text.lower() == 'работа с фото')
async def photo_handler(message: Message) -> None:
    await message.answer("Жду фашу фотографию")


@router.message(F.photo)
async def photoshop(message: Message) -> None:
    photo_data = message.photo[-1]
    frame_path = await Frame(photo_data.file_id).create_frame()
    await message.answer("Вот ваша фотография")
    await message.answer_photo(FSInputFile(frame_path),
                               reply_markup=get_menu_kb())
