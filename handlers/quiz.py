from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram import Router, F
from aiogram.filters import StateFilter
from keyboards.for_quiz import get_start_quiz_kb
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from database.models import User


router = Router()

questions = {
    1: {
        'text': 'Сколько планет в Солнечной системе?',
        'options': ['8', '9', '10'],
        'correct_answer': '8'
    },
    2: {
        'text': 'Какая самая длинная река в мире?',
        'options': ['Нил', 'Амазонка', 'Янцзы'],
        'correct_answer': 'Амазонка'
    },
    3: {
        'text': 'Какое животное является символом США?',
        'options': ['Орёл', 'Медведь', 'Змея'],
        'correct_answer': 'Орёл'
    },
    4: {
        'text': 'Какая самая высокая гора в мире?',
        'options': ['Эверест', 'Килиманджаро', 'Эльбрус'],
        'correct_answer': 'Эверест'
    },
    5: {
        'text': 'В каком году произошло открытие Америки Колумбом?',
        'options': ['1492', '1520', '1453'],
        'correct_answer': '1492'
    }
}


class Quiz(StatesGroup):
    start_quiz = State()
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()


@router.message(StateFilter(None), F.text.lower() == 'прохождение теста')
async def send_welcome(message: Message, state: FSMContext, session: AsyncSession):
    query = select(User.complete_quiz).where(User.complete_quiz == True and User.id == message.from_user.id)
    result = await session.execute(query)
    if result.scalar():
        await message.reply("Ой, ты уже проходил викторину", reply_markup=get_start_quiz_kb())
    else:
        await state.set_state(Quiz.start_quiz)
        await message.reply("Привет! Давай начнем викторину", reply_markup=get_start_quiz_kb())


@router.message(Quiz.start_quiz, F.text.lower() == 'начать')
async def start_quiz(message: Message, state: FSMContext):
    await state.set_state(Quiz.q1)
    question_id = 1
    question = questions[question_id]['text']
    options = questions[question_id]['options']
    options_str = ', '.join(options)
    await state.update_data(correct_answers=0)
    await message.reply(f"{question}\n\nВарианты ответа: {options_str}")


@router.message(Quiz.q1)
async def answer_q1(message: Message, state: FSMContext):
    if message.text in questions[1]['options']:
        if message.text == questions[1]['correct_answer']:
            await state.update_data(correct_answers=1)
        await state.set_state(Quiz.q2)
        question_id = 2
        question = questions[question_id]['text']
        options = questions[question_id]['options']
        options_str = ', '.join(options)
        await message.reply(f"{question}\n\nВарианты ответа: {options_str}")
    else:
        await message.reply("Выберите ответ из предложенных вариантов: 8, 9, 10.")


@router.message(Quiz.q2)
async def answer_q2(message: Message, state: FSMContext):
    if message.text in questions[2]['options']:
        if message.text == questions[2]['correct_answer']:
            correct_answers = await state.get_data()
            correct_answers = correct_answers['correct_answers'] + 1
            await state.update_data(correct_answers=correct_answers)
        await state.set_state(Quiz.q3)
        question_id = 3
        question = questions[question_id]['text']
        options = questions[question_id]['options']
        options_str = ', '.join(options)
        await message.reply(f"{question}\n\nВарианты ответа: {options_str}")
    else:
        await message.reply("Выберите ответ из предложенных вариантов: Нил, Амазонка, Янцзы.")


@router.message(Quiz.q3)
async def answer_q3(message: Message, state: FSMContext):
    if message.text in questions[3]['options']:
        if message.text == questions[3]['correct_answer']:
            correct_answers = await state.get_data()
            correct_answers = correct_answers['correct_answers'] + 1
            await state.update_data(correct_answers=correct_answers)
        await state.set_state(Quiz.q4)
        question_id = 4
        question = questions[question_id]['text']
        options = questions[question_id]['options']
        options_str = ', '.join(options)
        await message.reply(f"{question}\n\nВарианты ответа: {options_str}")
    else:
        await message.reply("Выберите ответ из предложенных вариантов: Орёл, Медведь, Змея.")


@router.message(Quiz.q4)
async def answer_q4(message: Message, state: FSMContext):
    if message.text in questions[4]['options']:
        if message.text == questions[4]['correct_answer']:
            correct_answers = await state.get_data()
            correct_answers = correct_answers['correct_answers'] + 1
            await state.update_data(correct_answers=correct_answers)
        await state.set_state(Quiz.q5)
        question_id = 5
        question = questions[question_id]['text']
        options = questions[question_id]['options']
        options_str = ', '.join(options)
        await message.reply(f"{question}\n\nВарианты ответа: {options_str}")
    else:
        await message.reply("Выберите ответ из предложенных вариантов: Эверест, Килиманджаро, Эльбрус.")


@router.message(Quiz.q5)
async def answer_q5(message: Message, state: FSMContext, session: AsyncSession):
    if message.text in questions[5]['options']:
        if message.text == questions[5]['correct_answer']:
            correct_answers = await state.get_data()
            correct_answers = correct_answers['correct_answers'] + 1
            await state.update_data(correct_answers=correct_answers)
        result = await state.get_data()
        await message.reply(f"Поздравляем! Вы дали {result['correct_answers']} правильных ответов из 5.")
        await state.clear()
        query = update(User).where(User.id == message.from_user.id).values(complete_quiz=True)
        await session.execute(query)
        await session.commit()
    else:
        await message.reply("Выберите ответ из предложенных вариантов: 1492, 1520, 1453.")
